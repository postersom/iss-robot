from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class Setting(Base):
    __tablename__ = 'setting_db'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    title = Column(String(100))
    value = Column(String(100))
    categories = Column(String(100))
    order = Column(Integer)
    created = Column(DateTime())

    def update(self, id=None, name=None, value=None, title=None, categories=None, order=None, created=None):
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value
        if title is not None:
            self.title = title
        if categories is not None:
            self.categories = categories
        if order is not None:
            self.order = order
        if created is not None:
            self.created = created

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])
