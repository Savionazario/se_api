from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship
import uuid

from app.database import Base

class Gate(Base):
    __tablename__ = "gates"

    gate_id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    name = Column(String)
    current_state = Column(Boolean)
    gate_state_history = relationship("GateStateHistory", back_populates="owner")

class GateStateHistory(Base):
    __tablename__ = 'gate_state_history'

    id = Column(Integer, primary_key=True, index=True)
    gate_id = Column(String, ForeignKey('gates.gate_id'))
    gate_state = Column(Boolean)
    time = Column(DateTime)
    owner = relationship("Gate", back_populates="gate_state_history")