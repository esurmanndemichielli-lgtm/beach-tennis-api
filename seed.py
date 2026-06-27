from database import SessionLocal
from models.db_models import Player, Match, PointEvent

db = SessionLocal()

players = [
    Player(name="Joao Silva", partner="Pedro Alves", matches=8, wins=6, aces=34, winners=112, errors=58, serve_accuracy=87.0, avg_rally_seconds=4.1),
    Player(name="Pedro Alves", partner="Joao Silva", matches=8, wins=6, aces=21, winners=98, errors=71, serve_accuracy=82.0, avg_rally_seconds=4.3),
    Player(name="Lucas Mendes", partner="Rafael Costa", matches=6, wins=3, aces=18, winners=76, errors=89, serve_accuracy=74.0, avg_rally_seconds=5.1),
    Player(name="Rafael Costa", partner="Lucas Mendes", matches=6, wins=3, aces=12, winners=64, errors=95, serve_accuracy=71.0, avg_rally_seconds=5.4),
    Player(name="Ana Beatriz", partner="Carla Souza", matches=5, wins=4, aces=28, winners=91, errors=62, serve_accuracy=85.0, avg_rally_seconds=3.9),
    Player(name="Carla Souza", partner="Ana Beatriz", matches=5, wins=4, aces=19, winners=83, errors=70, serve_accuracy=79.0, avg_rally_seconds=4.2),
]

match = Match(
    team_a="Joao Silva e Pedro Alves",
    team_b="Lucas Mendes e Rafael Costa",
    result="6-3, 6-4",
    status="concluido",
    duration_minutes=48,
)

db.add_all(players)
db.add(match)
db.commit()
db.refresh(match)

points = [
    PointEvent(match_id=match.id, number=1, winner_team="A", type="Ace", duration_seconds=2.0, score="0-15"),
    PointEvent(match_id=match.id, number=2, winner_team="B", type="Erro nao forcado", duration_seconds=6.0, score="15-15"),
    PointEvent(match_id=match.id, number=3, winner_team="A", type="Winner", duration_seconds=4.0, score="15-30"),
    PointEvent(match_id=match.id, number=4, winner_team="A", type="Erro devolucao", duration_seconds=1.0, score="15-40"),
    PointEvent(match_id=match.id, number=5, winner_team="A", type="Ace", duration_seconds=1.0, score="Game A"),
]

db.add_all(points)
db.commit()
db.close()

print("Dados inseridos com sucesso!")
