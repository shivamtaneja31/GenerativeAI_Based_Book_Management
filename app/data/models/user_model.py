from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.data.database import Base

class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="user")
