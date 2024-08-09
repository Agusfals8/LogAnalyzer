from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URI = 'sqlite:///mydatabase.db'

engine = create_engine(DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)

def get_db_session():
    session = None
    try:
        session = Session()
    except SQLAlchemyError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return session

if __name__ == "__main__":
    session = get_db_session()
    if session:
        print("Session successfully created!")
        session.close()
    else:
        print("Failed to create a database session.")