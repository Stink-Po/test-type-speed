import sqlalchemy
from sqlalchemy import Integer, Column, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data_base.sqlite', echo=True)
base = sqlalchemy.orm.declarative_base()


# sqlite database using sqlalchemy i just add some data to database and delete the commands
class Database(base):
    __tablename__ = "typing_sample"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    record = Column(Integer)

    def __init__(self, id, text, record):
        self.id = id
        self.text = text
        self.record = record


base.metadata.create_all(engine)
