from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as DBSession

from config import config
from .models import Base, SessionDB, MessageDB
from models.session import Session, Message, SessionStatus


class DatabaseService:
    """Service for managing database operations"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = config.database_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def create_session(self) -> Session:
        """Create a new session"""
        session_id = str(uuid.uuid4())
        
        db = self.SessionLocal()
        try:
            db_session = SessionDB(
                id=session_id,
                created_at=datetime.now(),
                status=SessionStatus.ACTIVE.value
            )
            db.add(db_session)
            db.commit()
            
            return Session(
                id=session_id,
                created_at=db_session.created_at,
                messages=[],
                status=SessionStatus.ACTIVE
            )
        finally:
            db.close()
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        db = self.SessionLocal()
        try:
            db_session = db.query(SessionDB).filter(SessionDB.id == session_id).first()
            if not db_session:
                return None
            
            messages = [
                Message(
                    role=msg.role,
                    content=msg.content,
                    timestamp=msg.timestamp
                )
                for msg in db_session.messages
            ]
            
            return Session(
                id=db_session.id,
                created_at=db_session.created_at,
                messages=messages,
                status=SessionStatus(db_session.status)
            )
        finally:
            db.close()
    
    def save_message(self, session_id: str, role: str, content: str) -> None:
        """Save a message to session"""
        db = self.SessionLocal()
        try:
            message = MessageDB(
                session_id=session_id,
                role=role,
                content=content,
                timestamp=datetime.now()
            )
            db.add(message)
            db.commit()
        finally:
            db.close()
    
    def update_session_status(self, session_id: str, status: SessionStatus) -> None:
        """Update session status"""
        db = self.SessionLocal()
        try:
            db_session = db.query(SessionDB).filter(SessionDB.id == session_id).first()
            if db_session:
                db_session.status = status.value
                db.commit()
        finally:
            db.close()
    
    def get_all_sessions(self) -> List[Session]:
        """Get all sessions"""
        db = self.SessionLocal()
        try:
            db_sessions = db.query(SessionDB).order_by(SessionDB.created_at.desc()).all()
            
            sessions = []
            for db_session in db_sessions:
                messages = [
                    Message(
                        role=msg.role,
                        content=msg.content,
                        timestamp=msg.timestamp
                    )
                    for msg in db_session.messages
                ]
                
                sessions.append(Session(
                    id=db_session.id,
                    created_at=db_session.created_at,
                    messages=messages,
                    status=SessionStatus(db_session.status)
                ))
            
            return sessions
        finally:
            db.close()
