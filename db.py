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


class Persistence(object):

    def __init__(self):
        self.Session = sessionmaker(bind=db_engine)
        self.create_database()

    @classmethod
    def create_database(cls):
        metadata.create_all(db_engine, checkfirst=True)

    def add_record(self, record):
        session = self.Session()
        if hasattr(record, '__iter__'):
            session.add_all(record)
        else:
            session.add(record)
        session.commit()
