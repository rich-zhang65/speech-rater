from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from contextlib import contextmanager

engine = create_engine(
    settings.get_mysql_url(),
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.ENVIRONMENT == "development"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    """
    Context manager for database sessions.
    
    Usage:
        with get_db() as db:
            user = db.query(User).filter(User.email == "test@test.com").first()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

