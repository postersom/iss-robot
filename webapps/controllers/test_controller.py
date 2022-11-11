import os
import re
import sys
import signal
import shutil
import psutil
import logging
import subprocess
import json


from database import db_session
from datetime import datetime
from connexion import NoContent, request

from model.swagger.testing import Testing
from model.swagger.managing import Managing
from model.test import Test
from model.status import Status
from model.testView import test_schema
from model.testcaselist import TestCaseList

from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.orm import joinedload


from controllers.status_controller import *
from controllers.setting_controller import *
from controllers.userinteraction_controller import *


WORKING = []
managing_model = Managing()


def remove_sync_point_internal(sn):
    global managing_model
    try:
        managing_model.all_sn_scaning.remove(sn) if sn in managing_model.all_sn_scaning else None
        return True
    except Exception as e:
        print(e)
    return False


# def get_tests(limit):
#     q = db_session.query(Test).options(joinedload('statuses')).all()
#     return [test_schema.dump(p).data for p in q][:limit]


def get_tests(limit):
    q = db_session.query(Test).options(joinedload('statuses')).all()
    return [test_schema.dump(p) for p in q][:limit]


def get_test_slots(total):
    test_slot = [{'slot': i, 'data': {}} for i in range(1, total+1)]
    q = db_session.query(Test).options(joinedload('statuses')).all()
    for p in q:
        location = test_schema.dump(p).data['location']
        item = test_schema.dump(p).data
        item['statuses'] = sorted(item['statuses'], key=lambda i: i['id'], reverse=True)
        item['test_info'] = dict()
        if len(item['statuses']) > 0:
            item['test_info']['created'] = item['statuses'][-1]['created']
            if ':' == item['test_info']['created'][-3:-2]:
                item['test_info']['created'] = item['test_info']['created'][:-3] + item['test_info']['created'][-2:]
            if ':' == item['statuses'][0]['created'][-3:-2]:
                item['statuses'][0]['created'] = item['statuses'][0]['created'][:-3] + item['statuses'][0]['created'][-2:]
            if item['statuses'][0]['status'] != 'end_suite':
                item['test_info']['status'] = 'Testing'
                for test_case in item['statuses']:
                    if test_case['status'] == 'end_test' and test_case['message'].split(':')[1][:4] == 'FAIL':
                        item['test_info']['status'] = 'failing'
                        break

                item['test_info']['test_case'] = item['statuses'][0]['message']
                created_time = datetime.datetime.strptime(item['test_info']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                elapsed_time = datetime.datetime.now(tz) - created_time.replace(tzinfo=tz)
                item['test_info']['elapsed_time'] = str(elapsed_time).split('.')[0]
            else:
                created_time = datetime.datetime.strptime(item['test_info']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                finished_time = datetime.datetime.strptime(item['statuses'][0]['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                elapsed_time = finished_time - created_time
                item['test_info']['elapsed_time'] = str(elapsed_time).split('.')[0]
                item['test_info']['status'] = item['statuses'][0]['message'].split(':')[1].strip()
                if item['test_info']['status'] == 'FAIL':
                    item['test_info']['status'] = 'failed'
                elif item['test_info']['status'] == 'PASS':
                    item['test_info']['status'] = 'passes'
                else:
                    item['test_info']['status'] = 'failed'
        test_slot[int(location)-1] = {'slot': int(location), 'data': item}
    if len(test_slot) > 0:
        user_interactions = get_interactions()
        for interact in user_interactions:
            tmp_slot = int(interact['slot_no'])
            test_slot[tmp_slot-1]['data']['user_interactions'] = interact
    return test_slot


def get_test(test_id):
    test = db_session.query(Test).filter(Test.id == id).one_or_none()
    return test.dump() or ('Not found', 404)


def put_test(test):
    logging.info('Creating test ...')
    test['created'] = datetime.datetime.now()
    db_session.add(Test(**test))
    db_session.commit()
    return NoContent, 201


def delete_test(id):
    test = db_session.query(Test).filter(Test.id == id).one_or_none()
    if test is not None:
        logging.info('Deleting pet %s..', id)
        db_session.query(Test).filter(Test.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


def add_testing(batch_id, sn, robot_name, operation_id, location, uut_log_dir, test_mode, code_from, logop, product_name):
    db_session.add(Test(batch_id=batch_id, serial_number=sn, robot_name=robot_name, operation_id=operation_id, test_mode=test_mode, code_from=code_from,
                        logop=logop, product_name=product_name, uut_log_dir=uut_log_dir, flag="unlock", location=location, created=datetime.datetime.now()))
    db_session.commit()


def remove_testing(location):
    test = db_session.query(Test).filter(Test.location == location).delete()
    statuses = db_session.query(Status).filter(Status.slot_no == location).delete()
    db_session.commit()


def add_testcaselist(test_case, slot_no):
    db_session.add(TestCaseList(test_case=test_case, slot_no=slot_no))
    db_session.commit()


def remove_testcaselist(slot_no):
    test_case = db_session.query(TestCaseList).filter(TestCaseList.slot_no == slot_no).delete()
    db_session.commit()


def check_test_slot_isEmpty(slot_no):
    q = test = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    if not q:
        return True
    return False

# Testing functions ###


def scanin(body):
    """
        execute robot framework to testing with serial number that provide from website
    """
    # Prepare variable for this process

    global managing_model
    testing_model = Testing()
    tmpReturnData = testing_model.return_data
    request_body = Testing.from_dict(request.get_json())
    log_header = '[Testing-Scanin]'
    managing_model.print_log.info(log_header, f'request body is\n{request_body}')
    testing_model.root_path = request_body.get('code_from'), request_body.get('slot_location')
    print('scanin', testing_model.root_path)

    ck_empty = testing_model.root_path.split('/')

    # Send verify serial number to ODC if get status OK process can start test
    if request_body.get('odc_type') == 'verifychamber':
        try:
            result_odc = testing_model.run_command_python(testing_model.getScaninChamberPathScript(), json.dumps(request_body))
            result_odc_json = json.loads(result_odc)
        except Exception as e:
            managing_model.print_log.error(log_header, f'Error with: {e}')
            tmpReturnData['error'] = 'Error with execution ODC Script.'
        else:
            managing_model.print_log.info(log_header, f'Verify process is done.\n{result_odc_json}')
            tmpReturnData['data'] = result_odc_json

        status = 200 if tmpReturnData['error'] else 400
        return tmpReturnData, 200
    elif request_body.get("odc_type") == "verify":
        try:
            result_odc = testing_model.run_command_python(testing_model.getScaninPathScript(), json.dumps(request_body))
            result_odc_json = json.loads(result_odc)
        except Exception as e:
            if ck_empty[3] == 'empty':
                print('Please create Zone Release', ck_empty[3])
                tmpReturnData['error'] = 'Please create Zone Release'
            else:
                managing_model.print_log.error(log_header, f'Error with: {e}')
                tmpReturnData['error'] = 'Error with execution ODC Script.'
        else:
            managing_model.print_log.info(log_header, "Verify process is done.\n{}".format(result_odc_json))
            tmpReturnData["data"] = result_odc_json

        status = 200 if tmpReturnData["error"] else 400
        return tmpReturnData, 200
    # If parameter not found process cannot start test
    if not request_body or not request_body.get("sn_count"):
        managing_model.print_log.error(log_header, "Process is not starting test because parameter is empty.Please try again")
        tmpReturnData["error"] = "Process is not starting test because parameter is empty.Please try again"
        return json.dumps(tmpReturnData), 400
    managing_model.print_log.info(log_header, testing_model.getScaninPathScript())

    tmp_batch_id = request_body.get("batch_id")
    tmp_sn = request_body.get("serial_number").strip()

    if tmp_batch_id not in managing_model.all_sn_scaning:
        managing_model.all_sn_scaning[tmp_batch_id] = {"sns": [], "sn_count": int(request_body.get("sn_count"))}

    if tmp_sn not in managing_model.all_sn_scaning.get(tmp_batch_id) and not request_body.get("odc_type") == "verify":
        managing_model.print_log.info(log_header, "New sn scan-in")
        managing_model.all_sn_scaning[tmp_batch_id]["sns"].append(request_body.get("serial_number").strip())
    else:
        tmpReturnData["error"] = "Duplicate sn scan-in: {}".format(tmp_sn)
        return tmpReturnData, 400

    # Execute ODC Script
    try:
        result_odc = testing_model.run_command_python(testing_model.getScaninPathScript(), json.dumps(request_body))
    except Exception as e:
        managing_model.print_log.error(log_header, f'Error on execute Scanin_ODC.py with: {e}')
        tmpReturnData['error'] = f'Process error on execute Scanin_ODC.py: {e}'
        return json.dumps(tmpReturnData), 400
    else:
        try:
            result_odc_json = json.loads(result_odc)
        except Exception as e:
            managing_model.print_log.error(log_header, "Cannot create json of result from odc script with: {}".format(e))
            tmpReturnData["error"] = "Process is not starting test when create json data from ODC script: {}".format(e)
            return json.dumps(tmpReturnData), 400
        else:
            managing_model.print_log.info(log_header, "Result from odc:\n{}".format(result_odc_json))
            try:
                if not testing_model.checkRobotFileExists(result_odc_json, request_body):
                    tmpReturnData["error"] = "Cannot found robot file please create robot file {}/{}_{}_{}.robot and try again.".format(
                        testing_model.root_path, result_odc_json.get("part_number"), result_odc_json.get("product_reversion"), request_body.get("logop"))
                    raise Exception
                # Check listener file will be found before execution
                if not testing_model.checkListenerFileExists:
                    tmpReturnData["error"] = "Cannot found listener file please create listener file and try again."
                    raise Exception

                # Set parameter for send to robot testing
                try:
                    parameter_robot_test, robot_name, console_log, param_timestamp = testing_model.getParameterRobot(result_odc_json, request_body)
                except Exception as e:
                    tmpReturnData["error"] = f"Process is not starting test: {e}"
                    raise Exception

                # create test in database
                if check_test_slot_isEmpty(request_body.get('slot_no')):

                    try:
                        test_case_list = request_body.get('test_case')
                        if len(test_case_list) > 0:
                            for test_case in test_case_list:
                                add_testcaselist(test_case_list[test_case], request_body.get('slot_no'))
                        # use param_timestamp for the same folder name
                        add_testing(tmp_batch_id,
                                    request_body.get("serial_number"),
                                    "{}/{}_{}_{}.robot".format(testing_model.root_path, result_odc_json.get("part_number"), result_odc_json.get("product_reversion"), request_body.get("logop")),
                                    request_body.get("operation_id"),
                                    request_body.get("slot_no"), "{}_{}_{}".format(result_odc_json.get("product_id"), request_body.get("serial_number"), param_timestamp),
                                    request_body.get('test_mode'),
                                    request_body.get('code_from'),
                                    request_body.get('logop'),
                                    result_odc_json.get('product_name'))
                        # Execute robot testing
                        cmd = "{} -m robot {} {} {} &".format(sys.executable, parameter_robot_test, robot_name, console_log)
                        print("cmd= {}".format(cmd))
                        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    except Exception as e:
                        tmpReturnData['error'] = f'Cannot add test: {e}'
                        remove_testcaselist(request_body.get('slot_no'))
                        remove_testing(slot_location_to_slot_no(request_body.get('slot_location')))
                        raise Exception

                else:
                    tmpReturnData['error'] = f"Process is not starting test: Test exist in database slot: {request_body.get('slot_location')}"
                    managing_model.print_log.error(log_header, tmpReturnData['error'])
            except Exception as e:
                managing_model.print_log.error(log_header, tmpReturnData['error'])
                if os.path.exists(f"{testing_model.bom_path(result_odc_json.get('serial_number'))}.py"):
                    os.remove(f"{testing_model.bom_path(result_odc_json.get('serial_number'))}.py")
                print(e)
            else:
                if not tmpReturnData['error']:
                    tmpReturnData['data'] = 'Process starting test'
                    tmpReturnData['error'] = None

    if not tmpReturnData['error'] is None:
        remove_sync_point_internal(tmp_sn)
    return tmpReturnData, 200 if tmpReturnData['data'] else 400

# Testing functions ###


def verify(body):
    """
        Execute robot framework to testing with serial number that provide from website
    """
    if req:= json.loads(body.decode()):
        result_odc = subprocess.check_output([sys.executable, '/opt/Robot/ODC_Script/Scanin_ODC.py', json.dumps(req)])
        print(f'Response from ODC: {result_odc}')
        return {'status': 'OK', 'error_message': 'Return value from ODC'}, 200
    return 'Parameter is empty', 401


def verify_testcase(body):
    request_body = body
    testing_model = Testing()
    testing_model.root_path = request_body.get('code_from'), request_body.get('slot_location')
    request_body['odc_type'] = 'verify'

    result_odc = json.loads(testing_model.run_command_python(testing_model.getScaninPathScript(), json.dumps(request_body)))
    result_odc['robot_path'] = testing_model.root_path
    return result_odc


def checkout(body):
    '''
        Delivery out testing from server with serial number
    '''
    tmpReturnError = "Cannot checkout because"
    global managing_model
    log_header = "[{}-{}]".format("Testing_Controller", "Checkout")
    request_body = Testing.from_dict(request.get_json())
    testing_model = Testing()
    tmpReturnData = testing_model.return_data
    # Set path of root this testing.
    # testing_model.root_path = request_body.get("test_mode")
    print(request_body.get("slot_location"), "root_path")

    testing_model.root_path = request_body.get("code_from"), request_body.get("slot_location")

    # testing_model.root_logs = request_body.get("test_mode")

    if not request_body:
        tmpReturnData["error"] = "Cannot checkout the test becuase parameter is empty"
        return tmpReturnData, 400

    serial_number = request_body.get("serial_number")
    uut_log_path = testing_model.uut_log_path(request_body)
    print(uut_log_path, "uut_log_path")
    bom_path = testing_model.bom_path(serial_number)
    request_body["uut_log_dir_path"] = uut_log_path
    
    # Execute Scanout_ODC.py for check can checkout this serial number
    print(request_body, "request_body")

    dataLog = get_test_info_status_by_slot(request_body.get("slot_no"))

    if not dataLog or len(dataLog['statuses']) == 0:
        managing_model.print_log.error(log_header, f'Checkout fail with: No test data in database serial number: {serial_number}')
        tmpReturnData['error'] = f'Checkout fail with: No test data in database serial number: {serial_number}'
        return tmpReturnData, 400

    dataLog["start_time"] = dataLog.get("start_time").strftime("%Y-%m-%d %H:%M:%S")
    request_body["start_time"] = dataLog["start_time"]
    dataLog["end_time"] = dataLog.get("end_time").strftime("%Y-%m-%d %H:%M:%S")
    request_body["end_time"] = dataLog["end_time"]

    release_version = get_release_version_by_location(request_body.get("slot_location"))
    
    request_body["release_version"] = release_version['value']

    try:
        result_odc = testing_model.run_command_python(testing_model.getScanoutPathScript(), json.dumps(request_body))

    except Exception as e:
        managing_model.print_log.error(
            log_header, "Error on execute Scanout_ODC.py with: {}".format(e))
        tmpReturnData["error"] = "{} error on execute Scanout_ODC.py: {}".format(tmpReturnError, e)
        return tmpReturnData, 400

    # Create JSON object from result of ODC script
    try:
        result_odc_json = json.loads(result_odc)
        print(result_odc_json, "result_odc_json")
    except Exception as e:
        managing_model.print_log.error(log_header, "Cannot create json from result scanout odc with: {}".format(e))
        tmpReturnData["error"] = "{} error on parse data to json"
        return tmpReturnData, 400

    if not result_odc_json.get("status") == "OK" or not result_odc_json.get("status"):
        managing_model.print_log.error(log_header, "ScanOut from ODC return fail with: {} ".format(result_odc_json.get("error_message")))
        tmpReturnData["error"] = "{} get status fail from Scanout_ODC.py because: {}".format(tmpReturnError, result_odc_json.get("error_message"))
        return tmpReturnData, 400

    try:
        result_delete_inteaction = delete_interaction_by_slot(request_body.get("slot_no"))
    except Exception as e:
        managing_model.print_log.error(log_header, "Error with: {}".format(e))
        tmpReturnData["error"] = True

    # Extract log file before remove directory
    checkZip, message = testing_model.archiveLogFile(
        request_body, dataLog.get("start_time")[:10])
    if not checkZip:
        managing_model.print_log.error(log_header, "Cannot create archive file because: {}".format(message))
        tmpReturnData["error"] = "{} error on archive file: {}".format(tmpReturnError, message)
        return tmpReturnData, 400

    checkMeta, message = testing_model.createMetadataLog(request_body, dataLog)
    if not checkMeta:
        managing_model.print_log.error(
            log_header, "Cannot create metadata file because: {}".format(message))
        tmpReturnData["error"] = "{} error on creating metadata file: {}".format(
            tmpReturnError, message)
        return tmpReturnData, 400

    try:
        # Remove all files in UUT of this serial number if path exists
        if os.path.exists(uut_log_path):
            shutil.rmtree(uut_log_path)
        # Remove all file in BOM of this serial number if path exists
        if os.path.exists(bom_path):
            shutil.rmtree(bom_path)
    except Exception as e:
        managing_model.print_log.error(
            log_header, "Cannot checkout {}:\n{}".format(serial_number, e))
        tmpReturnData["error"] = "{} error on delete data of {} with {}".format(
            tmpReturnError, serial_number, e)
        return tmpReturnData, 400

    remove_testcaselist(slot_location_to_slot_no(request_body.get("slot_location")))
    remove_testing(slot_location_to_slot_no(request_body.get("slot_location")))
    managing_model.print_log.info(log_header, "Checkout {} complete".format(serial_number))

    tmp_batch_id = request_body.get("batch_id")
    if managing_model.all_sn_scaning.get(tmp_batch_id) and len(managing_model.all_sn_scaning.get(tmp_batch_id).get("sns")) > 0:
        managing_model.all_sn_scaning.pop(tmp_batch_id)
        if managing_model.sn_sync.get(tmp_batch_id):
            managing_model.sn_sync.pop(tmp_batch_id)
        managing_model.print_log.info(log_header, "Remove data scan-in complete")
    managing_model.print_log.info(log_header, "Checkout {} complete".format(serial_number))

    # De-Allocate variable
    testing_model = None
    serial_number = None
    uut_log_path = None
    bom_path = None
    checkZip = None
    message = None
    tmp_csn_sn = None
    tmpReturnData["data"] = "Checkout is complete"
    return tmpReturnData, 200

# call init testcase


def set_flag_abort(body):
    request_body = json.loads(body.decode())
    if not request_body:
        return "Parameter is empty", 400

    slot_no = slot_location_to_slot_no(request_body["slot_location_no"])
    flag = request_body["flag"]
    res = {"data": {"message": ""}, "error": ""}

    q = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    q.flag = flag
    res["data"]["message"] = "Set flag Successfully."
    q.update()
    db_session.commit()

    return res, 200


def test_get_abort(slot_no):
    q = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    if q.flag == "abort":
        return True, 200
    return False, 200


def abort_pid(pid):
    # Send the signal to all the process groups
    os.killpg(os.getpgid(pid), signal.SIGTERM)
    return "ff"


def abort_process(test_location):
    procs = {p.pid: p.info for p in psutil.process_iter(
        attrs=['name', 'cmdline']) if 'python' in p.info['name']}

    for x in procs:
        cmd = procs[x]["cmdline"]
        for var in reversed(cmd):
            if test_location in var:
                # os.killpg(os.getpgid(x), signal.SIGTERM)  # Send the signal to all the process groups
                os.kill(x, signal.SIGTERM)
                return "Killed, Test Abort Successfully."
    return "Not found process, Test may be aborted or finished"

# ui call abort command


def test_abort(body):
    request_body = json.loads(body.decode())
    if not request_body:
        return "Parameter is empty", 400

    slot_no = slot_location_to_slot_no(request_body["test_location"])
    print(slot_no)
    res = {"data": {"message": ""}, "error": ""}

    q = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    if q.flag == "lock":
        q.flag = "abort"
        res["data"]["message"] = "Set Abort Successfully. Please wait for test ending."
        q.update()
        db_session.commit()
    elif q.flag == "abort":
        res["data"]["message"] = "Test was set to abort. Please wait for test ending."
    else:
        message = abort_process(request_body["test_location"])
        res["data"]["message"] = message

    return res, 200

# test profile call to check abort flag


def get_abort(slot_location_no):
    '''
        Abort robot testing process with user
    '''
    slot_no = slot_location_to_slot_no(slot_location_no)

    #testing_model = Testing()
    #tmpReturnData = testing_model.return_data
    #global managing_model
    print(slot_no)
    q = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    print(q.flag)

    res = {"data": {"flag": q.flag}, "error": ""}
    return res, 200

    # managing_model.log_header = "[{}-{}]".format("Testing_Controller", "abort")
    # tmp_csn_sn = request_body.get("slot_location").split("_", 1)[0]

    # if not tmp_csn_sn:
    #     managing_model.print_log.error(managing_model.log_header, "Chassis is not found")
    #     tmpReturnData["error"] = "Chassis is not found on slot-location"
    #     return json.dumps(tmpReturnData), 400

    # try:
    #     tmp_parent_sn = managing_model.all_sn_scaning.get(tmp_csn_sn)
    # except Exception as e:
    #     managing_model.print_log.error(managing_model.log_header, "Cannot get chassis serial number that user starting test\n:{}".format(e))
    #     tmpReturnData["error"] = "Cannot get chassis serial number that user starting test"
    #     return json.dumps(tmpReturnData), 400

    # tmp_parent_sn.remove(request_body.get("serial_number"))

    #tmpReturnData["data"] = "Abort is complete"

    # De-allowcate variable
    # request_body = None
    # testing_model = None
    # tmp_csn_sn = None
    # tmp_parent_sn = None

    # return tmpReturnData, 200


def view_log(start_time, sn):
    log_header = "[{}-{}]".format("Testing_Controller", "viewLog")
    managing_model.print_log.info(
        log_header, "Welcome to view log: {}".format(sn))
    testing_model = Testing()
    tmpReturnError = "Cannot view log because"
    tmpReturnData = testing_model.return_data
    managing_model.print_log.info(
        log_header, "star_time: {}\nsn: {}".format(start_time, sn))

    if not (sn == "" and start_time == "") and (sn == "" or start_time == ""):
        testing_model.print_log.error(
            log_header, "some parameter is empty please try again with all parameter are not empty or all parameter are empty")
        tmpReturnData["error"] = "some parameter is empty please try again with all parameter are not empty or all parameter are empty"
    else:
        try:
            if not (sn == "" and start_time == ""):
                try:
                    datetime.datetime.strptime(start_time, "%Y-%m-%d")
                except Exception as e:
                    testing_model.print_log.error(
                        log_header, "Datetime is wrong format, , it should be YYYY-mm-dd")
                    return "Start Datetime is wrong format, it should be YYYY-mm-dd: {}".format(start_time), 400
                else:
                    testing_model.viewLog(start_time, sn)
            else:
                testing_model.viewLog()
        except Exception as e:
            testing_model.print_log.error(
                log_header, "Error view log with: {}".format(e))

    status = 200 if tmpReturnData.get("data") else 400

    # De-allocate variable
    testing_model = None
    log_header = None
    tmpReturnError = None

    return tmpReturnData, status


def slot_location_to_slot_no(slot_location):
    slot_no = 0
    if(slot_location != ''):
        slot_no = re.search(r'\d+\_*\d*', slot_location).group()
    return str(slot_no)


def sync_point(body):
    '''
        Function sync point for provide robot framework wait or continue testing
    '''
    global managing_model
    request_body = json.loads(body.decode())
    #tmpReturnData = managing_model.return_sync_point
    managing_model.log_header = "{}-{}".format("managing", "sync_point")
    tmp_allow_timeout = True if request_body.get(
        "allow_timeout") == "True" else False
    request_body["allow_timeout"] = tmp_allow_timeout
    tmp_batch_id = request_body.get("batch_id")
    managing_model.print_log.info(
        managing_model.log_header, "Parameter: {}".format(request_body))
    tmp_return = {
        "data": None,
        "error": True
    }

    if managing_model.remove_csn_after_complete(request_body):
        tmp_return["data"] = "Sync-point is complete"
        tmp_return["error"] = None
        managing_model.print_log.info(managing_model.log_header, "after remove Sync sn: {}\n ".format(managing_model.sn_sync))
        return tmp_return, 200

    if request_body.get("setup"):
        request_body["setup"] = True if request_body.get("setup") == "True" else False

    if request_body.get("sn_count") == 1:
        tmp_return['data'] = "Sync-point is complete"
        tmp_return['error'] = None
        return tmp_return, 200

    try:
        if managing_model.sn_sync.get(tmp_batch_id) and len(managing_model.sn_sync.get(tmp_batch_id).get("sn")) > 0 and request_body.get("allow_timeout"):
            managing_model.check_timeout_sync_point(request_body)
        managing_model.check_sync_point(request_body)
    except Exception as e:
        managing_model.print_log.error(managing_model.log_header, "error on check sync point: {}".format(e))

    tmp_return["data"] = managing_model.sn_sync.get(tmp_batch_id).get("data")
    tmp_return["error"] = managing_model.sn_sync.get(tmp_batch_id).get("error")
    managing_model.print_log.info(managing_model.log_header, "return data: {}".format(tmp_return))

    # De-allocate variable
    request_body = None
    status = 200 if not tmp_return.get("error") else 400

    return tmp_return, status


def remove_sync_point(body):
    '''
        Remove serial number that kept on scan-in process out of stack that using check on sync-point process
    '''
    global managing_model
    request_body = json.loads(body.decode())
    tmpReturnData = managing_model.return_sync_point
    managing_model.log_header = "{}-{}".format("Test_controller", "remove_sync_point")
    managing_model.print_log.info(managing_model.log_header, "Remove sync-point request from robot")
    managing_model.remove_sn_from_syncpoint(request_body)
    managing_model.print_log.info(managing_model.log_header, "Status from remove serial-number: {}".format(managing_model.return_sync_point.get("error")))
    status = 200 if not tmpReturnData.get("error") else 400
    return tmpReturnData, status


def queue_hardware(body):
    '''
        Function Request/Release queue for using a queue or using a queue complete.
    '''
    global managing_model
    managing_model.log_header = "managing-queue"
    queue = json.loads(body.decode())
    managing_model.print_log.info(
        managing_model.log_header, "Check parameter: {}".format(body))
    tmpReturnData = managing_model.return_queue
    tmpReturnData["error"] = True
    if not queue.get("serial_number") and not queue.get("type"):
        tmpReturnData["error"] = "Cannot get serial number and queue type please check parameter and try again."
    else:
        try:
            managing_model.queue_access_hardware(queue)
        except Exception as e:
            managing_model.print_log.info(managing_model.log_header, e)
            tmpReturnData["data"] = e
    status = 200 if not tmpReturnData['error'] else 400
    managing_model.print_log.info(
        managing_model.log_header, "Return: {}".format(tmpReturnData))
    return tmpReturnData, status
# clean and update git data


def update_latest_code(repo_path):
    git_query = subprocess.Popen('/usr/bin/git checkout . --quiet', cwd=repo_path,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = git_query.communicate()
    if len(error.decode('utf-8').strip()) > 0:
        print("checkout . {}|{}".format(output, error))
        return (error.decode('utf-8').strip(), True)
    git_query = subprocess.Popen('/usr/bin/git checkout master --quiet',
                                 cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = git_query.communicate()
    if len(error.decode('utf-8').strip()) > 0:
        print("checkout master {}|{}".format(output, error))
        return (error.decode('utf-8').strip(), True)
    git_query = subprocess.Popen('/usr/bin/git pull --quiet', cwd=repo_path,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, error) = git_query.communicate(timeout=10)
    if len(error.decode('utf-8').strip()) > 0:
        print("pull  {}|{}".format(output, error))
        return (error.decode('utf-8').strip(), True)
    return ("Code Updated", None)
