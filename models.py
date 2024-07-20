from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError  # Import for handling SQL Alchemy exceptions
from datetime import datetime
import os

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///log_analysis.db')

engine = create_engine(DATABASE_URI)
Base = declarative_base()

class LogFile(Base):
    __tablename__ = 'log_files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(100))

    reports = relationship('Report', back_populates='log_file')

    def __repr__(self):
        return f"<LogFile(filename='{self.filename}', upload_date='{self.upload_date}', status='{self.status}')>"

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey('log_files.id'))
    report_data = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)

    log_file = relationship('LogFile', back_populates='reports')

    def __repr__(self):
        return f"<Report(report_data='{self.report_data}', generated_at='{self.generated_at}')>"

def add_log_file(session, filename, status):
    try:
        new_log_file = LogFile(filename=filename, status=status)
        session.add(new_log_file)
        session.commit()
        return new_log_file
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding log file: {e}")
        return None

def add_report(session, log_id, report_data):
    try:
        new_report = Report(log_id=log_id, report_data=report_data)
        session.add(new_report)
        session.commit()
        return new_report
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error adding report: {e}")
        return None

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_models():
    return LogFile, Report

if __name__ == "__main__":
    log_file = add_log_file(session, 'example.log', 'Uploaded')
    if log_file is not None:
        add_report(session, log_file.id, 'Report data here.')
