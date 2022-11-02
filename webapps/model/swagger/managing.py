from __future__ import absolute_import
from datetime import datetime
from typing import List, Dict
from model.swagger.base_model_ import Model
from model.swagger import util
from service.logging import Logging
import sys
import time

class Managing(Model):

    def __init__(self):
        self._sn_sync = {}
        self._all_sn_scaning = {}
        self._print_log = Logging()
        self._return_data = {
            "data": None,
            "error": True,
            "setup": False
        }
        self._return_sync_point = {
            "data": None,
            "error": True,
            "setup": False
        }
        self._return_queue = {
            "data": None,
            "error": True,
            "setup": False
        }
        self._log_header = None
        self._hardware_working_with = {}
        self._queue_stack = {}

    @property
    def return_data(self) -> dict:
        return self._return_data
    @property
    def return_sync_point(self) -> dict:
        return self._return_sync_point
    @property
    def return_queue(self) -> dict:
        return self._return_queue
    @property
    def sn_sync(self) -> dict:
        return self._sn_sync
    @property
    def all_sn_scaning(self) -> dict:
        return self._all_sn_scaning
    @property
    def print_log(self) -> Logging:
        return self._print_log

    @property
    def log_header(self) -> str:
        return self._log_header

    @log_header.setter
    def log_header(self, header):
        self._log_header = header

    def check_sync_point(self, request_body) -> bool:
        # SN_SYNC and CSN_SN are global variables that passed by test_controller
        self.log_header = "{}-{}".format("Managing", "check_sync_point")
        tmp_log_header = "{}-{}".format("Managing", "check_sync_point")
        tmp_sn = request_body.get("serial_number").strip()
        tmp_chassis_sn = request_body.get("slot_location").split("_", 1)[0]
        tmp_batch_id = request_body.get("batch_id")
        tmp_sn_count = self.all_sn_scaning.get(tmp_batch_id).get("sn_count")

        message = ""
        tmp = {
            "sn": [],
            "checked_time": None,
            "timeout": None,
            "data": None,
            "error": None,
            "setup": None
        }
        if not tmp_sn or not tmp_batch_id:
            tmp_batch_id = None
            tmp_sn = None
            message = "Cannot sync point of testing because serial-number or slot-location is empty"
            self.print_log.error(self.log_header, message)
            return

        if not self.sn_sync.get(tmp_batch_id):
            self.sn_sync[tmp_batch_id] = tmp

        self.sn_sync[tmp_batch_id]["error"] = True
        try:
            all_sn = self.all_sn_scaning.get(tmp_batch_id).get("sns") if self.all_sn_scaning.get(tmp_batch_id).get("sns") else []
            sync_sn = self.sn_sync[tmp_batch_id].get("sn")
            # Not found sn on this chassis_sn
            if not all_sn or len(all_sn) == 0:
                message = "Cannot get this serial-number assume this chassis number({}) is not starting test".format(
                    tmp_chassis_sn)
            elif not tmp_sn in all_sn:
                # sn sync-point is not found on sn scan-in 
                message = "This serial-number({}) is not start testing please check your serial-number".format(
                    tmp_sn)
            elif tmp_sn in all_sn and tmp_sn in sync_sn and not tmp_sn_count == len(sync_sn):
                # Waiting for other sn
                message = "This serial-number has synced-point will wait other serial-number for check point"
            elif len(sync_sn) == 0:
                # This sn is a first of sync-point
                message = "SN: {} sync point on Batch: {} at the first time".format(
                    tmp_sn, tmp_batch_id)
                tmp_first = {
                    'checked_time': datetime.now(),
                    'timeout': int(request_body.get("timeout")),
                    'setup': False
                }
                self.sn_sync[tmp_batch_id]['sn'].append(tmp_sn)
                self.sn_sync.get(tmp_batch_id).update(tmp_first)
            elif tmp_sn in all_sn and not tmp_sn in sync_sn:
                # New sn sync-point
                self.sn_sync[tmp_batch_id].get("sn").append(tmp_sn)
                message = "SN: {} sync point on Batch: {} and waiting another serial number".format(
                    tmp_sn, tmp_batch_id)
                if tmp_sn_count == len(sync_sn):
                    message = "Sync-point maybe success please wait serial-number on next round"
            elif not len(sync_sn) == 0 and tmp_sn_count == len(sync_sn) and not tmp_sn in sync_sn:
                # SN sync-point have number of sn more than sn scan-in 
                message = "Now Sync-point has serial-number: {}\n And All scan-in with chassis({}) is: {} that occure something\
                     wrong with serial-number({})".format(sync_sn, tmp_chassis_sn, all_sn, tmp_sn)
            elif tmp_sn_count == len(sync_sn):
                # Number of sn sync-point is equal sn scan-in
                check_sync = True
                # Check sn in sync-point must be like sn scan-in
                for sn in sync_sn:
                    if not sn in all_sn:
                        check_sync = False
                        message = "Count of serial number that entry to sync-point\
                                 is correct but some these serial number is not scan-in"
                        self.print_log.error(self.log_header, message)
                        self.sn_sync[tmp_batch_id]["data"] = message
                        return

                if check_sync:
                    # Robot framework need to setup something before run next step
                    if request_body.get("setup") and not self.sn_sync.get(tmp_batch_id).get("setup"): 
                        self.setup_after_sync_point(tmp_batch_id)
                    else:    
                        # Sync-point have complete
                        self.sn_sync[tmp_batch_id]["error"] = False
                        message = "Sync-point is complete of chassis: {}".format(tmp_batch_id)
            else:
                # This SN and chassis-sn are not matched any condition
                message = "This serial-number({}) and chassis-number({}) are not match any case"
        except Exception as E:
            message = "Error on preparing to check serial number or add this serial number for sync-point: {}\nOn line: {}".format(E, sys.exc_info()[-1].tb_lineno)
        self.print_log.error(self.log_header, message)
        #self.return_sync_point.update({"data": message})
        self.sn_sync[tmp_batch_id]["data"] = message
        self.print_log.info(
            "Managing.Model", "SN scan-in and SN sync-point:\n{} {}".format(self.all_sn_scaning, self.sn_sync))

        # De-allocate variable
        tmp_sn = None
        tmp_chassis_sn = None
        tmp_batch_id = None
        tmp_sn_count = None
        sync_sn = None
        all_sn = None
        message = None
        check_sync = None 
        return

    def remove_sn_from_syncpoint(self, request_body) -> bool:
        tmp_batch_id = request_body.get("batch_id")
        tmp_sn = request_body.get("serial_number")
        self.log_header = "Mananing-remove_sn_from_syncpoint"

        if not tmp_batch_id or not tmp_sn:
            tmp_batch_id = None
            tmp_sn = None
            self.print_log.error(
                self.log_header, "Cannot get slot-location or serial-number for remove serial number out from sync-poing stack")
            self.sn_sync.get(tmp_batch_id).update({"data": "Cannot get slot-location or serial-number for remove serial number out from sync-poing stack", "error": True})
            return

        tmp_sn_count = self.all_sn_scaning.get(tmp_batch_id).get("sn_count")
        tmp_csn_sn = self.all_sn_scaning.get(tmp_batch_id).get("sns")
        if not tmp_csn_sn:
            self.print_log.error(
                self.log_header, "Cannot get chassis from testing stack please check your chassis")
            self.sn_sync.get(tmp_batch_id).update({"data": "Cannot get chassis from testing stack please check your chassis", "error": True})
            return
        if not tmp_sn in tmp_csn_sn:
            self.print_log.error(
                self.log_header, "Cannot get serial-number({}) from batch id ({}) please check your chassis".format(tmp_sn, tmp_batch_id))
            self.sn_sync.get(tmp_batch_id).update({"data": "Cannot get serial-number({}) from batch id ({}) please check your chassis".format(tmp_sn, tmp_batch_id), "error": True})
            return

        try:
            self.all_sn_scaning.get(tmp_batch_id).get("sns").remove(tmp_sn)
            tmp_sn_count -= 1
            self.all_sn_scaning.get(tmp_batch_id)["sn_count"] = tmp_sn_count
            message = "Remove serial-number on the sync-point is complete"
            self.sn_sync.get(tmp_batch_id).update({"data": message, "error": False})
        except Exception as e:
            self.sn_sync.get(tmp_batch_id).update({"error": True, "data": "Error on remove serial-number cannot found {} or this serial-number never scan-in".format(tmp_sn)})
        
        if tmp_sn in self.sn_sync.get(tmp_batch_id).get("sn"):
            self.sn_sync.get(tmp_batch_id).remove(tmp_sn)
        
        return
        
    def setup_after_sync_point(self,tmp_batch_id):
        try:
            # with open("", "r") as content:
                # read file and assign to local variable
            # setup testing with value from local variable 
            tmp_message = "Setup after all serial-number are synced complete"
            tmp_setup = True
        except Exception as e: 
            tmp_message = "Cannot setup after all serial-number are synced: {}".format(
                e)
            tmp_setup = False
        tmp = { 
            "error": tmp_message,
            "setup": tmp_setup
        }

        # De-allocate variable 
        tmp_message = None
        tmp_setup = None

        self.sn_sync.get(tmp_batch_id).update(tmp)

    def remove_csn_after_complete(self, request_body):
        tmp_batch_id = request_body.get("batch_id")

        if not self.sn_sync.get(tmp_batch_id):
            return False

        if request_body.get("setup"):
            self.print_log.info(self.log_header, "Detect setup")
            if self.sn_sync.get(tmp_batch_id).get("setup"):
                self.print_log.info(self.log_header, "Setup is True")
                return True
                
            # if request_body.get("serial_number") == self.sn_sync.get(tmp_batch_id).get("sn")[0]:
            #     self.print_log.info(self.log_header, "First Sync")
            #     if self.sn_sync.get(tmp_batch_id).get("setup") is None:
            #         self.print_log.info(self.log_header, "First time")
            #         self.sn_sync.get(tmp_batch_id).update({'data': self.sn_sync.get("sn")[0], 'setup': False})
            #     elif self.sn_sync.get(tmp_batch_id).get("setup") == False:
            #         self.print_log.info(self.log_header, "Second time")
            #         self.sn_sync.get(tmp_batch_id).update({'error': None, 'data': 'sync-point is complete', 'setup': True})
            # else:
            #     self.print_log.info(self.log_header, "Not First sync")
            #     self.sn_sync.get(tmp_batch_id).update({'data': 'Wait slot {} setup enveronment'.format(self.sn_sync.get(tmp_batch_id).get("sn")[0])})

        #     return True

        if self.sn_sync.get(tmp_batch_id).get("error") is not True:
            try:
                tmp_sn = request_body.get("serial_number")
                if tmp_sn in self.sn_sync.get(tmp_batch_id).get("sn"):
                    self.sn_sync.get(tmp_batch_id).get("sn").remove(tmp_sn)  

                if len(self.sn_sync.get(tmp_batch_id).get("sn")) == 0:
                    self.sn_sync.pop(tmp_batch_id)

                return True
            except Exception as e:
                self.print_log.error(self.log_header, e)
        return False

    def check_timeout_sync_point(self, request_body):
        tmp_batch_id = request_body.get("batch_id")
        if not self.sn_sync.get(tmp_batch_id):
            return
        tmp_checked_time = self.sn_sync.get(tmp_batch_id).get("checked_time")
        tmp_timeout = self.sn_sync.get(tmp_batch_id).get("timeout")
        tmp_sn_sync = self.sn_sync.get(tmp_batch_id).get("sn").copy()
        self.log_header = "Managing-check_timeout_sync_point"
        tmp_datetime_now = datetime.now()
        tmp_sn_count = self.all_sn_scaning.get(tmp_batch_id).get("sn_count")
        try:
            if len(tmp_sn_sync) < tmp_sn_count: 
                if tmp_checked_time is not None:
                    if (tmp_datetime_now - tmp_checked_time).seconds >= tmp_timeout:
                        self.print_log.info(self.log_header, "Found sn timeout before entry to sync-point")
                        tmp_arr_sn = list(set(self.all_sn_scaning.get(tmp_batch_id).get("sns")) - set(tmp_sn_sync))
                        for tmp_sn in tmp_arr_sn:
                            self.all_sn_scaning.get(tmp_batch_id).update({"sn_count": tmp_sn_count - 1})
                            self.all_sn_scaning.get(tmp_batch_id).get("sns").remove(tmp_sn)
                            tmp_sn_count = self.all_sn_scaning.get(tmp_batch_id).get("sn_count")
                            self.print_log.info(self.log_header, "{} removed".format(tmp_sn))
        except Exception as e:
            self.print_log.error(self.log_header, "Error on check timout sync-pont: {}".format(e))
            raise
        return

    def remove_sn_sync_not_allow_timeout(self, request_body):
        
        tmp_batch_id = request_body.get("batch_id")
        if not self.sn_sync.get(tmp_batch_id):
            return False

        tmp_checked_time = self.sn_sync.get(tmp_batch_id).get("checked_time")
        tmp_timeout = self.sn_sync.get(tmp_batch_id).get("timeout")
        tmp_datetime_now = datetime.now()

        if (tmp_datetime_now - tmp_checked_time).seconds >= tmp_timeout:
            self.all_sn_scaning.pop(tmp_batch_id)
            self.sn_sync.pop(tmp_batch_id)
            return True
        return False
    
    def queue_access_hardware(self, queue):
        tmp_sn = queue.get("serial_number")
        tmp_remove_all = self._queue_stack.copy()
        tmp_hardware_name = queue.get("hardware_name")
        message = ""

        if not tmp_hardware_name:
            self.return_queue["data"] = "Not found hardware name please try again"
            return
        
        print(self.log_header, self._hardware_working_with)
        # Check timeout queue
        if self._hardware_working_with and self._hardware_working_with.get(tmp_hardware_name):
            if self._hardware_working_with.get(tmp_hardware_name).get("entry_time") and self._hardware_working_with.get(tmp_hardware_name).get("timeout"):
                tmp_entry_time = self._hardware_working_with.get(tmp_hardware_name).get("entry_time")
                tmp_timeout = self._hardware_working_with.get(tmp_hardware_name).get("timeout")
                if (datetime.now() - tmp_entry_time).seconds > tmp_timeout:
                    self._hardware_working_with.pop(tmp_hardware_name)
        
        # Request from robot is release queue after access hardware complete
        if queue.get("type") == "release":
            if not self._hardware_working_with.get(tmp_hardware_name) and not self._queue_stack.get(tmp_hardware_name):
                self.return_queue["data"] = "Not found {} is accessed from any test".format(tmp_hardware_name)
                return

            tmp_hw_working = self._hardware_working_with.get(tmp_hardware_name) if self._hardware_working_with.get(tmp_hardware_name) else {}
            if tmp_hw_working:
                if tmp_sn == tmp_hw_working.get("sn"):
                    self.return_queue["data"] = "Release {} out of using hardware({}) can access\
                         from other serial number".format(tmp_sn, tmp_hardware_name)
                    self.return_queue["error"] = False
                    self._hardware_working_with.pop(tmp_hardware_name)
                else:
                    message = "Cannot release because serial number accessing hardware is not serial number on request"
                    self.return_queue["data"] = message
                self.print_log.info(self.log_header, message)
                return
            
            tmp_queue_stack = self._queue_stack.get(tmp_hardware_name) if self._queue_stack.get(tmp_hardware_name) else []
            if not tmp_queue_stack:
                message = "Queue is empty cannot release now."
            elif tmp_sn in tmp_queue_stack:
                self._queue_stack.remove(tmp_sn)
                message = "Remove serial number {} out of queue on {}".format(tmp_sn, tmp_hardware_name)
                self.return_queue["error"] = False
            elif tmp_sn not in tmp_queue_stack:
                message = "Not found this serial({}) number in queue of {}".format(tmp_sn, tmp_hardware_name)

            self.return_queue['data'] = message
            self.print_log.error(self.log_header, message)
            return
        # Reuqest type is not both request and release
        elif not queue.get("type") == "request":
            message = "This action are not both request and release({})".format(queue.get("type"))
            self.return_queue["data"] = message
            self.print_log.info(self.log_header, message)
            return

        tmp_queue_stack = self._queue_stack.get(tmp_hardware_name) if self._queue_stack.get(tmp_hardware_name) else []
        tmp_hw_working = self._hardware_working_with.get(tmp_hardware_name).get("sn") if self._hardware_working_with.get(tmp_hardware_name) else ""
        if tmp_hw_working:# Hardware is busy
            if not tmp_sn in tmp_queue_stack and not tmp_sn == tmp_hw_working:
                message = "Hardware is working with other unit now this serial number is added to queue please try again"
                if not self._queue_stack.get(tmp_hardware_name):
                    self._queue_stack[tmp_hardware_name] = [tmp_sn]
                else:
                    self._queue_stack.get(tmp_hardware_name).append(tmp_sn)
            elif tmp_sn in tmp_queue_stack:
                message = "This serial number is in queue at {}, Please wait".format(tmp_queue_stack.index(tmp_sn) + 1)
            else:
                message = "This serial number({}) is access hardware({}) now".format(tmp_sn, tmp_hardware_name)
                self.return_queue["error"] = False
        else:# Hardware is free.
            if len(tmp_queue_stack) == 0:
                self._hardware_working_with[tmp_hardware_name] = {
                    "sn": tmp_sn,
                    "entry_time": datetime.now(),
                    "timeout": int(queue.get("timeout"))
                }
                self.return_queue["error"] = False
                message = "Hardware is not working, This serial number({}) is using {} now".format(tmp_sn, tmp_hardware_name)
            elif tmp_sn in tmp_queue_stack:
                if tmp_queue_stack.index(tmp_sn) == 0:
                    self._hardware_working_with[tmp_hardware_name] = {
                        "sn": tmp_sn,
                        "entry_time": datetime.now(),
                        "timeout": int(queue.get("timeout"))
                    }
                    self.return_queue["error"] = False
                    message = "Hardware is not working, This serial number({}) is using {} now".format(tmp_sn, tmp_hardware_name)
                    self._queue_stack.get(tmp_hardware_name).remove(tmp_sn)
                else:
                    message = "This serial number is not first queue(on {} queue) please try again".format(tmp_queue_stack.index(tmp_sn) + 1)
            else:
                message = "This serial number({}) is added to queue please try again".foramt(tmp_sn)
                if not self._queue_stack.get(tmp_sn):
                    self._queue_stack[tmp_hardware_name] = [tmp_sn]
                else:
                    self._queue_stack.get(tmp_hardware_name).append(tmp_sn)

        self.return_queue["data"] = message
        self.print_log.info(self.log_header, message)

        return
