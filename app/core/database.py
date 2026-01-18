from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 1. The Connection String
# Format: postgresql://user:password@postgresserver/db_name
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. The Engine
# Unlike SQLite, PostgreSQL handles its own threading, so we don't need 'check_same_thread'
engine = create_engine(DATABASE_URL)

# 3. The Session Factory
# This creates a 'Session' object every time a user interacts with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Base Class
# This is the "Parent" of all our tables
Base = declarative_base()