# coding: utf-8
from __future__ import absolute_import
from datetime import datetime
from typing import List, Dict
from model.swagger.base_model_ import Model
from model.swagger import util
from controllers.setting_controller import get_release_version_by_location
import platform
import shutil
import os

import subprocess
import sys
import json
from service.logging import Logging
from flask import current_app as app


class Testing(Model):

    def __init__(self):
        self._odc_script_directory = "ODC_Script"
        self._root_path = "C:\\Robot" if platform.system() == "Windows" else "/opt/Robot"
        self._scanin_chamber_file_name = os.getenv('SCANIN_CHAMBER')
        self._scanout_chamber_file_name = os.getenv('SCANOUT_CHAMBER')
        self._scanin_file_name = os.getenv('SCANIN_ODC')
        self._scanout_file_name = os.getenv('SCANOUT_ODC')
        self._release_file_name = os.getenv('RELEASE_FILENAME')
        self._archive_directory = "archive"
        self._view_log_directory = "view_logs"
        self._interaction_images_directory = "Interaction_images"
        self._logs_directory = "Logs"
        self._listener_file_name = "listener.py"
        self._library_directory = "Library"
        self._return_data = {
            "data": False,
            "error": False
        }
        self._print_log = Logging()

    @classmethod
    def from_dict(cls, dikt) -> 'Testing':
        # Returns the dict as a model
        return util.deserialize_model(dikt, cls)

    @property
    def root_path(self) -> str:
        return self._root_path

    @root_path.setter
    def root_path(self, val):
        test_type, slot_no = val
        if not test_type == "Production":
            self._root_path = self._root_path.replace("Robot", "Robot_Debug")
        else:
            release_version = get_release_version_by_location(slot_no)
            self._root_path = "%s/%s" % (self._root_path,release_version['value'])
            # self._root_path = self._root_path
    @property
    def root_logs(self) -> str:
        return self._root_logs

    # @root_path.setter
    # def root_path(self, test_type):
    #     if not test_type == "Production":
    #         self._root_path = self._root_path.replace("Robot", "Robot_Debug")

    # @root_path.setter
    # def root_path(self, test_type):
    #     if not test_type == "Production":
    #         self._root_path = self._root_path.replace("Robot", "Robot_Debug")

    @property
    def root_log_path(self) -> str:
        return "C:\\Logs_Robot" if platform.system() == "Windows" else "/opt/Logs_Robot"

    @property
    def timestamp(self) -> str:
        # Get timestamp
        return datetime.now().strftime("%Y%m%d-%H%M%S")

    @property
    def getArchivePath(self) -> str:
        tmp = os.path.join(self.root_log_path, self._archive_directory)
        if not os.path.exists(tmp):
            os.mkdir(tmp)
            os.chmod(tmp, 0o777)
        return tmp

    @property
    def getInteractionimagesPath(self) -> str:
        tmp = os.path.join(self.root_path, self._interaction_images_directory)
        return tmp

    @property
    def getLibraryPath(self) -> str:
        return self._library_directory

    @property
    def getListenerScript(self) -> str:
        return os.path.join(app.root_path, self._listener_file_name)

    @property
    def print_log(self) -> 'Logging':
        return self._print_log

    @property
    def return_data(self) -> dict:
        return self._return_data

    @property
    def getViewLogPath(self) -> str:
        tmp = os.path.join(self.root_log_path, self._view_log_directory)
        if not os.path.exists(tmp):
            os.mkdir(tmp)
            os.chmod(tmp, 0o777)
        return tmp

    @property
    def getLogsPath(self) -> str:
        tmp = os.path.join(self.root_path, self._logs_directory)
        if not os.path.exists(tmp):
            os.mkdir(tmp)
            os.chmod(tmp, 0o777)
        return tmp

    def uut_log_path(self, *args) -> str:
        if len(args) > 1:
            tmp = os.path.join(self.root_path, "Logs",
                               "{}_{}_{}".format(args[0], args[1], args[2]))
            if not os.path.exists(tmp):
                os.mkdir(tmp)
                os.chmod(tmp, 0o777)
            return tmp
        elif len(args) == 1:
            return os.path.join(self.root_path, "Logs", args[0].get("uut_log_dir"))

    def bom_path(self, sn: str) -> str:
        # Get bom path
        # return "{}/ODC_Script/BOM/{}".format(self.root_path, sn)
        return os.path.join(self.root_path, self._odc_script_directory, "BOM", sn)

    def getParameterRobot(self, result_odc: dict, request_body: dict) -> str:
        # Get all parameter that using pass to robot testing
        sn = request_body.get("serial_number")
        second_param = request_body.get("second_param")
        batch_id = request_body.get("batch_id")
        second_param_name = list(second_param.keys())[0]
        second_param_value = list(second_param.values())[0]
        testcase_list = request_body.get("test_case")
        ts = self.timestamp
        sn_timestamp = "{}_{}".format(sn, ts)
        uut_log_path = self.uut_log_path(result_odc.get("product_id"), sn, ts)

        robot_obj = {
            "serial_number": sn,
            "operation_id": request_body.get("operation_id"),
            "batch_id": batch_id,
            "slot_location": request_body.get("slot_location"),
            "test_mode": request_body.get("test_mode"),
            "test_robot_name": os.path.join(self.root_path, "{}_{}_{}.robot".format(result_odc.get("part_number"),
                                                                                    result_odc.get("product_reversion"), request_body.get("logop"))),
            "dir_uut_log_path": uut_log_path,
            "test_log_name": os.path.join(uut_log_path, "log_{}".format(sn_timestamp)),
            "test_output_name": os.path.join(uut_log_path, "output_{}".format(sn_timestamp)),
            "test_report_name": os.path.join(uut_log_path, "report_{}".format(sn_timestamp)),
            "raw_logs_path": os.path.join(uut_log_path, "Raw_logs"),
            "console_log_path": os.path.join(uut_log_path, "{}.monitor".format(sn_timestamp)),
            "timestamp": ts,
            "test_test": ""

        }

        if len(testcase_list) > 0:
            for test_case in testcase_list:
                robot_obj["test_test"] = '{} -t {}'.format(
                    robot_obj["test_test"], testcase_list[test_case])

        return "--listener {} {} -v serial_number:{} -v operation_id:{} -v slot_location:{} -v test_mode:{} -v Raw_logs_path:{} -v timestamp:{} -v batch_id:{} -v port_api:{} -v {}:{} -d {} -o {} -l {} -r {}".format(
            self.getListenerScript, robot_obj.get("test_test"), robot_obj.get("serial_number"), robot_obj.get("operation_id"), robot_obj.get("slot_location"), robot_obj.get(
                "test_mode"), robot_obj.get("raw_logs_path"), robot_obj.get("timestamp"), robot_obj.get("batch_id"), os.getenv('PORT'), second_param_name, second_param_value,
            robot_obj.get("dir_uut_log_path"), robot_obj.get(
                "test_output_name"), robot_obj.get("test_log_name"),
            robot_obj.get("test_report_name")), robot_obj.get("test_robot_name"), '> {} 2>&1'.format(robot_obj.get("console_log_path")), ts

    @property
    def checkListenerFileExists(self) -> bool:
        return False if not os.path.exists(self.getListenerScript) else True

    def checkRobotFileExists(self, result_odc, request_body) -> bool:
        tmp_robot_path = os.path.join(self.root_path, "{}_{}_{}.robot".format(result_odc.get(
            "part_number"), result_odc.get("product_reversion"), request_body.get("logop")))

        return False if not os.path.exists(tmp_robot_path) else True

    def getScaninPathScript(self) -> str:
        # Get scan-in script path that keep on /root_path/ODC_Script
        # return '/{}/ODC_Script/Scanin_ODC.py'.format(self.root_path)
        return os.path.join(self.root_path, self._odc_script_directory, self._scanin_file_name)

    def getScaninChamberPathScript(self) -> str:
        # Get scan-in script path that keep on /root_path/ODC_Script
        # return '/{}/ODC_Script/Scanin_ODC.py'.format(self.root_path)
        return os.path.join(self.root_path, self._odc_script_directory, self._scanin_chamber_file_name)

    def getScanoutPathScript(self) -> str:
        # Get scan-out script path that keep on /root_path/ODC_Script
        # return '/{}/ODC_Script/Scanout_ODC.py'.format(self.root_path)
        print(self.root_path, "self.root_path")
        return os.path.join(self.root_path, self._odc_script_directory, self._scanout_file_name)
    
    def getScanoutChamberPathScript(self) -> str:
        # Get scan-out script path that keep on /root_path/ODC_Script
        # return '/{}/ODC_Script/Scanout_ODC.py'.format(self.root_path)
        print(self.root_path, "self.root_path")
        return os.path.join(self.root_path, self._odc_script_directory, self._scanout_chamber_file_name)

    def archiveLogFile(self, body: dict, start_time: str) -> str:

        tmpArc = self.getArchivePath
        tmpDate = os.path.join(tmpArc, start_time)
        if not os.path.exists(tmpDate):
            os.mkdir(tmpDate)
            os.chmod(tmpDate, 0o777)

        if len(body.get("log_name")) > 0:
            template = body.get("log_name")
        else:
            template = body.get("uut_log_dir")

        tmpPath = os.path.join(tmpDate, template)
        try:
            shutil.make_archive(tmpPath, 'zip', self.uut_log_path(body))
            shutil.rmtree(self.uut_log_path(body))
        except Exception as e:
            return False, e

        return True, ""

    def createMetadataLog(self, body: dict, dataLog: dict) -> bool:
        if len(body.get("log_name")) > 0:
            tmpName = body.get("log_name")
        else:
            tmpName = body.get("uut_log_dir")
        tmpArcPath = self.getArchivePath
        tmpDate = os.path.join(tmpArcPath, dataLog.get("start_time")[:10])
        tmpDataPath = os.path.join(tmpDate, "{}.info".format(tmpName))

        if not os.path.exists(tmpDate):
            os.mkdir(tmpDate)
            os.chmod(tmpDate, 0o777)

        try:
            with open(tmpDataPath, 'w') as f:
                json.dump(dataLog, f, ensure_ascii=False)
            # with open(tmpDataPath, "w") as content:
            #     content.write("filename={}\n".format(tmpName))
            #     content.write("start_time={}\n".format(dataLog.get("start_time")))
            #     content.write("end_time={}\n".format(dataLog.get("end_time")))
            #     content.write("result={}\n".format(dataLog.get("result")))
        except Exception as e:
            if os.path.exists(tmpDataPath):
                shutil.rmtree(tmpDataPath)
            return False, "Error when create metadata with: {}".format(e)

        return True, ""

    def viewLog(self, *args):
        '''
            View log have separate out to 2 format:
                One => View specific file. User want to view result of the one testing with serial number and start time of the test
                Two => Get all log information such as start time, end time and filename for users want to see overall status of all testing.
        '''
        if len(args) == 0:
            # View overview log of the all testing
            data = []
            for roots, dirs, files in os.walk(self.getArchivePath):
                for f in files:
                    if f.endswith("zip"):
                        tmpObj = {}
                        try:
                            tmpInfo = f.split(".")[0]
                            if not os.path.exists(os.path.join(roots, "{}.info".format(tmpInfo))):
                                self.print_log.error(
                                    "Testing-viewLog", "Found zip file but not found its info {}".format(f))
                                continue
                            tmpObj["filename"] = f
                            # with open("{}/{}/{}.info".format(roots, f, tmpInfo), "r") as content:
                            # Read JSON file

                            with open(os.path.join(roots, "{}.info".format(tmpInfo))) as data_file:
                                try:
                                    data_loaded = json.load(data_file)
                                except ValueError as e:
                                    print('value error')
                                    continue
                            '''
                            with open(os.path.join(roots, "{}.info".format(tmpInfo)), "r") as content:
                                for ct in content:
                                    if "start_time" in ct:
                                        tmpObj["start_time"] = ct.split("=")[-1].strip()
                                    if "end_time" in ct:
                                        tmpObj["end_time"] = ct.split("=")[-1].strip()
                                    if "result" in ct:
                                        tmpObj["result"] = ct.split("=")[-1].strip()
                            if len(tmpObj.keys()) >= 3:
                                data.append(tmpObj)
                            print(tmpObj)
                            '''
                            if data_loaded["start_time"]:
                                tmpObj["start_time"] = data_loaded["start_time"]
                            if data_loaded["end_time"]:
                                tmpObj["end_time"] = data_loaded["end_time"]
                            if data_loaded["result"]:
                                if data_loaded["result"] == "ABORT":
                                    tmpObj["result"] = "aborted"
                                elif data_loaded["result"] == "PASS":
                                    tmpObj["result"] = "passes"
                                elif data_loaded["result"] == "FAIL":
                                    tmpObj["result"] = "failed"
                                else:
                                    tmpObj["result"] = "failed"

                            if len(tmpObj.keys()) >= 3:
                                data.append(tmpObj)
                        except Exception as e:
                            self.return_data.update({"error": e})
                            # return
                            continue

            self.return_data.update({"data": data})
            self.print_log.info("Testing-viewLog",
                                "View all logs are complete")
            return 200, data
        else:
            # View status of the one testing
            tmpPathLogZip = os.path.join(
                self.getArchivePath, args[0], "{}".format(args[1]))
            if not os.path.exists(self.getViewLogPath):
                os.mkdir(self.getViewLogPath)
                os.chmod(self.getViewLogPath, 0o777)
            tmpPathLogDir = os.path.join(
                self.getViewLogPath, args[1].replace('.zip', ''))
            self.print_log.info("Testing-viewLog",
                                "View log file: {}".format(tmpPathLogZip))
            if not os.path.exists(tmpPathLogDir):
                os.mkdir(tmpPathLogDir)
                os.chmod(tmpPathLogDir, 0o777)
            if not os.path.exists(tmpPathLogZip):
                self.return_data.update(
                    {"error": "Cannot view log file {}.zip because this file is not found.".format(args[1])})
            else:
                try:
                    # unpack_archive of shutil library has argruments are:
                    #   First => path zip log file
                    #   Two => extract zip to this path
                    #   Three => type of archive file
                    shutil.unpack_archive(tmpPathLogZip, tmpPathLogDir, 'zip')
                    tmpInfo = tmpPathLogZip.split(".")[0]

                    if not os.path.exists("{}.info".format(tmpInfo)):
                        self.print_log.error(
                            "Testing-viewLog", "Found zip file but not found its info {}".format(f))
                        self.return_data.update({"data": True, "error": None})
                        return 500, return_data

                    with open("{}.info".format(tmpInfo)) as data_file:
                        try:
                            data_loaded = json.load(data_file)
                        except ValueError as e:
                            print('value error')
                            return 500, return_data
                    print(data_loaded)
                    self.return_data.update(
                        {"data": data_loaded, "error": None})
                    return 200, data_loaded
                except Exception as e:
                    self.return_data.update(
                        {"error": "Error on extract file {}.zip:\n{}".format(args[1], e)})
                    return 500, self.return_data

    def run_command_python(self, python_file, parameter):
        return subprocess.check_output([sys.executable, python_file, parameter], universal_newlines=True)
