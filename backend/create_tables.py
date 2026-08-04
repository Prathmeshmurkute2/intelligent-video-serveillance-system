from app.database.base import Base
from app.database.database import engine
from app.core.logger import logger

import app.database.models

Base.metadata.create_all(bind=engine)

logger.info("Tables created successfully!")