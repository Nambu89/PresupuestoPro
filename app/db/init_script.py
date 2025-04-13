import logging
from app.db.init_db import init_db
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

def main() -> None:
    logger.info("Inicializando base de datos con datos de ejemplo")
    init()
    logger.info("Base de datos inicializada")

if __name__ == "__main__":
    main()
