from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Userinteraction(Base):
    __tablename__ = 'userinteraction_db'
    id = Column(Integer, primary_key=True)
    slot_no = Column(Integer)
    title = Column(String(1000))
    message = Column(String(10000))
    picture = Column(String(1000))
    html = Column(String(1000))
    timeout = Column(Integer)
    answer = Column(String(1000))
    operation_id = Column(String(1000))
    reason = Column(String(1000))
    created = Column(DateTime())

    def update(self, id=None, slot_no=None, title=None, message=None, picture=None, html=None, timeout=None, created=None, answer=None, operation_id=None, reason=None):
        if slot_no is not None:
            self.slot_no = slot_no
        if message is not None:
            self.message = message
        if picture is not None:
            self.picture = picture
        if html is not None:
            self.html = html
        if timeout is not None:
            self.created = created
        if created is not None:
            self.created = created
        if answer is not None:
            self.answer = answer
        if operation_id is not None:
            self.operation_id = operation_id
        if title is not None:
            self.title = title
        if reason is not None:
            self.reason = reason

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])
