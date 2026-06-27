from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Player

router = APIRouter()

@router.get("/")
async def list_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    return players

@router.get("/{player_id}")
async def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Jogador nao encontrado.")
    return player
