from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database file ka rasta
DATABASE_URL = "sqlite:///./tasks.db"

# 2. Connection engine banana
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Database session banane wala tool
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tables banane ke liye Base class
Base = declarative_base()

# 5. Dependency: Har request par naya connection lene ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()