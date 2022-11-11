from database import db_session
from model.status import Status
from model.test import Test
from model.testcaselist import TestCaseList
from connexion import NoContent
import datetime
import logging

from sqlalchemy import or_
import os
from flask import g
from model.swagger.testing import Testing
from model.statusView import status_schema
from flask import current_app as app

import json
import re


# def get_statuses(limit):
#     q = db_session.query(Status)
#     return [status_schema.dump(p).data for p in q][:limit]


def get_statuses(limit):
    q = db_session.query(Status)
    return [status_schema.dump(p) for p in q][:limit]


def get_status(id):
    status = db_session.query(Status).filter(Status.id == id).one_or_none()
    return status.dump() or ('Not found', 404)


def get_status_by_slot(slot_no):
    statuses = db_session.query(Status).filter(Status.slot_no == slot_no)
    return [p.dump() for p in statuses]


def get_test_info_status_by_slot(slot_no):
    statuses = db_session.query(Status).filter(Status.slot_no == slot_no).filter(or_(Status.status == "start_suite",
                                                                                     Status.status == "end_suite",
                                                                                     Status.status == "end_test"))
    info = dict()
    info["statuses"] = get_status_by_slot(slot_no)
    for index, item in enumerate(info["statuses"]):
        item["created"] = item["created"].strftime("%Y-%m-%d %H:%M:%S")

    info["chassis_name"] = ''
    info["slot_no"] = ''
    info["result"] = ''
    for x in statuses:
        status = x.__dict__
        if status["status"] == "start_suite":
            info["start_time"] = status["created"]
        elif status["message"].split(':')[1][:5] == "ABORT":
            info["result"] = "ABORT"
        elif status["status"] == "end_suite":
            info["end_time"] = status["created"]
            if info["result"] != "ABORT":
                info["result"] = status["message"].split(':')[1].strip()
    return info


def put_status(status):
    slot_no = 0
    if status['test_location'] != '':
        loc = status['test_location']
        print(loc)
        slot_no = re.search(r'\d+\_*\d*', loc).group()

    logging.info('Creating status')
    logging.info('Put status to  : ' + slot_no)
    # logging.info('Put message : ' + status['message'])
    test = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    db_session.add(Status(status=status['status'],
                          message=status['message'],
                          slot_no=slot_no,
                          created=datetime.datetime.now(),
                          test_id=test.id))
    db_session.commit()
    socket = getattr(g, 'socket', None)
    data = update_data(slot_no)
    data_out = json.dumps(data, default=convert_timestamp)
    socket.emit('update_status', {"data": json.loads(data_out)}, namespace='/slot/' + str(slot_no))
    return NoContent, 201


def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return str(item_date_object)


def update_data(slot_no):
    raw_statuses = get_status_by_slot(slot_no)
    statuses = list()
    info = {'result': "Testing", 'slot_no': slot_no}
    if len(raw_statuses) == 0:
        return {}
    for index, item in enumerate(raw_statuses):
        if item["status"] == 'start_test':
            elapsed_time = datetime.datetime.now() - item['created']
            statuses.append({'name': item['message'], 'status': 'Testing', 'started': item['created'],
                             'finished': None, 'elapsed_time': str(elapsed_time).split('.')[0], 'reason': '',
                             "id": index})
        elif item["status"] == 'end_test':
            msg = item['message'].split(' ', 1)
            statuses[-1]['status'] = msg[0].replace("Result:", "")
            if len(msg) > 1:
                statuses[-1]['reason'] = msg[1]
            else:
                statuses[-1]['reason'] = '-'
            statuses[-1]['finished'] = item['created']
            elapsed_time = statuses[-1]['finished'] - statuses[-1]['started']
            statuses[-1]['elapsed_time'] = str(elapsed_time).split('.')[0]
            statuses[-1]['finished'] = str(statuses[-1]['finished']).split('.')[0]
            statuses[-1]['started'] = str(statuses[-1]['started']).split('.')[0]
        elif item["status"] == 'end_suite':
            info["result"] = item['message'].split(':')[1].strip()
        elif item["status"] == 'start_suite':
            pass
    if item["status"] != 'start_suite':
        statuses[-1]['started'] = str(statuses[-1]['started']).split('.')[0]
    return {"statuses": statuses, "info": info}


def delete_status(id):
    status = db_session.query(Status).filter(Status.id == id).one_or_none()
    if status is not None:
        logging.info('Deleting pet %s..', id)
        db_session.query(Status).filter(Status.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404


def view_status_rawlog(slot_no, slot, filename, info):
    testing_model = Testing()
    test = get_test_by_slot(slot_no)
    path = test['uut_log_dir']
    testing_model.root_path = test['code_from'], slot

    raw_logs_dir = 'Raw_logs'
    full_path = os.path.join(testing_model.getLogsPath, path, raw_logs_dir, filename + '.raw')
    data = ['File not found']
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='ISO-8859-1') as f:
            data = [i.strip() for i in f.readlines()]
    return data


def view_status_sequencelog(slot_no, slot, filename, info):
    testing_model = Testing()
    test = get_test_by_slot(slot_no)
    path = test['uut_log_dir']
    testing_model.root_path = test['code_from'], slot

    raw_logs_dir = 'Raw_logs'
    full_path = os.path.join(testing_model.getLogsPath, path, raw_logs_dir, filename + '.txt')
    data = ['File not found']
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='ISO-8859-1') as f:
            data = [i.strip() for i in f.readlines()]
    return data


def view_log_rawlog(filezip, filename):
    testing_model = Testing()
    folder = filezip.split('.')[0]
    raw_logs_dir = 'Raw_logs'
    full_path = os.path.join(testing_model.getViewLogPath, folder, raw_logs_dir, filename + '.raw')
    data = ['File not found']
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='ISO-8859-1') as f:
            data = [i.strip() for i in f.readlines()]
    return data


def view_log_sequencelog(filezip, filename):
    testing_model = Testing()
    folder = filezip.split('.')[0]
    raw_logs_dir = 'Raw_logs'
    full_path = os.path.join(testing_model.getViewLogPath, folder, raw_logs_dir, filename + '.txt')
    data = ['File not found']
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='ISO-8859-1') as f:
            data = [i.strip() for i in f.readlines()]
    return data


def get_test_by_slot(slot_no):
    test = db_session.query(Test).filter(Test.location == slot_no).one_or_none()
    return test.dump() or ('Not found', 404)


def get_testcaselist_by_slot(slot_no):
    test_cases = db_session.query(TestCaseList).filter(TestCaseList.slot_no == slot_no).all()
    return [i.test_case for i in test_cases]
