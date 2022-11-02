import urllib3
import xmltodict
import logging
import re

logging.basicConfig(filename='/tmp/myapp.log', filemode='w', level=logging.DEBUG,
                    format='[%(asctime)s]: %(levelname)-7s : %(message)s')


class ODCServer(object):
    def __init__(self, ip, family, serial_number, timeout=60):
        self.http = urllib3.PoolManager(timeout=timeout)
        self.ip = ip if isinstance(ip, list) else [ip]
        self.family = family
        self.serial_number = serial_number
        self.get_data = ''

    def request_data(self, url):
        try:
            for ip in self.ip:
                req = self.http.request('GET', f'http://{ip}/des/{self.family}/{url}', preload_content=False)
                if req.status == 200:
                    return req.data.decode('utf-8')
            return False
        except Exception as err:
            logging.error(err, exc_info=True)
            raise Exception(err)

    def clear_ticket(self):
        tk = self.get_ticket()
        self.get_data = self.request_data(f'clearticket.asp?SN={self.serial_number}&ticket={tk}')
        return self.get_data

    def request_ticket(self):
        self.get_data = self.request_data(f'getticket.asp?SN={self.serial_number}')
        return self.get_data

    def get_ticket(self):
        self.get_data = self.request_data(f'getparameter.asp?SN={self.serial_number}&profile=ticket')
        return self.get_data

    def get_data_odc(self, profile, serial_number=None):
        self.get_data = dict()
        serial_number = serial_number if serial_number else self.serial_number
        for i in profile if isinstance(profile, list) else [profile]:
            data_odc = ''
            try:
                data_odc = self.request_data(f'getparameter.asp?profile={i}&SN={serial_number}')
                data_odc = xmltodict.parse(data_odc)
                for k, v in data_odc['Parameter'].items():
                    v = re.sub(r'-', '', str(v))
                    v = v.split(',') if ',' in v else v
                    data_odc['Parameter'].update({k: None if isinstance(v, str) and v in ['None'] else v})
                self.get_data.update(**data_odc['Parameter'])
            except xmltodict.expat.ExpatError:
                self.get_data = data_odc
        return self.get_data

    def get_current_station(self):
        self.get_data = self.request_data(f'check.asp?SN={self.serial_number}')
        return self.get_data

    def get_process_ticket(self, ticket):
        self.get_data = self.request_data(f'process.asp?ticket={ticket}&process=true')
        return self.get_data

    def put_data_odc(self, data):
        try:
            for ip in self.ip:
                req = self.http.request('POST', f'http://{ip}/des/{self.family}/result.asp', body=data,
                                        headers={'Content-Type': 'text/xml'})
                if req.status == 200:
                    return req.data.decode('utf-8')
            return False
        except Exception as err:
            logging.error(err, exc_info=True)
            raise Exception(err)

