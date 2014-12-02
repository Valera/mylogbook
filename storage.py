import datetime
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db.sqlite', echo=True)


Base = declarative_base()


class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Context(Base):
    __tablename__ = 'contexts'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    name = Column(String(200))
    description = Column(String(2000))
    start_date = Column(Date)
    due_date = Column(Date)
    added_date = Column(Date)
    finished_date = Column(Date)
    active = Column(Boolean)
    planned_work_units = Column(Integer)
    accomplished_work_units = Column(Integer)
    folder = Column(Integer, ForeignKey('folders.id'))
    context = Column(Integer, ForeignKey('contexts.id'))

    def __init__(self, name, description, start_date=None, due_date=None,
                 active=True, planned_work_units=0, accomplished_work_units=0,
                 folder=None, context=None):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.added_date = datetime.date.today()
        self.finished_date = None
        self.active = active
        self.planned_work_units = planned_work_units
        self.accomplished_work_units = accomplished_work_units
        self.folder = folder
        self.context = context


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey('projects.id'))
    name = Column(String)
    description = Column(String(2000))
    start_date = Column(Date)
    due_date = Column(Date)
    finished_date = Column(Date)
    added_date = Column(Date)
    active = Column(Boolean)
    planned_work_units = Column(Integer)
    accomplished_work_units = Column(Integer)
    repeat = Column(Boolean)
    postpone_mode = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    email = Column(String(200), unique=True)
    salt = Column(String(80))  # TODO: use salt
    password = Column(String(80))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UserSession(Base):
    __tablename__ = "usersessions"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey("users.id"))
    token = Column(String(40))

    def __init__(self, user):
        import random

        self.user = user.id
        self.token = str(random.randrange(0, 10 ** 40)).zfill(40)


class WorkUnit(Base):
    __tablename__ = "workunits"
    id = Column(Integer, primary_key=True)
    project = Column(Integer, ForeignKey("projects.id"))
    date = Column(Date)
    unit_type = Column(Integer)
    info = Column(String(200))


class Contact(Base):
    """
    Now Contact class is mostly for birthday reminders.
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    birthday = Column(Date)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def main():
    with session_scope() as session:
        pr = Project("hello", "first project")
        session.add(pr)
        session.commit()
        print(session.query(User).all())
        # pr = Project("hello", 1)
        # session.add(pr)
    with session_scope() as session:
        print(session.query(User).all())


if __name__ == "__main__":
    main()
