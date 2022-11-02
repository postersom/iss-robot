import logging
from libs.engine import utils
from libs.engine import odc
from libs.engine import constants as engine_constants
from libs import sequencer_definitions

LOG = logging.getLogger(__name__)

PASS = engine_constants.PASS
apdicts = utils.APDicts()
SequenceDefinition = sequencer_definitions.SequenceDefinition


def get_iss_info():
    """
    Returns an ISS Info object that contains information needed in a Verify-ODC.

    This returns data if called while running a Verify-ODC.

    The returned ISS Info object has the following attributes:
    - chassis_name : Name of the container if the container is not a super
    - code_from :
    - logop :
    - odc_type :
    - operation_id :
    - robot_path :
    - serial_number : The serial number associated with this container.
    - slot_location :
    - test_mode : 
    - test_station : The test station for this container if only 1 area is associated with it.

    :return dict:
    """
    return utils.get_iss_info()


def add_iss_data(serial_number, **kwargs):
    """Used to setup your DUT information in the pre-sequence or add data to a given serial number inside your sequence.

    This will set the specified data for the specified serial number (serial_number) to generate a TST record.

    Can be used to establish parent child geneology if the test record is a child, by specifying the parent.
        Basically this will call cesiumlib.register_genealogy function for you if not already done.
        Must give parent_serial_number, parent_product_id, serial_number, and product_id to do this.

    For ISS to start generating data correctly you need at least the following fields:
        serial_number: the serial number of the chassis/board/... (e.g "APO11011OPA")
        product_id: PID/Unit Under Test Type (e.g. "CISCO-2501")
        test_area: test area (e.g. "SYSFT")
        test_container: The container that will run the serial number when set from the pre-sequence.

    ISS will start sending your data to the DB from that point, with rectimes of the actual start time

    How to call the function:
    You may call with the key/value pairs in the call itself, or the key value pairs can be in a dict, or a mix of both
    For instance, the following examples are all equivalent; **a_dict in a call will be unrolled for add_tst_data
    In any case, 'serial_number' must be a key in the dict, or a key in the param list of the function call

    Main Example:   # all params are specified in the function call
    -   lib.add_iss_data(serial_number='FXXXXXXXXXX', part_number='R3153F110002015D', product_name='Miniphoton2')

    **Example:  # serial_number must be present in the dict (my_tst_data)
    -   my_tst_data = dict(serial_number='FXXXXXXXXXX', part_number='R3153F110002015D', product_name='Miniphoton2')
    -   lib.add_iss_data(**my_tst_data)

    Example with Geneology:
        lib.add_iss_data(serial_number='FXXXXXXXXXX', part_number='R3153F110002015D', product_name='Miniphoton2')

    It may be convenient to organize data into dicts and use those to call this function, rather than specifying
    each as a param in the function call

    Valid ISS data that can be added by the script:
        * serial_number: {'type': 'string'},
        * part_number:  {'type': 'string' },
        * product_reversion: {'type': 'string'},
        * shop_order: {'type': 'string'},
        * product_id: {'type': 'string'},
        * status: {'type': 'string', 'expected': 'OK,FAIL'},
        * error_message: {'type': 'string'},
        * product_name: {'type': 'string'},
    :param serial_number: The serial number you want to iss the data to
    :param kwargs: Can be key=value params or a dictionary of key=value that contains the field to set in TST.
    """
    return utils.add_iss_data(serial_number=serial_number, **kwargs)


def odcserver(ip, family, serial_number, timeout=60):
    """
    Param: ip: (str|list): ODC IP
           family: (str): ODC family
           serial_number: (str): Serial number UUT
           timeout: (inf): Default timeout request ODC (60)s

    Main Example:
        odc = lib.odcserver(ip, family, serial, timeout)
        odc.clear_ticket()
        odc.request_ticket()
        odc.get_ticket()
        odc.get_data_odc(profile)
        odc.get_current_station()
        odc.get_process_ticket(ticket)
        odc.put_data_odc(data)

    :return:
    """
    return odc.ODCServer(ip=ip, family=family, serial_number=serial_number, timeout=timeout)


def get_xml_data(serial_number, **keyword):
    """
    :param serial_number: Serial Number
    :param keyword:
    :return:
    """
    return utils.get_xml_data(serial_number=serial_number, **keyword)


def finalization():
    return utils.finalization()
