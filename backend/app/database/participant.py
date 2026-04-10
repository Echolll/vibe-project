from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.database import Base
from datetime import datetime

class Participants(Base):
    __tablename__: str = 'Participants'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    event_id = Column(Integer, ForeignKey('events.id'), nullable = False)
    joined_at = Column(DateTime, default=datetime.now)
    status = Column(String, default = 'confirmed')

    user = relationship('Users', back_populates = 'participants', foreign_keys = [user_id])
    event = relationship('Events', back_populates = 'participants', foreign_keys = [event_id])