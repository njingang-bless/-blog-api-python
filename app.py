from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import sqlite3

app = FastAPI()

# ========== DATABASE SETUP ==========
def init_db():
    conn = sqlite3.connect('blog.db')
    conn.execute('''
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

init_db()  # Create table when app starts

# ========== MODELS ==========
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

# ========== HELPER FUNCTION ==========
def row_to_dict(row):
    """Convert database row to dictionary"""
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

# Welcome endpoint
@app.get("/")
def home():
    return {
        "message": "Blog API is working!",
        "endpoints": {
            "GET /": "This message",
            "POST /api/articles": "Create new article",
            "GET /api/articles": "Get all articles",
            "GET /api/articles/{id}": "Get one article",
            "PUT /api/articles/{id}": "Update article",
            "DELETE /api/articles/{id}": "Delete article",
            "GET /api/articles/search?query=": "Search articles"
        }
    }

# 1. CREATE article
@app.post("/api/articles")
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
    today = str(date.today())
    
    cursor.execute(
        "INSERT INTO articles (title, content, author, category, tags, date) VALUES (?, ?, ?, ?, ?, ?)",
        (article.title, article.content, article.author, article.category, tags_str, today)
    )
    
    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    
    return {
        "message": "Article created successfully",
        "id": article_id,
        "date": today
    }

# 2. GET all articles
@app.get("/api/articles")
def get_articles():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [row_to_dict(row) for row in rows]

# 3. GET one article
@app.get("/api/articles/{id}")
def get_article(id: int):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")
    
    return row_to_dict(row)

# 4. UPDATE article
@app.put("/api/articles/{id}")
def update_article(id: int, article: ArticleUpdate):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    # Check if article exists
    cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")
    
    # Get current values
    current = row_to_dict(row)
    
    # Update only provided fields
    new_title = article.title if article.title is not None else current["title"]
    new_content = article.content if article.content is not None else current["content"]
    new_category = article.category if article.category is not None else current["category"]
    new_tags = article.tags if article.tags is not None else current["tags"]
    
    # Convert tags to string
    tags_str = ",".join(new_tags)
    
    cursor.execute(
        "UPDATE articles SET title=?, content=?, category=?, tags=? WHERE id=?",
        (new_title, new_content, new_category, tags_str, id)
    )
    
    conn.commit()
    conn.close()
    
    return {"message": "Article updated successfully"}

# 5. DELETE article
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

# 6. SEARCH articles
@app.get("/api/articles/search")
def search_articles(query: str):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute(
        "SELECT * FROM articles WHERE title LIKE ? OR content LIKE ? ORDER BY date DESC",
        (search_term, search_term)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [row_to_dict(row) for row in rows]