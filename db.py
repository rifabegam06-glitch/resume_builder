import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Replace the connection string with your PostgreSQL credentialssql:
#Format: postgresql://username:password@host:port/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/resume_db"
)

#Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

#Create a SessionLocal class  for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)        

#Create a Base class for our models to inherit
Base = declarative_base()


