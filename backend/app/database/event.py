from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.database import Base
from datetime import datetime

class Events(Base):
    __tablename__: str = 'Events'

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    description = Column(String)
    date = Column(DateTime, nullable = False)
    location = Column(String, nullable = False)
    max_participants = Column(Integer, default = 10)
    creator_id = Column(Integer, ForeignKey('Users.id'), nullable = False)
    created_at = Column(DateTime, default=datetime.now())
    status = Column(String, default = 'active')

    creator = relationship('Users', back_populates = 'created_events', foreign_keys = [creator_id])
    participants = relationship('Participants', back_populates = 'event', foreign_keys = 'Participants.event_id')
    reviews = relationship('Reviews', back_populates = 'event', foreign_keys = 'Reviews.event_id')
