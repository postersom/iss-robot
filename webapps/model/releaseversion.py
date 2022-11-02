from sqlalchemy import Column, Integer, String
from database import Base


class ReleaseVersion(Base):
    __tablename__ = 'releaseversion_db'
    id = Column(Integer, primary_key=True)
    location = Column(String(100))
    value = Column(String(100))

    def update(self, id=None, location=None, value=None):
        if location is not None:
            self.location = location
        if value is not None:
            self.value = value

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])