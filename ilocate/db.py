import functools
import logging

from sqlalchemy import Column, Integer, DateTime, Date, Time, Float, String, create_engine
from sqlalchemy.dialects.sqlite import NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

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

    def session_scope(decorated_function):
        """Decorate the DB functions with this to automatically get a session."""
        @functools.wraps(decorated_function)
        def wrapper(*args, **kwargs):
            self = args[0]
            session = kwargs['session'] if 'session' in kwargs else kwargs.setdefault('session', self.Session())
            try:
                db_result = decorated_function(*args, **kwargs)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

            return db_result

        return wrapper

    @classmethod
    def create_database(cls):
        log.info("Initialising DB")
        metadata.create_all(db_engine, checkfirst=True)

    @session_scope
    def add_record(self, record, session=None):
        if hasattr(record, '__iter__'):
            session.add_all(record)
        else:
            session.add(record)

    @session_scope
    def commit(self, session=None):
        session.commit()

    @session_scope
    def get_count(self, session=None):
        return session.query(RECORD).count()

    @session_scope
    def get_attribute(self, name, session=None):
        return session.query(ATTR.value).filter(ATTR.name == name).first()

    @session_scope
    def set_attribute(self, name, value, session=None):
        attribute = self.get_attribute(name)
        if not attribute:
            attribute = ATTR(name=name, value=value)
        return session.add(attribute)

    @property
    @session_scope
    def is_first_run(self, session=None):
        return bool(session.query(ATTR).filter(ATTR.name == "first_run").first())

    @property
    @session_scope
    def latest_record_datetime(self, session=None):
        result = session.query(RECORD.dt).order_by(RECORD.dt.desc()).first()
        return result[0] if result else result
