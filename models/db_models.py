from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    partner = Column(String)
    matches = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    aces = Column(Integer, default=0)
    winners = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    serve_accuracy = Column(Float, default=0.0)
    avg_rally_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    team_a = Column(String, nullable=False)
    team_b = Column(String, nullable=False)
    result = Column(String)
    status = Column(String, default="processando")
    duration_minutes = Column(Integer)
    video_path = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    points = relationship("PointEvent", back_populates="match")

class PointEvent(Base):
    __tablename__ = "point_events"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    number = Column(Integer)
    winner_team = Column(String)
    type = Column(String)
    duration_seconds = Column(Float)
    score = Column(String)
    match = relationship("Match", back_populates="points")

class VideoJob(Base):
    __tablename__ = "video_jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    status = Column(String, default="queued")
    progress = Column(Float, default=0.0)
    current_step = Column(String, default="Na fila")
    error = Column(Text)
    stats_json = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
