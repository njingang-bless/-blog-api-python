from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import sqlite3
import json

app = FastAPI(title="Blog API", description="A simple blog API", version="1.0.0")

# ========== DATABASE SETUP ==========
def create_table():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()  # Create table when app starts

# ========== MODELS (Pydantic) ==========
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: str
    category: str
    tags: List[str]

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    category: str
    tags: List[str]
    date: str

# ========== HELPER FUNCTIONS ==========
def article_from_row(row):
    """Convert database row to article dictionary"""
    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "author": row[3],
        "category": row[4],
        "tags": row[5].split(",") if row[5] else [],
        "date": row[6]
    }

# ========== API ENDPOINTS ==========

# Welcome route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Blog API",
        "endpoints": {
            "Create article": "POST /api/articles",
            "Get all articles": "GET /api/articles",
            "Get article by ID": "GET /api/articles/{id}",
            "Update article": "PUT /api/articles/{id}",
            "Delete article": "DELETE /api/articles/{id}",
            "Search articles": "GET /api/articles/search?query=text",
            "Filter articles": "GET /api/articles?category=Tech&author=John&date=2026-03-19"
        }
    }

# 1. CREATE article - POST /api/articles
@app.post("/api/articles", status_code=201)
def create_article(article: ArticleCreate):
    # Validation
    if not article.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    if not article.author.strip():
        raise HTTPException(status_code=400, detail="Author cannot be empty")
    
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Convert tags list to string
    tags_str = ",".join(article.tags)
    today = date.today().isoformat()
    
    cursor.execute('''
        INSERT INTO articles (title, content, author, category, tags, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (article.title, article.content, article.author, article.category, tags_str, today))
    
    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    
    return {"message": "Article created successfully", "id": article_id}

# 2. GET all articles (with filters) - GET /api/articles
@app.get("/api/articles", response_model=List[ArticleResponse])
def get_articles(
    category: Optional[str] = Query(None, description="Filter by category"),
    author: Optional[str] = Query(None, description="Filter by author"),
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)")
):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Build query with filters
    query = "SELECT * FROM articles WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    if author:
        query += " AND author = ?"
        params.append(author)
    if date:
        query += " AND date = ?"
        params.append(date)
    
    query += " ORDER BY date DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [article_from_row(row) for row in rows]

# 3. GET single article - GET /api/articles/{id}
@app.get("/api/articles/{id}", response_model=ArticleResponse)
def get_article(id: int):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")
    
    return article_from_row(row)

# 4. UPDATE article - PUT /api/articles/{id}
@app.put("/api/articles/{id}")
def update_article(id: int, article_update: ArticleUpdate):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")
    
    # Get current values
    current = article_from_row(row)
    
    # Update only provided fields
    new_title = article_update.title if article_update.title is not None else current["title"]
    new_content = article_update.content if article_update.content is not None else current["content"]
    new_category = article_update.category if article_update.category is not None else current["category"]
    new_tags = article_update.tags if article_update.tags is not None else current["tags"]
    
    # Convert tags to string
    tags_str = ",".join(new_tags)
    
    cursor.execute('''
        UPDATE articles 
        SET title = ?, content = ?, category = ?, tags = ?
        WHERE id = ?
    ''', (new_title, new_content, new_category, tags_str, id))
    
    conn.commit()
    conn.close()
    
    return {"message": "Article updated successfully"}

# 5. DELETE article - DELETE /api/articles/{id}
@app.delete("/api/articles/{id}")
def delete_article(id: int):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")
    
    cursor.execute("DELETE FROM articles WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return {"message": "Article deleted successfully"}

# 6. SEARCH articles - GET /api/articles/search?query=text
@app.get("/api/articles/search", response_model=List[ArticleResponse])
def search_articles(query: str = Query(..., min_length=1, description="Search term")):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT * FROM articles 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY date DESC
    ''', (search_term, search_term))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [article_from_row(row) for row in rows]

# Run with: hypercorn blog_complete:app --reload