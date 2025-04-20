from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.data.database import get_db
from app.domain.models.book import BookCreate, BookResponse, BookUpdate
from app.domain.services.book_service import BookService
from app.api.auth import get_current_active_user
from app.domain.models.user import UserInDB

router = APIRouter()

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Create a new book
    """
    book_service = BookService(db)
    return await book_service.create_book(book)

@router.get("/", response_model=List[BookResponse])
async def read_books(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all books with optional filtering
    """
    book_service = BookService(db)
    return await book_service.get_books(skip=skip, limit=limit, title=title, author=author, genre=genre)

@router.get("/{book_id}", response_model=BookResponse)
async def read_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a specific book by ID
    """
    book_service = BookService(db)
    book = await book_service.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Update a book's information
    """
    book_service = BookService(db)
    updated_book = await book_service.update_book(book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Delete a book
    """
    book_service = BookService(db)
    result = await book_service.delete_book(book_id)
    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return None

@router.get("/{book_id}/summary", response_model=dict)
async def get_book_summary(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a summary and aggregated rating for a book
    """
    from app.domain.services.summary_service import SummaryService
    
    book_service = BookService(db)
    book = await book_service.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    summary_service = SummaryService(db)
    return await summary_service.get_book_summary(book_id)