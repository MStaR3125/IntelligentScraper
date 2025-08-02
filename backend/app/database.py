from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scraper.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScrapingJob(Base):
    __tablename__ = "scraping_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(500), index=True)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    max_results = Column(Integer, default=15)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    results_count = Column(Integer, default=0)
    results_file = Column(String(200), nullable=True)
    error_message = Column(Text, nullable=True)
    
    scraped_items = relationship("ScrapedItem", back_populates="job")

class ScrapedItem(Base):
    __tablename__ = "scraped_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    description = Column(Text)
    url = Column(String(1000))
    price = Column(String(100))
    rating = Column(String(50))
    date = Column(String(100))
    additional_data = Column(Text)  # JSON string
    
    job_id = Column(Integer, ForeignKey("scraping_jobs.id"))
    job = relationship("ScrapingJob", back_populates="scraped_items")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)