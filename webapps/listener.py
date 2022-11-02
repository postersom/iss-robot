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
outfile = open(outpath, 'w')
outfile.close()


def sending_status(status, message, test_location, test_id):
    conn = http.client.HTTPConnection(STATUS_UPDATE_API_URL)
    payload = {
        "test_id": test_id,
        "message": message,
        "status": status,
        "test_location": test_location}
    headers = {'content-type': "application/json"}
    conn.request("PUT", "/api/statuses", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()


def start_suite(name, attrs):
    outfile = open(outpath, 'a')
    outfile.write("%s Location:%s '%s' Total cases=%d\n" %
                  (name, attrs['metadata']['Location'], attrs['doc'], attrs['totaltests']))
    outfile.close()
    sending_status('start_suite', "%s Location:%s '%s' Total cases=%d" % (
        name, attrs['metadata']['Location'], attrs['doc'], attrs['totaltests']), attrs['metadata']['Location'], 0)


def start_test(name, attrs):
    outfile = open(outpath, 'a')
    tags = attrs['tags'][0]
    outfile.write("- %s '%s' [Location: %s ] :: " % (name, attrs['doc'], tags))
    outfile.close()
    print(attrs)
    sending_status('start_test', "%s" % (name), tags, 0)


def end_test(name, attrs):
    outfile = open(outpath, 'a')
    tags = attrs['tags'][0]
    if tags == 'robot:exit':
        tags = attrs['tags'][1]
    outfile.write('Tags : %s\n' % tags)
    if attrs['status'] == 'PASS':
        outfile.write('PASS\n')
        sending_status('end_test', "Result:%s" % attrs['status'], tags, 0)
    else:
        outfile.write('FAIL: %s\n' % attrs['message'])
        if attrs['message'] == 'Execution terminated by signal':
            sending_status('end_test', "Result:%s %s " %
                           ('ABORT', attrs['message']), tags, 0)
            outfile.write('ABORT: %s\n' % attrs['message'])
        else:
            sending_status('end_test', "Result:%s %s " %
                           (attrs['status'], attrs['message']), tags, 0)
            outfile.write('FAIL: %s\n' % attrs['message'])
    outfile.close()
    print(attrs)


def end_suite(name, attrs):
    outfile = open(outpath, 'a')
    outfile.write('%s\n%s\n' % (attrs['status'], attrs['message']))
    outfile.close()
    sending_status('end_suite', "Result:%s" %
                   (attrs['status']), attrs['metadata']['Location'], 0)
