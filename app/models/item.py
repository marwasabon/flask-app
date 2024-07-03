from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(Enum('Lost', 'Found', name='status_types'), nullable=False)
    date_reported = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='items')
    claims = relationship('Claim', back_populates='item')
    matches = relationship('Match', back_populates='item')
