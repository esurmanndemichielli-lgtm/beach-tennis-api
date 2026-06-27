from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Match, PointEvent

router = APIRouter()

@router.get("/")
async def list_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).all()
    return matches

@router.get("/{match_id}")
async def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partida nao encontrada.")
    return match

@router.post("/")
async def create_match(team_a: str, team_b: str, db: Session = Depends(get_db)):
    match = Match(team_a=team_a, team_b=team_b, status="processando")
    db.add(match)
    db.commit()
    db.refresh(match)
    return match
