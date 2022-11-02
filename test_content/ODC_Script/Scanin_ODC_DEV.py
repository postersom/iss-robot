import sys
import json
import xml.etree.ElementTree as ET
import ssl
import urllib.request 


def main():
    if(len(sys.argv) > 1): 
        input = json.loads(sys.argv[1])
        snpass = input["serial_number"].split('snpass')
        snfail = input["serial_number"].split('snfail')
        snsync = input["serial_number"].split('sync')
        if(input["serial_number"] == 'pass'):
            response = {
                "serial_number": "CF2SZ183400021",
                "part_number": "ABC1235",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "1234ABC",
                "status": "OK",
                "error_message": "TEST PASS "
            }
        elif(input["serial_number"] == 'fail'):
            response = {
                "serial_number": "CF2SZ183400021",
                "part_number": "ABC1235",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "1234ABC",
                "status": "FAIL",
                "error_message": "Fail Message"
            }
        elif(input["serial_number"] == 'warning'):
            response = {
                "serial_number": "CF2SZ183400021",
                "part_number": "ABC1235",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "1234ABC",
                "status": "WARNING",
                "error_message": "WARNING Message"
            }
        elif input["serial_number"] == 'interact':
            response = {
                "serial_number": "interact",
                "part_number": "userinteraction",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "TEST",
                "status": "OK",
                "error_message": "interact"
            }

        elif len(snsync) > 1:
            suffix = int(snsync[1])
            if suffix % 2 == 0:
                number = 1
            else:
                number = 2
            response = {
                "serial_number": "sync"+str(number),
                "part_number": "sync",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "1234ABC",
                "status": "OK",
                "error_message": "-"
            }
        # elif input["serial_number"] == 'sync2':
        #     response = {
        #         "serial_number": "sync2",
        #         "part_number": "sync",
        #         "product_reversion": "rev01",
        #         "shop_order": "P2",
        #         "product_id": "1234ABC",
        #         "status": "OK",
        #         "error_message": "sync2"
        #     }
        elif input["serial_number"] == 'F01DUMMYSN003':
            tree = ET.parse(urllib.request.urlopen('https://10.196.100.17/des/f5/getparameter.asp?profile=sn_prop&sn=' +
                                                   input["serial_number"], context=ssl._create_unverified_context()))
            root = tree.getroot()
            sn = root.attrib['SN']
            data = {'sn': sn}
            for child in root:
                data[child.tag] = child.text
            response = {
                "serial_number": data["sn"],
                "part_number": data["PN"],
                "product_reversion": "rev"+data["REVISION"],
                "shop_order": data["SO"],
                "product_id": data["PRODUCTID"],
                "status": "OK",
                "error_message": "-"
            }
        elif len(snpass) > 1:
            suffix = int(snpass[1])
            if 1 <= suffix <= 20:
                minute = 0.5
            elif 21 <= suffix <= 40:
                minute = 1
            elif 41 <= suffix <= 60:
                minute = 2
            elif 61 <= suffix <= 80:
                minute = 5
            elif 81 <= suffix <= 100:
                minute = 10
            response = {
                "serial_number": input["serial_number"],
                "part_number": "test_script_pass",
                "product_reversion": "rev01",
                "shop_order": str(minute)+"_minutes",
                "product_id": "1234ABC",
                "status": "OK",
                "error_message": "-"
            }
        elif len(snfail) > 1:
            suffix = int(snfail[1])
            if 1 <= suffix <= 20:
                minute = 0.5
            elif 21 <= suffix <= 40:
                minute = 1
            elif 41 <= suffix <= 60:
                minute = 2
            elif 61 <= suffix <= 80:
                minute = 5
            elif 81 <= suffix <= 100:
                minute = 10
            response = {
                "serial_number": input["serial_number"],
                "part_number": "test_script_fail",
                "product_reversion": "rev01",
                "shop_order": str(minute)+"_minutes",
                "product_id": "1234ABC",
                "status": "OK",
                "error_message": "-"
            }
        else:
            response = {
                "serial_number": "CF2SZ183400021",
                "part_number": "ABC1234",
                "product_reversion": "rev01",
                "shop_order": "P1",
                "product_id": "1234ABC",
                "status": "OK",
                "error_message": "FAIL PASS"
            }

    return json.dumps(response)


if __name__ == '__main__':
    print(main())
