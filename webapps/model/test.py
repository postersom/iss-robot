from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from flask import json
from collections import defaultdict
from sqlalchemy import inspect


class Test(Base):
    __tablename__ = 'test_db'
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(100))
    serial_number = Column(String(100))
    robot_name = Column(String(100))
    flag = Column(String(100))
    uut_log_dir = Column(String(1000))  # uut_log_dir
    operation_id = Column(String(1000))  # uut_log_dir
    test_mode = Column(String(1000))
    code_from = Column(String(1000))
    location = Column(String(1000))
    logop = Column(String(1000))
    product_name = Column(String(1000))
    created = Column(DateTime())
    statuses = relationship('Status', backref="test_db")

    def update(self, id=None, batch_id=None, serial_number=None, robot_name=None, flag=None, uut_log_dir=None, operation_id=None, test_mode=None, code_from=None, location=None, logop=None, product_name=None, statuses=None, created=None):
        if batch_id is not None:
            self.batch_id = batch_id
        if serial_number is not None:
            self.serial_number = serial_number
        if robot_name is not None:
            self.robot_name = robot_name
        if flag is not None:
            self.flag = flag
        if uut_log_dir is not None:
            self.uut_log_dir = uut_log_dir
        if location is not None:
            self.location = location
        if operation_id is not None:
            self.operation_id = operation_id
        if test_mode is not None:
            self.test_mode = test_mode
        if code_from is not None:
            self.code_from = code_from
        if logop is not None:
            self.logop = logop
        if product_name is not None:
            self.product_name = product_name
        if created is not None:
            self.created = created
        if statuses is not None:
            self.statuses = statuses

    def dump(self):
        return dict([(k, v) for k, v in self.__dict__.items() if k[0] != '_'])

    def dump2(self):
        insp = inspect(self)
        attr_state = insp.attrs.statuses
        print(attr_state.value)
        return "completed"
