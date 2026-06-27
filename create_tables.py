from database import engine, Base
from models.db_models import Player, Match, PointEvent, VideoJob

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
