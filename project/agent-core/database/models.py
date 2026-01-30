from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SessionDB(Base):
    """Database model for sessions"""
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String, default="active")
    
    messages = relationship("MessageDB", back_populates="session", cascade="all, delete-orphan")


class MessageDB(Base):
    """Database model for messages"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    
    session = relationship("SessionDB", back_populates="messages")
