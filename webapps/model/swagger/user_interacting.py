from __future__ import absolute_import
from typing import List, Dict
from model.swagger.base_model_ import Model
from model.swagger import util
from service.logging import Logging


class UserInteracting(Model):

    def __init__(self):
        self._return_data = {
            "data": None,
            "error": False
        }
        self._property_create = {
            "slot_location_no": None,
            "message": None,
            "picture": None,
            "html": None,
            "timeout": None
        }
        self._property_user = {
            "slot_location_no": None
        }
        self._log_header = "UserInteraction-{}"
        self._log = Logging()

    @property
    def return_data(self) -> dict:
        return self._return_data

    @property
    def property_create(self) -> dict:
        return self._property_create

    @property
    def property_user(self) -> dict:
        return self._property_user

    @property
    def log(self) -> Logging:
        return self._log

    @property
    def log_header(self) -> str:
        return self._log_header

    @property_create.setter
    def property_create(self, prop):
        self._property_create = prop

    @property_user.setter
    def property_user(self, prop):
        self._property_user = prop

    @log_header.setter
    def log_header(self, header):
        self._log_header = header

    def create_user_interaction(self):
        self.log_header = self.log_header.format("create_user_interaction")
        self.log.info(self.log_header, "Create User Interaction")

    def user_interaction(self):
        try:
            self.log_header = self.log_header.format("user_interaction")
            self.log.info("user_interaction", "User Interaction")
        except Exception as e:
            print(e)
