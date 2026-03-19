# Blog API

A simple blog API built with FastAPI and SQLite.

## Features
- Create, read, update, delete articles
- Search articles
- Filter by category, author, date

## API Endpoints
- POST /api/articles - Create article
- GET /api/articles - Get all articles
- GET /api/articles/{id} - Get one article
- PUT /api/articles/{id} - Update article
- DELETE /api/articles/{id} - Delete article
- GET /api/articles/search?query= - Search articles

## How to Run
1. Install Python
2. Run: pip install fastapi uvicorn
3. Run: uvicorn app:app --reload
4. Open browser: http://localhost:8000

## Technologies
- FastAPI
- SQLite
- Python