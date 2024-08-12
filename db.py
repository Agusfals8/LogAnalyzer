from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
import sys

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
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

def log_demo_messages():
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

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

    log_demo_messages()