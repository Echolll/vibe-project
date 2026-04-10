from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from backend.app.database.database import Base
from datetime import datetime

class Reviews(Base):
    __tablename__: str = 'Reviews'

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('Users.id'), nullable = False)
    to_user_id = Column(Integer, ForeignKey('Users.id'), nullable = False)
    event_id = Column(Integer, ForeignKey('Events.id'), nullable = False)
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime, default = datetime.now())

    __table_args__ = (CheckConstraint('rating BETWEEN 1 AND 5'),)

    from_user = relationship('Users', back_populates = 'sent_reviews', foreign_keys = [from_user_id])
    to_user = relationship('Users', back_populates = 'received_reviews', foreign_keys = [to_user_id])
    event = relationship('Events', back_populates = 'reviews', foreign_keys = [event_id])