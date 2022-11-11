import os.path
import tempfile
import http.client
import urllib.parse
import json
from datetime import datetime
import platform
import os

main_path = "/opt/Logs_Robot"

if platform.system() == "Linux":
    # linux
    main_path = "/opt/Logs_Robot"

elif platform.system() == "Windows":
    # Windows...
    main_path = "C:\\Logs_Robot"


ROBOT_LISTENER_API_VERSION = 2
STATUS_UPDATE_API_URL = '127.0.0.1:'+os.getenv('PORT')


outpath = os.path.join(main_path, 'progress.txt')


def sending_status(status, message, test_location, test_id):
    conn = http.client.HTTPConnection(STATUS_UPDATE_API_URL)
    payload = {
        "test_id": test_id,
        "message": message,
        "status": status,
        "test_location": test_location}
    headers = {'content-type': "application/json"}
    conn.request("PUT", "/api/statuses", json.dumps(payload), headers)
    conn.getresponse().read()
    conn.close()


def start_suite(name, attrs):
    with open(outpath, 'a') as f:
        f.write(f"{name} Location:{attrs['metadata']['Location']} '{attrs['doc']}' Total cases={attrs['totaltests']}\n")
    sending_status('start_suite', f"{name} Location:{attrs['metadata']['Location']} '{attrs['doc']}' Total cases={attrs['totaltests']}",
                   attrs['metadata']['Location'], 0)


def start_test(name, attrs):
    with open(outpath, 'a') as f:
        tags = attrs['tags'][0]
        f.write(f"- {name} '{attrs['doc']}' [Location: {tags} ] :: ")
        sending_status('start_test', name, tags, 0)


def end_test(name, attrs):
    with open(outpath, 'a') as f:
        tags = attrs['tags'][0]
        if tags == 'robot:exit':
            tags = attrs['tags'][1]
        f.write('Tags : %s\n' % tags)
        if attrs['status'] == 'PASS':
            f.write('PASS\n')
            sending_status('end_test', f"Result:{attrs['status']}", tags, 0)
        else:
            f.write('FAIL: %s\n' % attrs['message'])
            if attrs['message'] == 'Execution terminated by signal':
                sending_status('end_test', f"Result:{'ABORT'} {attrs['message']}", tags, 0)
                f.write(f"ABORT: {attrs['message']}\n")
            else:
                sending_status('end_test', f"Result:{attrs['status']} {attrs['message']}", tags, 0)
                f.write(f"FAIL: {attrs['message']}\n")


def end_suite(name, attrs):
    with open(outpath, 'a') as f:
        f.write(f"{attrs['status']}\n{attrs['message']}\n")
    sending_status('end_suite', f"Result:{attrs['status']}", attrs['metadata']['Location'], 0)
