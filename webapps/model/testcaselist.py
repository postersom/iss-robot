from sqlalchemy import Column, Integer, String
from database import Base


class TestCaseList(Base):
    __tablename__ = 'testcaselist_db'
    id = Column(Integer, primary_key=True)
    test_case = Column(String(100))
    slot_no = Column(Integer)

    def update(self, id=None, test_case=None, slot_no=None):
        if test_case is not None:
            self.test_case = test_case

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])
