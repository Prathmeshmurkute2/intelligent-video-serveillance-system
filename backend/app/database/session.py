from sqlalchemy.orm import sessionmaker

from app.database.database import engine

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)