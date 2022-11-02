from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Log(Base):
    __tablename__ = 'log_db'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(100))
    location = Column(String(1000))
    created = Column(DateTime())

    def update(self, id=None, file_name=None, location=None, created=None):
        if file_name is not None:
            self.file_name = file_name
        if location is not None:
            self.location = location
        if created is not None:
            self.created = created

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])
