from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user" # Iska naam 'user' hi rehne do kyunki tumhare routers mein yahi use ho raha hai
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship: Ek user ke bohot saare tasks ho sakte hain
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    published = Column(Boolean, default=True) # Schema mein bhi 'published' hi hai ab ✅
    
    # Foreign Key: Ye batayega ki ye task kis user ka hai
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship: Task se wapas user ka data dekhne ke liye
    owner = relationship("User", back_populates="tasks")