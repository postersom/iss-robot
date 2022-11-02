from database import db_session
from model.log import Log
from connexion import NoContent
import datetime
import logging
from controllers.status_controller import *
from model.swagger.testing import Testing 
from service.logging import Logging 

print_log = Logging()
test_model = Testing() 

def get_logs(limit):
    q = db_session.query(Log)
    return [p.dump() for p in q][:limit]


def get_log(id):
    log = db_session.query(Log).filter(
        Log.id == id).one_or_none()
    return log.dump() or ('Not found', 404)


def put_log(log):
    p = db_session.query(Log).filter(
        Log.id == log['id']).one_or_none()
    id = log['id']
    if p is not None:
        logging.info('Updating pet %s..', id)
        p.update(**log)
    else:
        logging.info('Creating pet %s..', id)
        log['created'] = datetime.datetime.now()
        db_session.add(Log(**log))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)


def delete_log(id):
    log = db_session.query(Log).filter(Log.id == id).one_or_none()
    if log is not None:
        logging.info('Deleting pet %s..', id)
        db_session.query(Log).filter(Log.id == id).delete()
        db_session.commit()
        return NoContent, 204
    else:
        return NoContent, 404
def view_all_log(sn):
    log_header = "[{}-{}]".format("Testing_Controller", "viewLog")
    print_log.info(log_header, "Welcome to view log: {}".format(sn))
    testing_model = Testing()
    tmpReturnError = "Cannot view log because"
    tmpReturnData = testing_model.return_data
    try:
        if sn and not sn == "":
            complete, message_or_data = testing_model.viewLog(sn)
        else:
            complete, message_or_data = testing_model.viewLog()
    except Exception as e:
        print_log.error(log_header, "Error view log with: {}".format(e))
        tmpReturnData["error"] = "{} error when get data of log: {}".format(tmpReturnError, e)
        return tmpReturnData, 401

    
    message_or_data = sorted(message_or_data, key=lambda i: i['start_time'], reverse=True) 
    if not complete:
        print_log.error(log_header, message_or_data)
        tmpReturnData["error"] = "{}: {}".format(tmpReturnError, message_or_data)
        return tmpReturnData, 401

    print_log.info(log_header, "Result: {}".format(message_or_data))
    
    tmpReturnData["data"] = message_or_data
    return tmpReturnData, 200
    
def view_log_with_filter(request_body):
    log_header = "[{}-{}]".format("Testing_Controller", "viewLog")
    testing_model = Testing()
    tmpReturnError = "Cannot view log because"
    tmpReturnData = testing_model.return_data
    tmp_filter = {
        "serial_number": None,
        "result": None,
        "start_time": None,
        "end_time": None
    }
    data = []
    if request_body.get("serial_number") and len(request_body.get("serial_number")) > 0:
        tmp_filter["serial_number"] = request_body.get("serial_number")
    if request_body.get("result") and len(request_body.get("result")) > 0:
        tmp_filter["result"] = request_body.get("result").lower()
    if request_body.get("start_time") and len(request_body.get("start_time")) > 0:
        tmp_filter["start_time"] = "{} 00:00:00".format(request_body.get("start_time"))
    if request_body.get("end_time") and len(request_body.get("end_time")) > 0:
        tmp_filter["end_time"] = "{} 23:59:59".format(request_body.get("end_time"))

    print(tmp_filter)
    complete, tmp_data = testing_model.viewLog()
    if request_body.get("sortby_date") and len(request_body.get("sortby_date")) > 0 :
        sorter = lambda i: i[request_body.get("sortby_date")]
    else:
        sorter = lambda i: i['start_time']

    if request_body.get("sortby_date_added") and len(request_body.get("sortby_date_added")) > 0 :
        if request_body.get("sortby_date_added") == "oldest":
            tmp_data = sorted(tmp_data, key=sorter, reverse=False)
        else:
            tmp_data = sorted(tmp_data, key=sorter, reverse=True)
    else:
        tmp_data = sorted(tmp_data, key=sorter, reverse=True)

    for tmp in tmp_data:
        if tmp_filter["serial_number"] is not None and not tmp_filter["serial_number"] in tmp["filename"]:
            continue
        if tmp_filter["result"] is not None and not tmp_filter["result"] in tmp["result"].lower():
            continue
        if tmp_filter["start_time"] is None and tmp_filter["end_time"] is None:
            pass
        elif tmp_filter["start_time"] is not None and tmp_filter["end_time"] is None:
            tmp_start = tmp_filter["start_time"].split(" ")[0]
            if not tmp_start in tmp["start_time"]:
                continue
        elif tmp_filter["end_time"] is not None and tmp_filter["start_time"] is None:
            tmp_end = tmp_filter["end_time"].split(" ")[0]
            if not tmp_end in tmp["end_time"]:
                continue
        else:
            print(tmp["start_time"] < tmp_filter["start_time"])
            print(tmp["end_time"] > tmp_filter["end_time"])
            if tmp["start_time"] < tmp_filter["start_time"] or tmp["start_time"] >= tmp_filter["end_time"]:
                continue

        data.append(tmp)

    tmpReturnData["data"] = data
    return tmpReturnData, 200

def get_path_log():
    global test_model
    return test_model.getArchivePath
