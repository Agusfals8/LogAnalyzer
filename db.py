from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URI = 'sqlite:///mydatabase.db'

engine = create_engine(DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)

def get_db_session():
    session = None
    try:
        session = Session()
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
    
    return session

if __name__ == "__main__":
    session = get_db_session()
    if session:
        logger.info("Session successfully created!")
        try:
            session.close()
        except SQLAlchemyError as e:
            logger.error(f"Failed to close the session properly: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"An unexpected error occurred during session closure: {e}", exc_info=True)
    else:
        logger.info("Failed to create a database session.")