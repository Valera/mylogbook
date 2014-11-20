from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime


engine = create_engine('sqlite:///:memory:', echo=True)


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


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def main():
    session = Session()
    pr = Project("hello", "first project")
    session.add(pr)
    Project.sel
    session.commit()


if __name__ == "__main__":
    main()
