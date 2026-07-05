from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 1. Configure the local SQLite database storage engine
DATABASE_URL = "sqlite:///./reviews.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite multi-threading within FastAPI
)

# 2. Establish session factories for incoming API requests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Define the Code Review Relational Table Model
class ReviewRecord(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Saves execution runs automatically
    vulnerabilities = Column(Text, nullable=False)  # Stores serialized JSON arrays from the security task
    bugs = Column(Text, nullable=False)            # Stores serialized JSON arrays from the QA task
    quality_score = Column(Integer, nullable=False) # Stores the final calibrated health score percentage

# 4. Global initialization function to generate tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)

# Automatically trigger table generation on application boot/import
init_db()