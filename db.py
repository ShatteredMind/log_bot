from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from settings import DATABASE_URI


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.expire_on_commit = True
        session.expunge_all()
        session.close()


engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
