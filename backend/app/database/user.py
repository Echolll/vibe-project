from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    avatar = Column(String)
    bio = Column(String)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())

    created_events = relationship('Events', back_populates = 'creator', foreign_keys = 'Events.creator_id')
    participant = relationship('Participants', back_populates = 'user', foreign_keys = 'Participants.user_id')
    sent_reviews = relationship('Reviews', back_populates = 'from_user', foreign_keys = 'Reviews.from_user_id')
    received_reviews = relationship('Reviews', back_populates = 'to_user', foreign_keys = 'Reviews.to_user_id')
