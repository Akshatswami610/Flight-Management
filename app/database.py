# DB session / engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Example: postgresql://<user>:<password>@<host>:<port>/<dbname>
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/flightdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
