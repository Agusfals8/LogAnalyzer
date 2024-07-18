from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_models():
    return LogFile, Report