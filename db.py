import functools
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Boolean, DateTime, Date, Time, Float, String, create_engine
from sqlalchemy.dialects.sqlite import BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, REAL, NUMERIC, SMALLINT, TIME, TIMESTAMP, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

db_engine = create_engine('sqlite+pysqlite:///records.sqlite')

class RECORD(Base):
    __tablename__ = 'record'

    # id = Column(Integer, autoincrement=True, primary_key=True)
    timestamp = Column(NUMERIC, primary_key=True, unique=True)
    speed = Column(Float, nullable=True)  # km/h?
    lat = Column(NUMERIC, nullable=True)
    lon = Column(NUMERIC, nullable=True)
    time_from_last = Column(Integer, nullable=True)  # seconds
    dist_from_last = Column(Float, nullable=True)  # kilometers
    date = Column(Date, nullable=True)
    time = Column(Time, nullable=True)
    dt = Column(DateTime, nullable=True)
    device_state = Column(String(3), nullable=True)


class ATTR(Base):
    __tablename__ = 'attr'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)


class Persistence(object):

    def __init__(self):
        self.Session = sessionmaker(bind=db_engine)
        self.create_database()

    # def session_scope(self):
    #     """Provide a transactional scope around a series of operations."""
    #     session = self.Session()
    #     try:
    #         yield session
    #         session.commit()
    #     except:
    #         session.rollback()
    #         raise
    #     finally:
    #         session.close()

    def session_scope(func):
        """Decorator which wraps the decorated function in a transactional session. If the
           function completes successfully, the transaction is committed. If not, the transaction
           is rolled back."""

        # @functools.wraps(func)
        def outer_wrapper(*args, **kwargs):

            session = args[0].Session()
            try:
                yield func
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return outer_wrapper

    @classmethod
    def create_database(cls):
        metadata.create_all(db_engine, checkfirst=True)

    def add_record(self, record, session):
        session = self.Session()
        if hasattr(record, '__iter__'):
            session.add_all(record)
        else:
            session.add(record)
        session.commit()

    @session_scope
    def get_count(self, session=None):
        return session.filter(RECORD).count()

    def get_attribute(self, name, session):
        return session.query(ATTR.value).filter(ATTR.name == name).first()

    @property
    @session_scope
    def is_first_run(self, session):
        return session
