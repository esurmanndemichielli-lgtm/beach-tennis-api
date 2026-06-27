from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Player(BaseModel):
    id: int
    name: str
    avatar: str

class MatchCreate(BaseModel):
    team_a: List[str]
    team_b: List[str]
    video_url: Optional[str] = None

class PointEvent(BaseModel):
    number: int
    winner_team: str
    type: str
    duration_seconds: float
    score: str

class MatchStats(BaseModel):
    player_name: str
    serves: int
    serve_errors: int
    aces: int
    winners: int
    unforced_errors: int
    return_errors: int
    serve_accuracy: float

class Match(BaseModel):
    id: int
    team_a: List[str]
    team_b: List[str]
    date: datetime
    result: Optional[str] = None
    status: str
    stats: Optional[List[MatchStats]] = None
    points: Optional[List[PointEvent]] = None
    duration_minutes: Optional[int] = None
