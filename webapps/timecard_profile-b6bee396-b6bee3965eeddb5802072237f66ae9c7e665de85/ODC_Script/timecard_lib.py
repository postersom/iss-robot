import json
import logging
import os
import getpass
import socket
import re
from datetime import datetime
from libs import lib
from libs.lib import PASS

LOG = logging.getLogger(__name__)


def iss_info():
    userdict = lib.apdicts.userdict
    userdict['PATH'] = '/opt/Robot/BOM/'
    info = lib.get_iss_info()
    if info:
        [LOG.debug(f'ISS Info: {k} = {v}') for k, v in sorted(info.items())]
        userdict.update(**info)
        userdict['ODC'] = lib.odcserver(ip=['10.196.28.117', '10.196.100.17'],
                                        family='f5',
                                        serial_number=userdict['serial_number'])
        return PASS
    return 'Not Found Argument to ODC Script Test.'


def get_data_odc():
    userdict = lib.apdicts.userdict
    data_odc = dict()
    if userdict['logop'] in ['FCT']:
        data = userdict['ODC'].get_data_odc(profile='TC_BFT_INFO')
        data_odc.update(data) if isinstance(data, dict) else data_odc.clear()
    else:
        data = userdict['ODC'].get_data_odc(profile='TC_INFO')
        data_odc.update(data) if isinstance(data, dict) else data_odc.clear()
        data = userdict['ODC'].get_data_odc(profile='TC_BFT_INFO',
                                            serial_number=re.sub(r'^(F)(.{4})(.{4})', r'\1-\2-\3', data_odc['TC_SN']))
        if 'Not found Shop Order' in data:
            data = userdict['ODC'].get_data_odc(profile='TC_BFT_INFO',
                                                serial_number=re.sub(r'^(F)(.{4})(.{4})', r'\1\2-\3', data_odc['TC_SN']))
        data_odc.update(data) if isinstance(data, dict) else data_odc.clear()

    if data_odc and isinstance(data_odc, dict):
        [LOG.debug(f'ODC Data: {k} = {v}') for k, v in sorted(data_odc.items())]
        userdict['data_odc'] = data_odc
        return PASS
    return 'Can not Get Data ODC, Please Check ODC Server'


def check_station():
    userdict = lib.apdicts.userdict
    station = {'622300': 'FCT',
               '622001': 'ST',
               '622240': 'FST',
               '622220': 'RDT',
               '622002': 'HP',
               '622200': 'BI',
               '622021': 'PTP'}
    data_odc = userdict['ODC'].get_current_station()
    if userdict['logop'] == station[data_odc]:
        return PASS
    return f'UUT Wrong Station, Correct Station: [ {data_odc} ]'


def request_ticket():
    userdict = lib.apdicts.userdict
    for _ in range(3):
        if not userdict['ODC'].clear_ticket():
            break
    for _ in range(3):
        if re.search(r'^\d{17}$', userdict['ODC'].request_ticket()):
            break
    ticket = userdict['ODC'].get_ticket()
    if ticket:
        LOG.debug(f'Ticken: [ {ticket} ], PASSED')
        return PASS
    return 'Warning: System Cannot Request Ticken Number'


def check_ticket():
    userdict = lib.apdicts.userdict
    for i in range(1, 4):
        ticket = userdict['ODC'].get_ticket()
        if ticket:
            LOG.debug(f'Ticken: [ {ticket} ]')
            userdict['TICKET'] = ticket
            return PASS
        LOG.error(f'Error Ticket: {i}')
        request_ticket()
    return 'Warning: System Cannot Request Ticken Number'


def create_bom():
    userdict = lib.apdicts.userdict
    with open(f"{userdict['PATH']}/{userdict['serial_number']}.json", 'w') as fp:
        json.dump(userdict['data_odc'], fp, sort_keys=True)
    return PASS


def add_iss_data():
    userdict = lib.apdicts.userdict
    part_number = 'Orolia'
    if userdict['logop'] in ['FCT'] or re.search(r'^SG.+', userdict['data_odc']['TC_SN']):
        part_number = 'Timecard'
    lib.add_iss_data(serial_number=userdict['serial_number'],
                     part_number=part_number,
                     product_name='Timecard')
    return PASS


# Scan-Out ....................................................................................
def get_xml_data():
    userdict = lib.apdicts.userdict
    start = datetime.strptime(userdict['start_time'], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(userdict['end_time'], '%Y-%m-%d %H:%M:%S')
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    parameters = {'cth_ip': ip,
                  'login_name': getpass.getuser(),
                  'logop': userdict['logop'],
                  'test_slot': userdict['slot_location'],
                  'script_version': userdict['release_version'],
                  'start_time': str(start),
                  'end_time': str(end),
                  'test_time': str(end - start),
                  'view_log': f"http://{ip}:8080/log/{userdict['log_name']}.zip",
                  'download_log': f"http://{ip}:8080/log/download/{userdict['log_name']}.zip"
                  }
    if userdict['result'] in ['F']:
        parameters.update({'failure_step_log': f"http://{ip}:8080/log/{userdict['log_name']}.zip/view/{userdict['test_fail']}"})
    if userdict['logop'] in ['ST']:
        with open(f"/opt/Robot/BOM/{userdict['serial_number']}.json", 'r') as f:
            bom = json.loads(f.read())
        parameters.update({**bom['ISS_DATA']})
    userdict['XML_Data'] = lib.get_xml_data(serial_number=userdict['serial_number'],
                                            station=userdict['ODC'].get_current_station(),
                                            testername=hostname,
                                            user=userdict['operation_id'],
                                            ticket=userdict['TICKET'],
                                            result=userdict['result'],
                                            parameter=parameters,
                                            test_fail=userdict['test_fail'],
                                            message_fail=userdict['message_fail'])

    return PASS


def put_data():
    userdict = lib.apdicts.userdict
    if 'SUCCESS' in userdict['ODC'].put_data_odc(userdict['XML_Data']):
        if 'SUCCESS' in userdict['ODC'].get_process_ticket(userdict['TICKET']):
            return PASS
    return 'Warning: Can not Put data ODC'


def remove_bom():
    userdict = lib.apdicts.userdict
    bom = f"{userdict['PATH']}/{userdict['serial_number']}.json"
    os.remove(bom) if os.path.isfile(bom) else None
    return PASS


def finalization():
    lib.finalization()
    return PASS
