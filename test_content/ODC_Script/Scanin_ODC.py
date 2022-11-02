import sys
import json
import configparser
from ODCServer import ODCServer
import ssl
import urllib.request
import xml.etree.ElementTree as ET
import os
import re
import logging
import platform

main_path = "/opt/Robot/"
bom_path = "{}ODC_Script/BOM/".format(main_path)
temp_logs_path = "/tmp/"

if platform.system() == "Linux":
    # linux 
    main_path = "/opt/Robot/"
    bom_path = "{}ODC_Script/BOM/".format(main_path)
    temp_logs_path = "/tmp/"

elif platform == "Darwin":
    # OS X
    main_path = "/opt/Robot/"
    bom_path = "{}ODC_Script/BOM/".format(main_path)
    temp_logs_path = "/tmp/"

elif platform.system() == "Windows":
    # Windows...
    main_path = "C:\\Robot\\"
    bom_path = "{}ODC_Script\\BOM\\".format(main_path)
    temp_logs_path = "C:\\"

else:
    main_path = "/opt/Robot/"
    bom_path = "{}ODC_Script/BOM/".format(main_path)
    temp_logs_path = "/tmp/"


logging.basicConfig(filename='{}myapp.log'.format(temp_logs_path), level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


def main():
    try:
        if(len(sys.argv) > 1):
        #if(len("sys.argv") > 1):
            input_data = json.loads(sys.argv[1])
            #input_data = {"serial_number": "F0A1119110003",
            #              "odc_type": "verify"}

            tags_sn = {"SN": "odc_sn",
                    "PN": "odc_pn",
                    "REVISION": "odc_revision",
                    "SO": "odc_so",
                    "PRODUCTID": "odc_pro_id"}

            tags_bom = {"PRODUCT_PART_NUMBER": "odc_pro_pn",
                    "PRODUCTION_STATE": "odc_pro_state",
                    "PRODUCT_VERSION": "odc_pro_version",
                    "PCB_MANUFACTURE": "odc_pcb_mfg",
                    "SCM_PCBA_SN": "odc_scm_pcba_sn",
                    "FAN_1": "odc_fan1",
                    "FAN_2": "odc_fan2",
                    "FAN_3": "odc_fan3",
                    "FAN_4": "odc_fan4",
                    "FCM": "odc_fcm",
                    "PDB1": "odc_pdb1",
                    "PDB2": "odc_pdb2",
                    "RACK_MON": "odc_rack_mon",
                    "SCM": "odc_scm",
                    "SMB": "odc_smb",
                    "SSD_1": "odc_ssd1",
                    "SSD_2": "odc_ssd2",
                    "MACID": "odc_mac_id",
                    "MAC_COM_E": "odc_mac_com_e",
                    "PRODUCT_ASSET_TAG": "odc_pro_ass_tag"}

            
            config = configparser.ConfigParser()
            config.read(main_path+'/ODC_Script/ODC_Config.cfg')
            section = config['DEFAULT']
            odc_status = False
            odc = None

            #Check ODC conecting
            for i in range(0, 3):
                odc = ODCServer(section['Primary_ODC_IP'],
                                section['Business_Unit'])
                odc.connect()

                # True = ODC Online / False = ODC Down
                odc_status = odc.check_connection(profile=section['Bom_Profile'])

                if odc_status:
                    break

            # try connect to secondary ODC server.
            if not odc_status:

                for sec_url in section['Secondary_ODC_IP'].split(','):
                    for i in range(0, 3):
                        odc = ODCServer(sec_url,
                                        section['Business_Unit'])
                        odc.connect()
                        odc_status = odc.check_connection(
                                     profile=section['Bom_Profile'])
                        if odc_status:
                            break

                    if  odc_status:
                        break

                if not odc_status:
                    response = {
                        "serial_number": input_data["serial_number"],
                        "part_number": "",
                        "product_reversion": "",
                        "shop_order": "",
                        "product_id": "",
                        "status": "FAIL",
                        "error_message": "Cannot connect to ODC server of "
                                         "Primary IP : {} and "
                                         "Secondary IP : {}".format(
                            section['Primary_ODC_IP'],
                            section['Secondary_ODC_IP'])
                    }

                    return json.dumps(response)

            '''
            #Check the test current station
            station_ids = ""
            if  input_data["test_station"] == "System-Test":
                station_ids = section['current_sys']
            elif input_data["test_station"] == "Burn-In":
                station_ids = section['current_bi']
            elif input_data["test_station"] == "Final":
                station_ids = section['current_ft']
            elif input_data["test_station"] == "ESS":
                station_ids = section['current_ess']
            elif input_data["test_station"] == "Pre-RDT":
                station_ids = section['current_rdt']
            elif input_data["test_station"] == "Hi-Pot":
                station_ids = section['current_hp']
            else:
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "Not found the station name in list"
                }

                return json.dumps(response)

            current_station = odc.get_current_station(input_data["serial_number"]).decode("utf-8")
            '''
            '''
            if not station_ids in current_station:
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "{} is incorrect station expect {} but "
                                     "got {}.".format(input_data["serial_number"],
                                                      station_ids, current_station)
                }

                return json.dumps(response)
            '''

            data = ""

            if os.path.isfile('{}{}.py'.format(bom_path, input_data["serial_number"])):
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "Duplicate serial number testing file config."
                }

                return json.dumps(response)

            response = {
                "serial_number": "",
                "part_number": "",
                "product_reversion": "",
                "shop_order": "",
                "product_id": "",
                "status": "FAIL",
                "error_message": "-----------"
            }

            '''
            #Request ticket number
            ticket = odc.request_ticket(input_data["serial_number"]).decode("utf-8")
            if "working" in ticket:
                oldTicket = odc.get_ticket(input_data["serial_number"]).decode("utf-8")
                if odc.clear_ticket(input_data["serial_number"], oldTicket):
                    ticket = odc.request_ticket(input_data["serial_number"]).decode("utf-8")
                    
                    with open("{}{}.py".format(bom_path, input_data["serial_number"]),
                              "a+") as save_data:
                        save_data.write('ticket_number = "{}"\n'.format(ticket))
                    
                else:
                    response = {
                        "serial_number": input_data["serial_number"],
                        "part_number": "",
                        "product_reversion": "",
                        "shop_order": "",
                        "product_id": "",
                        "status": "FAIL",
                        "error_message": "Failed to clear ticket on the ODC System"
                    }

                    return json.dumps(response)
                    

            elif "not exist" in ticket:
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "Cannot get ticket number (not exist)."
                }

                return json.dumps(response)
            
            elif "not in process" in ticket:
                
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "Cannot get ticket number (not in process)."
                }

                return json.dumps(response)

            elif re.search('^[0-9]{17}$', ticket):

                pass
               
            else:
                response = {
                    "serial_number": input_data["serial_number"],
                    "part_number": "",
                    "product_reversion": "",
                    "shop_order": "",
                    "product_id": "",
                    "status": "FAIL",
                    "error_message": "Cannot get ticket number (Empty)."
                }

                return json.dumps(response)    
                '''

            for num in range(0, 2):
                if num:
                    data = odc.get_profile_parameter(input_data["serial_number"],
                                                     section['Bom_Profile'])
                    tags = tags_bom
                else:
                    data = odc.get_profile_parameter(input_data["serial_number"],
                                                     section['SN_Profile'])
                    tags = tags_sn

                if 'Not found Shop Order of' in str(data):
                    response = {
                        "serial_number": input_data["serial_number"],
                        "part_number": "",
                        "product_reversion": "",
                        "shop_order": "",
                        "product_id": "",
                        "status": "FAIL",
                        "error_message": "Not found Shop Order"
                    }

                    return json.dumps(response)


                root = ET.fromstring(data)
                sn = root.attrib['SN']
                data = {'SN': sn}
                for child in root:
                    data[child.tag] = child.text

                for key, val in tags.items():

                    if input_data["odc_type"] == "test":
                        with open("{}{}.py".format(bom_path, input_data["serial_number"]),
                                 "a+") as save_data:
                            save_data.write('{} = "{}"\n'.format(val,
                                      data['{}'.format(key)]))

                    if not num:
                        response = {
                            "serial_number": data['SN'],
                            "part_number": data['PN'],
                            "product_reversion": "rev{}".format(data['REVISION']),
                            "shop_order": data['SO'],
                            "product_id": data['PRODUCTID'],
                            "status": "OK",
                            "error_message": "-"
                        }

            return json.dumps(response)

        else:
            response = {
                "serial_number": "",
                "part_number": "",
                "product_reversion": "",
                "shop_order": "",
                "product_id": "",
                "status": "FAIL",
                "error_message": "Not found argument to ODC script test."
            }

            return json.dumps(response)

    except Exception as err:
        logger.error(err)
        response = {
            "serial_number": "",
            "part_number": "",
            "product_reversion": "",
            "shop_order": "",
            "product_id": "",
            "status": "FAIL",
            "error_message": "Error in ODC script test, Please inform developer for fix issue."
        }

        return json.dumps(response)

if __name__ == '__main__':
    print(main())
 