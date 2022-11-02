import sys
import json
import logging
import xmltodict

logging.basicConfig(filename='/tmp/myapp.log', filemode='w', level=logging.DEBUG,
                    format='[%(asctime)s]: %(levelname)-7s : %(message)s')


class APDicts:
    userdict = dict()


def get_iss_info():
    return json.loads(sys.argv[1]) if len(sys.argv) > 1 else ''


def add_iss_data(serial_number: str, product_name: str, part_number: str, product_rev='', shop_order='',
                 product_id=''):
    """
    :param serial_number:
    :param product_name:
    :param part_number:
    :param product_rev:
    :param shop_order:
    :param product_id:
    :return:
    """
    response = {'error_message': '-',
                'part_number': part_number,
                'product_id': product_id,
                'product_name': product_name,
                'product_reversion': product_rev,
                'serial_number': serial_number,
                'shop_order': shop_order,
                'status': 'OK'}
    return print(json.dumps(response))


def get_xml_data(serial_number: str, station: str, testername: str, user: str, ticket: str, result: str,
                 description='-', parameter=None, test_fail=None, message_fail=None):
    """
    :param serial_number:
    :param station:
    :param testername:
    :param user:
    :param ticket:
    :param result:
    :param description:
    :param parameter:
    :param test_fail:
    :param message_fail:
    :return:
    """
    xml = {'ticket': ticket,
           'sn': serial_number,
           'station': station,
           'testername': testername,
           'user': user,
           'result': result,
           'description': description}
    xml.update({'parameter': {'par': [{'@name': k, '#text': v} for k, v in parameter.items()]}}) if parameter else None
    xml.update({'failure': {'failcode': {'@name': test_fail, 'description': message_fail}}}) if test_fail else None
    logging.debug(f"XML Data: \n\n{xmltodict.unparse({'test': xml}, pretty=True)}\n")
    return xmltodict.unparse({'test': xml})


def finalization():
    """
    :return:
    """
    response = {'status': 'OK',
                'product_name': '',
                'error_message': '-'}
    return print(json.dumps(response))

