from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base


class Status(Base):
    __tablename__ = 'status_db'
    id = Column(Integer, primary_key=True)
    status = Column(String(100))
    message = Column(String(1000))
    created = Column(DateTime())
    slot_no = Column(Integer)

    test_id = Column(Integer, ForeignKey('test_db.id'), nullable=False)

    def update(self, id=None, status=None, slot_no=None, message=None, test_id=None, created=None):
        if status is not None:
            self.status = status
        if message is not None:
            self.message = message
        if created is not None:
            self.created = created
        if test_id is not None:
            self.test_id = test_id

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])
