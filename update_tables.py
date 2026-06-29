from database import engine
from models.db_models import Base

print("Atualizando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas atualizadas!")
