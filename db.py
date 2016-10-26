from sqlalchemy import Column, Integer, Boolean, DateTime, Date, Time, Float, String
from sqlalchemy.dialects.sqlite import BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, INTEGER, REAL, NUMERIC, SMALLINT, TIME, TIMESTAMP, VARCHAR

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class RECORD(Base):
    __tablename__ = 'record'

    id = Column(Integer, autoincrement=True, primary_key=True)
    speed = Column(Float, nullable=True)
    dist_from_last = Column(Float, nullable=True)
    device_state = Column(String(3), nullable=True)
    lat = Column(NUMERIC, nullable=True)
    lon = Column(NUMERIC, nullable=True)
    time_from_last = Column(Integer, nullable=True)
    time_st = Column(NUMERIC, nullable=True)
    time = Column(DateTime, nullable=True)
