from sqlalchemy import Column, Integer, String
from database import Base


class Logop(Base):
    __tablename__ = 'logop_db'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    order = Column(Integer)

    def update(self, id=None, name=None, order=None):
        if name is not None:
            self.name = name
        if order is not None:
            self.order = order

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])