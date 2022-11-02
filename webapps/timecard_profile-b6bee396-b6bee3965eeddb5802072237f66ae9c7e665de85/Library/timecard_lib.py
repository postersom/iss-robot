import re
import time
import json
import os
import sys
import matplotlib.pyplot as plt
from datetime import datetime
from prettytable import PrettyTable
from robot.libraries.BuiltIn import BuiltIn


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


from iss_libs.libs import lib
from iss_libs.libs.lib import iss_service
from iss_libs.libs.lib import log


@iss_service
def iss_info():
    userdict = lib.apdicts.userdict
    userdict.update(lib.get_variables)
    with open(f"/opt/Robot/BOM/{userdict['${serial_number}']}.json", 'r') as f:
        userdict.update(json.loads(f.read()))

    # HPE
    userdict['HPE_BIOS'] = 'U30_2.58_11_24_2021.fwpkg'
    userdict['HPE_CPLD'] = 'CPLD_DL360_DL380_Gen10_VP1_v3232.fwpkg'
    userdict['HPE_iLo'] = 'ilo5_260.fwpkg'
    userdict['HPE'] = {'Model': r'HPE\s+ProLiant\s+DL380\s+Gen10',
                       'CPU': r'Intel\(R\)\s+Xeon\(R\)\s+Gold\s+6138\s+CPU\s+@\s+2\.00GHz',
                       'Bios': r'U30\s+v2.58\s+\(11/24/2021\)',
                       'iLO': '2.60',
                       'CPLD': '0x32',
                       'TPM': '73.20'}

    # Timecard Orolia
    userdict['Oscillatord_Ver'] = '3.3.9'
    userdict['Orolia_FPGA_Ver'] = '0.0.15'
    userdict['Orolia_FW_FPGA'] = 'art_card_v15_usb.rpd'

    # Timecard Meta
    userdict['Meta_FPGA_Ver'] = '0x800A'
    userdict['Meta_FW_FPGA'] = 'TimeCardProduction800A.bin'
    userdict['MAC_Ver'] = '1.0.23'

    # Timecard Driver
    userdict['Timecard_DRV'] = 'TimeCard_V25'

    # Oscillatord RPM
    userdict['RPM_Oscillatord'] = {'oscillatord': 'oscillatord-3.3.9-2.el8.x86_64.rpm',
                                   'disciplining': 'liboscillator-disciplining-3.3.9-2.el8.x86_64.rpm',
                                   'ublox': 'ubloxcfg-1.13-2.20220420gita46d97c.el8.x86_64.rpm'}

    userdict['Oscillatord'] = {'oscillatord': '3.3.9-2.el8',
                               'liboscillator-disciplining': '3.3.9-2.el8',
                               'ubloxcfg': '1.13-2.20220420gita46d97c.el8'}

    # Mellanox NIC
    if userdict['${SUITE_NAME}'] not in ['FCT']:
        if userdict['NIC_MFG_PN'] in ['MCX623106PCCDAT']:
            userdict['FW_Mellanox'] = 'fw-ConnectX6Dx-rel-22_31_1550-MCX623106PC-CDA_Ax-UEFI-14.24.13-' \
                                      'FlexBoot-3.6.403.signed.bin'
            userdict['Mellanox'] = {'FW': '22.31.1550',
                                    'PXE': '3.6.0403',
                                    'UEFI': '14.24.0013'}

        elif userdict['NIC_MFG_PN'] in ['MCX623106TCCDAT']:
            userdict['FW_Mellanox'] = 'fw-ConnectX6Dx-rel-22_31_1550-MCX623106TC-CDA_Ax-UEFI-14.24.13-' \
                                      'FlexBoot-3.6.403.signed.bin'
            userdict['Mellanox'] = {'FW': '22.31.1550',
                                    'PXE': '3.6.0403',
                                    'UEFI': '14.24.0013'}
        else:
            lib.fail()

    # BIOS setting python scritp name
    userdict['Python_Bios_Script'] = 'bios-script-v5_S2.py'

    # .............................................................
    userdict['TimeCard'] = r'\[root\@localhost'
    userdict['Server'] = r'timecard\@CTHFB\d+'
    userdict['TC_I2C'] = '13' if userdict['${SUITE_NAME}'] in ['FCT'] else '1'
    userdict['Diag_Ver'] = '1.1.1'
    # .............................................................

    [log.debug(f'{k:<30}: {v}') for k, v in userdict.items()]


@iss_service
def power_control(control: str):
    psu = lib.getconnections()['WTI']
    p = lib.PowerControlHandler(driver=psu.model, connection=psu, port=psu.plug, timeout=10)
    if control == 'on':
        p.on()
    elif control == 'off':
        p.off()
    elif control == 'cycle':
        p.cycle(time_sleep=10)


@iss_service
def connection_check():
    with lib.getconnections()['Server'] as server:
        server.send(f"ping {lib.getconnections()['TimeCard'].host} -i 30\r", expectphrase=r'ttl=\d+', timeout=600,
                    wait_before_send=60)


@iss_service
def hpe_server_info():
    with ilorest() as hpe:
        hpe.system()
        hpe.processors()
        hpe.memory()
        hpe.firmware()


@iss_service
def hpe_fru_info():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('lsblk -S | grep ATA | cat\r', expectphrase=userdict['TimeCard'])
        if result := re.search(r'(sd[a-z]).+', tc.recbuf):
            disk = result.group(1)
            tc.send(f'smartctl -i /dev/{disk}\r', expectphrase=userdict['TimeCard'],
                    check_received_string=[r'Device\s+Model:\s+MK000480GWSSC', r'User\s+Capacity:.+\[480\s+GB\]'])
            if result := re.search(r'Serial Number:\s+(\S+)', tc.recbuf):
                add_iss_data(hdd_serial_number=result.group(1))
                tc.send(f'smartctl -H /dev/{disk}\r', expectphrase=userdict['TimeCard'],
                        check_received_string=r'SMART\s+overall\-health\s+self\-assessment\s+test\s+result:\s+PASSED')
    lib.fail() if not result else None
    with ilorest() as hpe:
        hpe.power()
        hpe.fan()


@iss_service
def hpe_thermals_health():
    with ilorest() as hpe:
        hpe.thermals()


@iss_service
def hpe_mac_address():
    with ilorest() as hpe:
        hpe.macaddress()


@iss_service
def hpe_bios_ilo_and_cpld_fw_update():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('cd /root/firmware/hpe/\r', expectphrase=userdict['TimeCard'],
                check_not_received_string='No such file or directory')
        for i, (fw, file) in enumerate([('BIOS', userdict['HPE_BIOS']),
                                        ('CPLD', userdict['HPE_CPLD']),
                                        ('iLO FW', userdict['HPE_iLo'])]):

            log.message(f'\r{f" HPE {fw} Update [ {file} ]":*^100}')
            tc.send(f'ilorest flashfwpkg {file}\r', expectphrase=[r'\(y/n\)', userdict['TimeCard']], timeout=1200)
            tc.send('y\r', expectphrase=userdict['TimeCard'], timeout=1200) if '(y/n)' in tc.recbuf else None

            crs = r'Firmware\s+has\s+successfully\s+been\s+flashed\s+and\s+a\s+reboot\s+' \
                  r'is\s+required\s+for\s+this\s+firmware\s+to\s+take\s+effect'
            if i == 2:
                crs = r'iLO\s+will\s+reboot\s+to\s+complete\s+flashing\.\s+Session\s+will\s+be\s+terminated'
            lib.fail() if not tc.check_received_string(crs) else None
        tc.send('reboot\r')
        time.sleep(5)


@iss_service
def hpe_asset_tag_check():
    with ilorest() as hpe:
        hpe.assettag()


class ilorest(object):
    def __init__(self):
        self.userdict = lib.apdicts.userdict
        self.timecard = lib.getconnections()['TimeCard']
        self.HPE = self.userdict['HPE']

    def __del__(self):
        self.timecard.close()

    def __enter__(self):
        self.timecard.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timecard.close()

    def fan(self):
        log.message(f'\r{f" [ HPE ]: FANs Info ":*^100}')
        self.timecard.send('ilorest serverinfo --fans\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[fr'Fan\s+{i}' for i in range(3, 7)])
        data = re.findall(r'Fan\s+(\S+):\s+'
                          r'Location:\s+(\S+)\s+'
                          r'Reading:\s+(\S+)%\s+'
                          r'Redundant:\s+(\S+)\s+'
                          r'Hot\s+Pluggable:\s+(\S+)\s+'
                          r'Health:\s+(\S+)', self.timecard.recbuf)
        _table = PrettyTable(
            ['FAN', 'Location', 'Redundant: "True"', 'Hot Pluggable: "True"', 'Health: "OK"', 'Result'])
        status = [len(data) == 4]
        for f, l, _, red, ho, he in data:
            result = all([red == 'True', ho == 'True', he == 'OK'])
            _table.add_row([f, l, red, ho, he, 'PASS' if result else 'FAIL'])
            status.append(result)
        log.message(f'{str(_table)}')
        lib.fail() if not all(status) else None

    def firmware(self):
        log.message(f'\r{f" [ HPE ]: Firmware Info ":*^100}')
        self.timecard.send('ilorest serverinfo --firmware\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[fr"iLO\s+5\s+:\s+{self.HPE['iLO']}",
                                                  fr"System\s+ROM\s+:\s+{self.HPE['Bios']}",
                                                  fr"System\s+Programmable\s+Logic\s+Device\s+:\s+{self.HPE['CPLD']}",
                                                  fr"TPM\s+Firmware\s+:\s+{self.HPE['TPM']}"])
        if data := dict(re.findall(r'(.+)\s+:\s+(.+)\s+', self.timecard.recbuf)):
            add_iss_data(hpe_ilo_version=data['iLO 5'],
                         hpe_bios_version=data['System ROM'],
                         hpe_cpld_version=self.HPE['CPLD'],
                         hpe_tpm_version=data['TPM Firmware'])
        else:
            lib.fail()

    def memory(self):
        log.message(f'\r{f" [ HPE ]: Memory Info ":*^100}')
        self.timecard.send('ilorest serverinfo --memory\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[fr'PROC\s+1\s+DIMM\s+{i}' for i in ['3', '5', '8', '10']])
        data = re.findall(r'Location:\s+(.+)\s+'
                          r'Memory\s+Type:\s+(.+)\s+'
                          r'Capacity:\s+(\S+)\s+MiB\s+'
                          r'Speed:\s+(\S+)\s+MHz\s+'
                          r'Status:\s+(\S+)\s+'
                          r'Health:\s+(\S+)\s+', self.timecard.recbuf)
        _table = PrettyTable(['Location', 'Memory: "DRAM DDR4"', 'Capacity: "16384" MiB', 'Speed: "2666" Mhz',
                              'Status: "GoodInUse"', 'Health: "OK"', 'Result'])
        status = [len(data) == 4]
        for l, m, c, sp, st, h in data:
            result = all([m == 'DRAM DDR4', c == '16384', sp == '2666', st == 'GoodInUse', h == 'OK'])
            _table.add_row([l, m, c, sp, st, h, 'PASS' if result else 'FAIL'])
            status.append(result)
        log.message(f'{str(_table)}')
        lib.fail() if not all(status) else add_iss_data(hpe_ram_memory=f'{len(status) - 1}x 16GB DDR4-2666')

    def power(self):
        log.message(f'\r{f" [ HPE ]: Power Info ":*^100}')
        self.timecard.send('ilorest serverinfo --power\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[r'Power\s+Supply\s+1', r'Power\s+Supply\s+2'])
        data = re.findall(r'(Power\s+Supply\s+[0-9]):\s(.+\s){8}|(PowerSupply\s+Redundancy\s+Group\s+1)\s(.+\s){3}',
                          self.timecard.recbuf)
        status = [data]
        for i, health in [tuple(filter(None, x)) for x in data]:
            result = 'OK' in health
            log.debug('{:>30}: {:>19} ---> | {} |'.format(i, re.sub(r'\s+', '', health), 'PASS' if result else 'FAIL'))
            status.append(result)
        add_iss_data(psu_health_status_1='OK', psu_health_status_2='OK') if all(status) else lib.fail()

        ###############################################################################################################
        self.timecard.send('ipmitool fru\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[r'FRU\s+Device\s+Description\s+:\s+PSU\s+1',
                                                  r'FRU\s+Device\s+Description\s+:\s+PSU\s+2'])

        data = re.findall(r'FRU\s+Device\s+Description\s+:\s+PSU\s+[12].+\s+.+\s+.+\s+'
                          r'Product\s+Part\s+Number\s+:\s+(\S+)\s+.+\s+'
                          r'Product\s+Serial\s+:\s+(\S+)', self.timecard.recbuf)

        add_iss_data(psu_part_number_1=data[0][0],
                     psu_serial_number_1=data[0][1],
                     psu_part_number_2=data[1][0],
                     psu_serial_number_2=data[1][1]) if data else lib.fail()

    def processors(self):
        log.message(f'\r{f" [ HPE ]: Processors Info ":*^100}')
        self.timecard.send('ilorest serverinfo --processors\r',
                           expectphrase=self.userdict['TimeCard'],
                           check_received_string=[fr"Model:\s+{self.HPE['CPU']}",
                                                  r'Step:\s+4',
                                                  r'Socket:\s+Proc\s+1',
                                                  r'Max\s+Speed:\s+4000\s+MHz',
                                                  r'Speed:\s+2000\s+MHz',
                                                  r'Cores:\s+20',
                                                  r'Threads:\s+40',
                                                  r'Health:\s+OK'])
        data = dict(re.findall(r'(.+):\s+(.+)\s+', self.timecard.recbuf))
        add_iss_data(hpe_cpu_model=data['Model'])

    def system(self):
        log.message(f'\r{f" [ HPE ]: System Info ":*^100}')
        self.timecard.send('ilorest\r', expectphrase=r'liLOrest\s+\>')
        self.timecard.send('exit\r', expectphrase=self.userdict['TimeCard'])
        self.timecard.send('ilorest serverinfo --system\r', expectphrase=self.userdict['TimeCard'],
                           check_received_string=[fr"Model:\s+{self.HPE['Model']}",
                                                  fr"Serial\s+Number:\s+{self.userdict['HPE_SN']}"])

        data = dict(re.findall(r'(.+):\s+(.+)\s+', self.timecard.recbuf))
        add_iss_data(hpe_model_number=data['Model'],
                     hpe_serial_number=data['Serial Number'],
                     mlx_nic_mac_1=data['MAC'].upper()) if data else lib.fail()

    def thermals(self):
        log.message(f'\r{f" [ HPE ]: Thermals Info ":*^100}')
        self.timecard.send('ilorest serverinfo --thermals\r', expectphrase=self.userdict['TimeCard'])
        data = re.findall(r'Sensor #(\S+):\s+Location:\s+(\S+)\s+(.+\s){4}\s+Health:\s+(.+)', self.timecard.recbuf)
        _table = PrettyTable(['Sensor', 'Location', 'Health: "OK"', 'Result'])
        status = [data]
        for s, l, _, h in data:
            result = 'OK' == h
            _table.add_row([s, l, h, 'PASS' if result else 'FAIL'])
            status.append(result)
        log.message(f'{str(_table)}')
        lib.fail() if not all(status) else None

    def assettag(self):
        log.message(f'\r{f" [ HPE ]: Compare Asset Tag with ODC ":*^100}')
        self.timecard.send('ilorest get AssetTag --select ComputerSystem\r',
                           expectphrase=self.userdict['TimeCard'],
                           check_received_string=self.userdict['TLA_PRODUCT_ASSET_TAG'])
        add_iss_data(hpe_assettag=self.userdict['TLA_PRODUCT_ASSET_TAG'])

    def macaddress(self):
        log.message(f'\r{f" [ HPE ]: ILO Mac Address ":*^100}')
        self.timecard.send('ilorest list macaddress --filter Name="Manager Dedicated Network Interface" --selector '
                           'EthernetInterface.v1_4_1\r', expectphrase=self.userdict['TimeCard'])
        mac = re.search(r'MACAddress=(\S+)', self.timecard.recbuf)
        add_iss_data(ilo_mac_address=mac.group(1)) if mac else lib.fail()

        log.message(f'\r{f" [ HPE ]: Mac Address ":*^100}')
        self.timecard.send("ip -o link show |cut -d ' ' -f 2,20\r", expectphrase=self.userdict['TimeCard'])
        mac = dict(re.findall(r'(\S+):\s+(\S+)', self.timecard.recbuf))
        add_iss_data(hpe_mac_address=mac['eno1'].upper()) if mac and mac['eno1'] else lib.fail()


@iss_service
def mlx_nic_firmware_update():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('lspci -v | grep Mellanox\r', expectphrase=userdict['TimeCard'])
        tc.send('cd /root/firmware/mellanox\r', expectphrase=userdict['TimeCard'])
        tc.send(f"ls -l {userdict['FW_Mellanox']}\r", expectphrase=userdict['TimeCard'])
        if tc.check_received_string('No such file or directory'):
            tc.send(f"scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
                    f"{lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:"
                    f"/home/timecard/firmware/mellanox/{userdict['FW_Mellanox']} .\r",
                    expectphrase=['yes/no', 'password:'])
            tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
            tc.send('W400admin\r', expectphrase=userdict['TimeCard'])
        tc.send('mlxfwmanager\r', expectphrase=userdict['TimeCard'])
        tc.send(f"mlxfwmanager -u -d 0000:61:00.0 -i {userdict['FW_Mellanox']}\r",
                expectphrase=[r'\[y/N\]', userdict['TimeCard']], timeout=600)
        tc.send('y\r', expectphrase=userdict['TimeCard'], timeout=600) if '[y/N]' in tc.recbuf else None
        if not tc.check_received_string(r'\d{2,3}%Writing\s+Boot\s+image\s+component\s+-\s+OK|'
                                        r'firmware\s+images\s+are\s+up\s+to\s+date'):
            lib.fail()


@iss_service
def ts2phc_offset_check(offset):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('cat /tmp/ts2phc.log\r', expectphrase=userdict['TimeCard'], timeout=120)
        m = re.findall(r'diff\s+(-?[0-9]+)', tc.recbuf)
    _table = PrettyTable(['Item', 'Offset', 'Values', 'Result'])
    _table.align['Item'] = 'r'
    status = []
    for i, v in enumerate(m[int(offset):]):
        result = -100 <= int(v) <= 100
        _table.add_row([i + 1, 'Offset', v, 'PASS' if result else 'FAIL'])
        status.append(result)
    log.message(f'{str(_table.get_string(title=f" Verify [ Offset < +/-100ns ] "))}\r\r')
    lib.fail() if not all(status) else None


@iss_service
def user_interaction_pre_pxe():
    if 'fail' == lib.ask_questions(question=f'Please Remove TSFP loopback and plug TSFP/VGA cables',
                                   picture_path='QSFP_Loopback_FST.jpg',
                                   html='user_interaction.html',
                                   timeout=86400):
        lib.fail()


@iss_service
def user_interaction_post_pxe():
    if 'fail' == lib.ask_questions(question=f'Check PXE Installation screen',
                                   picture_path='PXE_Install.jpg',
                                   html='user_interaction.html',
                                   timeout=86400):
        lib.fail()


@iss_service
def mlx_nic_realtime_clock_enable():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"mstconfig -d 61:00.0 -y s REAL_TIME_CLOCK_ENABLE=1\r", expectphrase=userdict['TimeCard'], timeout=60,
                check_received_string=r'Applying.+Done!|Please\s+reboot\s+machine\s+to\s+load\s+new\s+configurations')


@iss_service
def mlx_nic_pps_enable():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('/root/git/Time-Appliance-Project/Software/Experimental/PTPBox/tools/ptpmap\r',
                expectphrase=userdict['TimeCard'])
        if ptp_all := re.findall(r'(\S+).+ens1f[01]np[01]', tc.recbuf):
            for ptp in ptp_all:
                log.debug(f'| PPS Device | Name: {ptp} |')
                tc.send(f'~/ptp/testptp -d {ptp} -l\r', expectphrase=userdict['TimeCard'])
                [tc.send(f'~/ptp/testptp -d {ptp} -L {i},{i + 1}\r', expectphrase=userdict['TimeCard'],
                         check_received_string='set pin function okay') for i in range(2)]
                tc.send(f'~/ptp/testptp -d {ptp} -l\r', expectphrase=userdict['TimeCard'],
                        check_received_string=[r'name\s+mlx5_pps0\s+index\s+0\s+func\s+1\s+chan\s+0',
                                               r'name\s+mlx5_pps1\s+index\s+1\s+func\s+2\s+chan\s+0'])
                tc.send(f'~/ptp/testptp -d {ptp} -P 1\r', expectphrase=userdict['TimeCard'],
                        check_received_string=r'pps\s+for\s+system\s+time\s+request\s+okay', timeout=60)
        else:
            lib.fail()


@iss_service
def mlx_nic_pps_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('/root/git/Time-Appliance-Project/Software/Experimental/PTPBox/tools/ptpmap\r',
                expectphrase=userdict['TimeCard'])
        if ptp_all := re.findall(r'(\S+).+ens1f[01]np[01]', tc.recbuf):
            for ptp in ptp_all:
                log.debug(f'| PPS Device | Name: {ptp} |')
                tc.send(f"~/ptp/testptp -d {ptp} -l\r", expectphrase=userdict['TimeCard'],
                        check_received_string=[r'name\s+mlx5_pps0\s+index\s+0\s+func\s+0\s+chan\s+0',
                                               r'name\s+mlx5_pps1\s+index\s+1\s+func\s+2\s+chan\s+0'])
                tc.send(f"~/ptp/testptp -d {ptp} -c\r", expectphrase=userdict['TimeCard'],
                        check_received_string=r'1\s+pulse\s+per\s+second')
        else:
            lib.fail()


@iss_service
def mlx_nic_firmware_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('mlxfwmanager\r', expectphrase=userdict['TimeCard'],
                check_received_string=[fr"Base\s+MAC:\s+{userdict['NIC_MAC'].lower()}",
                                       fr"FW\s+{userdict['Mellanox']['FW']}",
                                       fr"PXE\s+{userdict['Mellanox']['PXE']}",
                                       fr"UEFI\s+{userdict['Mellanox']['UEFI']}"])


@iss_service
def mlx_nic_realtime_clock_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        for i in range(2):
            tc.send(f'mstconfig -d 61:00.{i} query | grep REAL_TIME_CLOCK | cat\r', expectphrase=userdict['TimeCard'],
                    check_received_string=r'REAL_TIME_CLOCK_ENABLE\s+True\(1\)', timeout=60)


@iss_service
def mlx_nic_info():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        pn = re.sub(r'(.+)(.{4})', r'\1-\2', userdict['NIC_MFG_PN'])
        tc.send('lspci -vv -s 61:00.0 | grep "Part number" -A 7 | cat\r', expectphrase=userdict['TimeCard'],
                check_received_string=[fr'Part\s+number:\s+{pn}',
                                       fr"Serial\s+number:\s+{userdict['NIC_SN']}"])
        if ec := re.search(r'Engineering\s+changes:\s+(\S+)', tc.recbuf):
            add_iss_data(mlx_nic_pn=pn,
                         mlx_nic_ec=ec.group(1),
                         mlx_nic_sn=userdict['NIC_SN'])
        else:
            lib.fail()


@iss_service
def mlx_pcie_info():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('mlxlink -d /dev/mst/mt4125_pciconf0 --port_type PCIE -c\r', expectphrase=userdict['TimeCard'],
                check_received_string=[r'Link\s+Speed\s+Active\s+\(Enabled\)\s+:\s+8G\-Gen\s+3\s+\(16G\-Gen\s+4\)',
                                       r'Link\s+Width\s+Active\s+\(Enabled\)\s+:\s+16X\s+\(16X\)'])


@iss_service
def mlx_eth_ports_link_check():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        for i in range(2):
            tc.send(f'mlxlink -d 61:00.{i}\r', expectphrase=userdict['TimeCard'],
                    check_received_string=[r'State\s+:\s+Active',
                                           r'Physical state\s+:\s+LinkUp',
                                           r'Speed\s+:\s+100G',
                                           r'Width\s+:\s+[2|4]x'])


@iss_service
def mlx_nic_loopback_test():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('ip a\r', expectphrase=userdict['TimeCard'], wait_before_send=300)
        ens = re.findall(r'(ens\S+):.+\s+link/ether\s+(\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2})', tc.recbuf)
        if len(ens) >= 2:
            log.debug(f'| Port 0 | Name: {ens[0][0]} | MAC Addresses: {ens[0][1]} |')
            log.debug(f'| Port 1 | Name: {ens[1][0]} | MAC Addresses: {ens[1][1]} |')
            for _ in range(3):
                log.message(f'{f" Setup the ip address for both QSFP ports ":*^100}')
                tc.send(f'ip -6 addr add fd00::10:0:1/64 dev {ens[0][0]}\r', expectphrase=userdict['TimeCard'])
                tc.send(f'ip -6 addr add fd00::10:1:1/64 dev {ens[1][0]}\r', expectphrase=userdict['TimeCard'])

                log.message(f'{f" Add the new routing ":*^100}')
                tc.send(f'ip -6 route add fd00::20:0:1 dev {ens[1][0]}\r', expectphrase=userdict['TimeCard'])
                tc.send(f'ip -6 route add fd00::20:1:1 dev {ens[0][0]}\r', expectphrase=userdict['TimeCard'])
                tc.send('route -6 -n\r', expectphrase=userdict['TimeCard'])

                log.message(f'{f" Set iptables nat POST and PRE routing ":*^100}')
                tc.send('ip6tables -t nat -A POSTROUTING -d fd00::20:1:1 -j SNAT --to-source fd00::20:0:1\r',
                        expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -t nat -A POSTROUTING -d fd00::20:0:1 -j SNAT --to-source fd00::20:1:1\r',
                        expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -t nat -A PREROUTING -d fd00::20:0:1 -j DNAT --to-destination fd00::10:0:1\r',
                        expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -t nat -A PREROUTING -d fd00::20:1:1 -j DNAT --to-destination fd00::10:1:1\r',
                        expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -A INPUT -i ens1f0np0 -j ACCEPT\r', expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -A INPUT -i ens1f1np1 -j ACCEPT\r', expectphrase=userdict['TimeCard'])
                tc.send(f'ip -6 neigh add fd00::20:0:1  lladdr {ens[0][1]} dev ens1f1np1 nud permanent\r',
                        expectphrase=userdict['TimeCard'], wait_before_send=180)
                tc.send(f'ip -6 neigh add fd00::20:1:1  lladdr {ens[1][1]} dev ens1f0np0 nud permanent\r',
                        expectphrase=userdict['TimeCard'])
                tc.send('ip6tables -t nat -nvL\r', expectphrase=userdict['TimeCard'])

                log.message(f'{f" Start iperf server side in Daemon mode ":*^100}')
                tc.send('rm -rf /tmp/listen.txt\r', expectphrase=userdict['TimeCard'])
                tc.send('iperf3 -6 -s -DB fd00::10:0:1 --logfile /tmp/listen.txt\r', expectphrase=userdict['TimeCard'])
                tc.send('ps aux | grep iperf | grep -v grep\r', expectphrase=userdict['TimeCard'])

                log.message(f'{f" Run iperf3 client side ":*^100}')
                tc.send('iperf3 -6 -B fd00::10:1:1 -c fd00::20:0:1\r', expectphrase=userdict['TimeCard'], timeout=600)
                if tc.check_not_received_string(['error', 'Cannot assign requested address']):
                    if userdict['${SUITE_NAME}'] in ['ST', 'FST']:
                        log.message(f'{f" Check the result on server side ":*^100}')
                        tc.send('cat /tmp/listen.txt\r', expectphrase=userdict['TimeCard'],
                                check_received_string=r'0\.00\-10\.00\s+sec\s+\d+\.\d\s+GBytes\s+\d+\.\d\s+Gbits/sec\s+receiver')

                        log.message(f'{f" Remove the log file ":*^100}')
                        tc.send('rm -rf /tmp/listen.txt\r', expectphrase=userdict['TimeCard'])

                        log.message(f'{f" Kill the iperf process ":*^100}')
                        tc.send('pkill iperf3\r', expectphrase=userdict['TimeCard'])
                        tc.send('ps aux | grep iperf | grep -v grep\r', expectphrase=userdict['TimeCard'])
                    return True
        lib.fail()


@iss_service
def messages_delete():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('rm -rf /tmp/*\r', expectphrase=userdict['TimeCard'], timeout=120)
        tc.send('ls -l /tmp/\r', expectphrase=userdict['TimeCard'])
        for _ in range(3):
            tc.send('rm -rf /var/log/messages*\r', expectphrase=userdict['TimeCard'], timeout=600)
            tc.send('ls -l /var/log/messages*\r', expectphrase=userdict['TimeCard'], wait_before_send=2)
            if tc.check_received_string('No such file or directory'):
                return True
        lib.fail()


@iss_service
def modprobe_ptp_ocp():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('modprobe ptp_ocp\r', expectphrase=userdict['TimeCard'])


@iss_service
def mst_start():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('mst start\r', expectphrase=userdict['TimeCard'],
                check_received_string=[r'Loading\s+MST\s+PCI\s+module.+Success',
                                       r'Unloading\s+MST\s+PCI\s+module\s+\(unused\).+Success'])


@iss_service
def pci_scan_test():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        model = userdict['${SUITE_NAME}'] in ['FCT'] or len(userdict['TC_SN']) == 13
        tc.send(f"lspci -vvv | grep -i {'Celestica' if model else 'spectracom'} -A 30 | grep -i LnkSta | cat\r",
                expectphrase=userdict['TimeCard'],
                check_received_string=['Speed 2.5GT/s', f"Width x{'1' if model else '4'}"])
        tc.send(f"lspci -nn | grep -i {'Celestica' if model else 'spectracom'}\r", expectphrase=userdict['TimeCard'],
                check_received_string=f"Device [{'18d4:1008' if model else '1ad7:a000'}]")


@iss_service
def integration_test():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib\r', expectphrase=userdict['TimeCard'])
        tc.send('art_integration_in_server_test -p /sys/class/timecard/ocp0/\r', expectphrase=userdict['TimeCard'],
                timeout=1200, check_received_string=r'Test\s+PASSED')


@iss_service
def usb_c_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('lsusb -tv\r', expectphrase=userdict['TimeCard'], check_received_string=r'Driver=ftdi_sio')
        tc.send('ftdi i2c pca\r', expectphrase=userdict['TimeCard'], check_received_string=r'The data is 0')
        tc.send('ftdi i2c eeprom\r', expectphrase=userdict['TimeCard'],
                check_received_string=r'bytearray\(b\'\\xfb\\xfb\'\)')


@iss_service
def verify_timecard_driver():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('dmesg | grep ptp_ocp\r', expectphrase=userdict['TimeCard'],
                check_received_string=[r'GNSS:\s+/dev/ttyS4\s+@\s+115200', r'MAC:\s+/dev/ttyS6\s+@\s+57600'])


@iss_service
def orolia_driver_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('ls -g /sys/class/timecard/ocp0/\r', expectphrase=userdict['TimeCard'],
                check_received_string=['0000:11:00.0', 'i2c-1', 'mro50.0', 'ptp6', 'sma1',
                                       'sma2', 'sma3', 'sma4', 'ttyS4'])
        tc.send('dmesg | grep ptp_ocp\r', expectphrase=userdict['TimeCard'],
                check_received_string=r'GNSS:\s+/dev/ttyS4\s+@\s+\d+')
        tc.send('ls /dev | grep mro | cat\r', expectphrase=userdict['TimeCard'], check_received_string='mro50.0')


@iss_service
def orolia_fpga_fw_verify():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('dmesg | grep ptp_ocp\r', expectphrase=userdict['TimeCard'],
                check_received_string=fr"Version\s+{userdict['Orolia_FPGA_Ver']}")
    add_iss_data(tc_fpga_fw_version=userdict['Orolia_FPGA_Ver'])


@iss_service
def verify_pca9546_i2c_bus():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        log.message(f'{f" PCA9546 Bus ":*^100}')
        tc.send(f"i2cdetect -y -r {userdict['TC_I2C']}\r", expectphrase=userdict['TimeCard'])
        for i, (senser, value) in enumerate(
                [('Temp', '0x004b'), ('Humidity', '44'), ('Air Pressure', '63'), ('Vibration', '4a')]):
            log.message(f'\r{f" Set to CH{i} [ {senser} Sensor ] ":*^100}')
            tc.send(f"i2cset -y -r {userdict['TC_I2C']} 0x70 0x0{pow(2, i)}\r", expectphrase=userdict['TimeCard'],
                    check_received_string='readback matched')
            if i == 0:
                for ii, address in enumerate(['48', '49', '4a']):
                    log.message(f'{f" {senser} Sensor #{ii + 1:02d} ":*^100}')
                    tc.send(f"i2cget -y {userdict['TC_I2C']} 0x{address} 0x02 w\r", expectphrase=userdict['TimeCard'],
                            check_received_string=value)
            else:
                tc.send(f"i2cdetect -y -r {userdict['TC_I2C']}\r", expectphrase=userdict['TimeCard'],
                        check_received_string=value)


@iss_service
def fpga_firmware_update(_id):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"devlink dev flash pci/0000:{_id} file {userdict['Meta_FW_FPGA']}\r",
                expectphrase=userdict['TimeCard'], timeout=120, check_received_string='Flash complete')


@iss_service
def eeprom_format_imgration():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"/opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/build/utils/art_disciplining_manager -p /sys/class/timecard/ocp0/i2c/1-0050/eeprom -r -o /tmp/coarse.txt\r",
                expectphrase=userdict['TimeCard'])
        coarse_value = re.search(r'coarse_equilibrium_factory\s+=\s+([0-9\-]+)', tc.recbuf)
        coarse_value = coarse_value.group(1)
        tc.send(f"cat /tmp/coarse.txt\r", expectphrase=userdict['TimeCard'])
        tc.send(f"/opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/build/utils/art_disciplining_manager -p /sys/class/timecard/ocp0/disciplining_config -f -c {coarse_value}\r",
                expectphrase=userdict['TimeCard'])
        tc.send(f"/opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/build/utils/art_temperature_table_manager -p /sys/class/timecard/ocp0/temperature_table -f\r",
                expectphrase=userdict['TimeCard'])


@iss_service
def orolia_fpga_firmware_update():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(
            f"flashrom -p ft2232_spi:type=4233H -c MT25QU256 -w /root/firmware/orolia/{userdict['Orolia_FW_FPGA']}\r",
            expectphrase=userdict['TimeCard'], timeout=600, check_received_string='Erase/write done.')


@iss_service
def fpga_firmware_verify(pci_id):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f'TestApp 0x{pci_id}\r', expectphrase=r'PPS\s+pulse\s+width\s+is\s+=\s+\d+',
                check_received_string=fr"FPGA\s+Image\s+Version\s+=\s+{userdict['Meta_FPGA_Ver']}")
        tc.send('\x03', expectphrase=userdict['TimeCard'])


@iss_service
def messages_log(save_log=False):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('dmesg\r', expectphrase=userdict['TimeCard'], timeout=1200)
        save_file(tc.recbuf, 'dmesg.log') if save_log else None
        tc.send('\n\r', expectphrase=userdict['TimeCard'])
        # tc.send('cat /var/log/messages\r', expectphrase=userdict['TimeCard'], timeout=1200)
        # save_file(tc.recbuf, 'Messages.log') if save_log else None


@iss_service
def hpe_hdd_check():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('lsblk -S\r', expectphrase=userdict['TimeCard'])
        if devices := re.search(r'(\S+).+sata', tc.recbuf):
            devices = devices.group(1)
            tc.send(f'mkfs.ext4 /dev/{devices}\r', expectphrase=['(y,N)', userdict['TimeCard']])
            tc.send('y\r', expectphrase=userdict['TimeCard']) if '(y,N)' in tc.recbuf else None
            tc.send(f'mount /dev/{devices} /mnt/hdd\r', expectphrase=userdict['TimeCard'])
            tc.send('lsblk\r', expectphrase=userdict['TimeCard'], check_received_string=fr'{devices}.+disk\s+/mnt/hdd')

            log_message('Test HDD Write Speed')
            tc.send('sync; dd if=/dev/zero of=/mnt/hdd/tempfile bs=1M count=1024; sync\r',
                    expectphrase=userdict['TimeCard'], check_received_string=r'\(1.1\s+GB,\s+1.0\s+GiB\)',
                    check_not_received_string=r'[Ee]rror')
            log_message('Test HDD Read Speed')
            tc.send('dd if=/mnt/hdd/tempfile of=/dev/null bs=1M count=1024\r', expectphrase=userdict['TimeCard'],
                    check_received_string=r'\(1.1\s+GB,\s+1.0\s+GiB\)', check_not_received_string=r'[Ee]rror')

            tc.send('umount /mnt/hdd\r', expectphrase=userdict['TimeCard'])
            tc.send('lsblk\r', expectphrase=userdict['TimeCard'], check_received_string=fr'{devices}.+disk[ ]+')
        else:
            lib.fail()


@iss_service
def eeprom_programming():
    userdict = lib.apdicts.userdict
    state = ['EVT', 'DVT', 'PVT', 'MP'].index(userdict['TC_PRODUCTION_STATE'])

    eeprom = ''
    eeprom += '[Meta]\n'
    eeprom += 'magic_word=0xfbfb\n'
    eeprom += 'format_version=0x03\n'
    eeprom += 'product_name=TIME CARD\n'
    eeprom += f"top_level_product_part_number={userdict['TLA_PRODUCT_PN']}\n"
    eeprom += f"system_assembly_part_number={userdict['TC_ASSY_PN']}\n"
    eeprom += f"facebook_pcba_part_number={userdict['TC_FB_PCBA_PN']}\n"
    eeprom += f"facebook_pcb_part_number={userdict['TC_FB_PCB_PN']}\n"
    eeprom += f"odm_pcba_part_number={userdict['TC_ODM_PCBA_PN']}\n"
    eeprom += f"odm_pcba_serial_number={userdict['TC_ODM_PCBA_SN']}\n"
    eeprom += f"product_production_state={str(state + 1)}\n"
    eeprom += f"product_version={userdict['TC_PRODUCT_VERSION']}\n"
    eeprom += f"product_sub_version={userdict['TC_PRODUCT_SUB_VERSION']}\n"
    eeprom += f"product_serial_number={userdict['TC_PRODUCT_SN']}\n"
    eeprom += 'product_asset_tag=NA\n'
    eeprom += 'system_manufacturer=CLS\n'
    eeprom += f'system_manufacturing_date={datetime.now().strftime("%m%d%Y")}\n'
    eeprom += f"pcb_manufacturer={userdict['TC_PCB_MFG']}\n"
    eeprom += 'assembled_at=CTH\n'
    eeprom += 'local_mac_address=000000000000\n'
    eeprom += 'extended_mac_address_base=000000000000\n'
    eeprom += 'extended_mac_address_size=0\n'
    eeprom += 'eeprom_location_on_fabric=TIME CARD'
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('cd /root/fbeeprom/\r', expectphrase=userdict['TimeCard'],
                check_not_received_string='No such file or directory')
        tc.send('rm -rf timecard.cfg\r', expectphrase=userdict['TimeCard'])
        tc.send(f'echo -e {repr(eeprom)} > timecard.cfg\r', expectphrase=userdict['TimeCard'])
        tc.send('cat timecard.cfg\r', expectphrase=userdict['TimeCard'])
        tc.send('fbeeprom build -c timecard.cfg -b timecard.bin\r', expectphrase=userdict['TimeCard'],
                check_received_string='bin file timecard.bin')
        tc.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        tc.send('j', expectphrase='please select test option')
        tc.send('b', expectphrase='Please input [filename]')
        tc.send('/root/fbeeprom/timecard.bin\r', expectphrase='Press Enter key to continue',
                check_received_string=r'\[timecard\.test_update_eeprom\].+PASS')


def eeprom_verify():
    userdict = lib.apdicts.userdict
    state = ['EVT', 'DVT', 'PVT', 'MP'].index(re.sub(r'[0-9]', '', userdict['TC_PRODUCTION_STATE']))
    with lib.getconnections()['TimeCard'] as tc:
        model = userdict['${SUITE_NAME}'] in ['FCT'] or len(userdict['TC_SN']) == 13
        timecard = {'magic_word': '0xfbfb',
                    'format_version': '0x03',
                    'product_name': 'TIME CARD',
                    'top_level_product_part_number': userdict['TLA_PRODUCT_PN'] if model else '00000000',
                    'system_assembly_part_number': userdict['TC_ASSY_PN'] if model else '19002225',
                    'facebook_pcba_part_number': userdict['TC_FB_PCBA_PN'] if model else '13200014402',
                    'facebook_pcb_part_number': userdict['TC_FB_PCB_PN'] if model else '13100010902',
                    'odm_pcba_part_number': userdict['TC_ODM_PCBA_PN'] if model else '1003066A00',
                    'odm_pcba_serial_number': userdict['TC_ODM_PCBA_SN'] if model else userdict['TC_SN'],
                    'product_production_state': str(state + 1) if model else '3',
                    'product_version': userdict['TC_PRODUCT_VERSION'] if model else '5',
                    'product_sub_version': userdict['TC_PRODUCT_SUB_VERSION'] if model else '0',
                    'product_serial_number': userdict['TC_PRODUCT_SN'] if model else userdict['TC_SN'],
                    'product_asset_tag': 'NA' if model else '0000000000',
                    'system_manufacturer': 'CLS' if model else 'OROLIA',
                    'pcb_manufacturer': userdict['TC_PCB_MFG'] if model else 'JOVE',
                    'assembled_at': 'CTH' if model else 'ASTEEL',
                    'local_mac_address': '000000000000',
                    'extended_mac_address_base': '000000000000',
                    'extended_mac_address_size': '0',
                    'eeprom_location_on_fabric': 'TIME CARD'}
        tc.send(f"i2cdump -y -f {userdict['TC_I2C']} 0x{'50' if model else '52'}\r", expectphrase=userdict['TimeCard'])
        tc.send(f"fbeeprom dump {userdict['TC_I2C']} 0x{'50' if model else '52'}\r", expectphrase=userdict['TimeCard'])
        value = dict(re.findall(r'(\S+)=(.+)\s+', tc.recbuf))
        _table = PrettyTable(['Name', 'EEPROM', 'ODC', 'Result'])
        _table.align['Name'] = 'l'
        status = []
        for k, v in timecard.items():
            result = v == value[k].strip()
            _table.add_row([k, value[k].strip(), v, 'PASS' if result else 'FAIL'])
            status.append(result)
        log.message(f'{str(_table.get_string(title=f" Verify [ EEPROM == ODC ] "))}\r\r')
        lib.fail() if not all(status) else None


@iss_service
def verify_gnss_module_and_atomic_clock_present():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('ls -g /sys/class/timecard/ocp0/\r', expectphrase=userdict['TimeCard'],
                check_received_string=[r'ttyGNSS\s+\-\>\s+\.\./\.\./tty/ttyS4',
                                       r'ttyMAC\s+\-\>\s+\.\./\.\./tty/ttyS6'])


@iss_service
def verify_time_card_gps_locked():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('cat /sys/class/timecard/ocp0/gnss_sync\r', expectphrase=userdict['TimeCard'], wait_before_send=5,
                check_received_string='SYNC', retry=10)


@iss_service
def verify_gps_device_in_timing_mode():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('tio -b 115200 /dev/ttyS4\r', expectphrase='Connected')
        tc.send('\x14', wait_before_send=5)
        tc.send('q\r', expectphrase=userdict['TimeCard'],
                check_not_received_string=['GLGSV', 'GAGSV', 'GNGGA', 'GNRMC', 'GNGSA', 'GPGSV', 'GBGSV', 'GNVTG',
                                           'GNGLL'])


@iss_service
def verify_mac():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('tio -b 57600 /dev/ttyS6\r', expectphrase='Connected')
        tc.send('c\r', expectphrase=r'Analog\s+Tuning\s+\(mv\)\s+=\s+\d+',
                check_received_string=fr"Version\s+=\s+V{userdict['MAC_Ver']}")
        tc.send('\x14')
        tc.send('q\r', expectphrase=userdict['TimeCard'])


@iss_service
def config_mac(disciplining=1, width=80000000, tau=1000, offset=-30, discipline=20):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('tio -b 57600 /dev/ttyS6\r', expectphrase='Connected')
        tc.send(f'\\{{set,Disciplining,{disciplining}}}\r', expectphrase='\n',
                check_received_string=f'[={disciplining}]')
        tc.send(f'\\{{set,PpsWidth,{width}}}\r', expectphrase='\n', check_received_string=f'[={width}]')
        tc.send(f'\\{{set,TauPps0,{tau}}}\r', expectphrase='\n', check_received_string=f'[={tau}]')
        tc.send(f'\\{{set,PpsOffset,{offset}}}\r', expectphrase='\n', check_received_string=f'[={offset}]')
        tc.send(f'\\{{set,DisciplineThresholdPps0,{discipline}}}\r', expectphrase='\n',
                check_received_string=f'[={discipline}]')
        tc.send('\\{get,PpsInDetected}\r', expectphrase='\n', check_received_string='[=1]')
        tc.send('\\{store}\r', expectphrase='\n', check_received_string='[=1]')
        tc.send('\x14')
        tc.send('q\r', expectphrase=userdict['TimeCard'])


@iss_service
def eeprom_i2c_bus_test():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('i2cdetect -y 13\r', expectphrase=userdict['TimeCard'])
        tc.send('i2cdump -y -f 13 0x50\r', expectphrase=userdict['TimeCard'])
        tc.send('i2cdump -y -f 13 0x58\r', expectphrase=userdict['TimeCard'])


@iss_service
def disciplining(timeout):
    userdict = lib.apdicts.userdict
    time.sleep(300)
    with lib.TimeIt() as t:
        while t.duration <= int(timeout):
            clear_row_file()
            log.message(f"\r{f' Checking Holdover Status ':*^100}")
            with lib.getconnections()['TimeCard'] as tc:
                tc.send("echo '{}' | nc 0.0.0.0 2958\r", expectphrase=userdict['TimeCard'], timeout=60,
                        check_not_received_string=r'Ncat:\s+Connection\s+refused')
                value = re.search(r'"ready_for_holdover":\s+"(\S+)"', tc.recbuf)
                if not value:
                    break
                log.message(f'Ready For Holdover: Expect "true", Actual: "{value.group(1)}"')
                if 'true' in value.group(1):
                    return True
            time.sleep(60)
    lib.fail()


@iss_service
def set_sma(ch, clock):
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f'echo OUT: {clock} > /sys/class/timecard/ocp0/{ch}\r', expectphrase=userdict['TimeCard'])
        tc.send(f'cat /sys/class/timecard/ocp0/{ch}\r', expectphrase=userdict['TimeCard'],
                check_received_string=f'OUT: {clock}')


@iss_service
def start_sentinel():
    with Sentinel() as s:
        s.start()


@iss_service
def stop_sentinel():
    with Sentinel() as s:
        s.stop()


@iss_service
def get_data_sentinel(clock, plus_minus, datatype='TIE', ch=None, timeout=60):
    s = Sentinel()
    s.getdata(clock=clock, plus_minus=plus_minus, datatype=datatype, ch=ch, timeout=timeout)


# class Sentinel(object):
#     def __init__(self):
#         self.userdict = lib.apdicts.userdict
#         self.timecard = lib.getconnections()['TimeCard']
#         self.Sentinal = lib.getconnections()['Sentinal']
#         self.host = self.Sentinal.host
#
#     def __del__(self):
#         self.timecard.close()
#
#     def __enter__(self):
#         self.timecard.shared_conn = self.userdict['${SUITE_NAME}'] in ['BI', 'RDT']
#         self.timecard.open()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.timecard.close()
#
#     def getstatus(self):
#         self.timecard.send(f'curl -k https://[{self.host}]/api/getstatus\r', expectphrase=self.userdict['TimeCard'])
#         return self.timecard.recbuf
#
#     def start(self):
#         for _ in range(2):
#             self.timecard.send(f'curl -k https://[{self.host}]/api/startmeasurement\r', expectphrase=self.userdict['TimeCard'])
#             if self.timecard.check_received_string('true'):
#                 return True
#             self.stop()
#             time.sleep(30)
#         lib.fail()
#
#     def stop(self):
#         self.timecard.send(f'curl -k https://[{self.host}]/api/stopmeasurement\r',
#                            expectphrase=self.userdict['TimeCard'], check_received_string='true')
#
#     def getdata(self, clock, plus_minus, datatype, ch, timeout):
#         ch = ch if ch else self.Sentinal.ch
#         group_name = lib.get_sync_container_name() if self.userdict['${SUITE_NAME}'] in ['BI', 'RDT'] else ''
#         data = []
#         with lib.RDB.lock(f'{group_name}::Lock Get Data Sentinel'):
#             with lib.getconnections()['TimeCard'] as tc:
#                 while 'No data available' not in tc.recbuf:
#                     tc.send(f"curl -k https://[{self.host}]/api/getdata?'channel={ch}&datatype={datatype.lower()}'\r",
#                             expectphrase=self.userdict['TimeCard'], timeout=timeout)
#                     data.extend(re.findall(r'(\d+\.\d+),(-?\d+\.\d+)', tc.recbuf))
#
#         status, x, y = [], [], []
#         # .............  Table  ..............
#         _table = PrettyTable(['Time [hh:mm:ss]', f'{datatype}/s', 'Result'])
#         start_time = float(data[0][0])
#         for t, v in data[80:]:
#             _time = float(t) - start_time
#             result = abs(float(v)) <= float(plus_minus)
#             _table.add_row([formatted_seconds(int(_time)), f'{float2si(v)}s', 'PASS' if result else 'FAIL'])
#             status.append(result)
#             x.append(_time)
#             y.append(float(v))
#         log.message(f'{str(_table.get_string(title=f"Channel {ch} - {clock} [+/-{float2si(plus_minus)}s]"))}\r\r')
#
#         # .............  Graph  ..............
#         fig = plt.figure()
#         ax = fig.add_subplot(1, 1, 1)
#         ax.plot(x, y)
#         ax.set_ylim([-float(plus_minus), float(plus_minus)])
#         plt.grid()
#         plt.xlabel('Time/s')
#         plt.ylabel(datatype)
#         plt.title(f'Channel {ch} - {clock}')
#         plt.savefig(f'{BuiltIn().get_variable_value("${Raw_logs_path}")}/Channel_{ch}.jpg')
#         plt.close(fig)
#         lib.fail() if not status or not all(status) else None


class Sentinel(object):
    def __init__(self):
        self.userdict = lib.apdicts.userdict
        self.timecard = lib.getconnections()['TimeCard']
        self.Sentinal = lib.getconnections()['Sentinal']
        self.host = self.Sentinal.host

    def __del__(self):
        self.timecard.close()

    def __enter__(self):
        self.timecard.shared_conn = self.userdict['${SUITE_NAME}'] in ['BI', 'RDT']
        self.timecard.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timecard.close()

    def getstatus(self):
        self.timecard.send(f'curl -k https://[{self.host}]/api/getstatus\r', expectphrase=self.userdict['TimeCard'])
        return self.timecard.recbuf

    def start(self):
        self.timecard.send(f'curl -k https://[{self.host}]/api/startmeasurement\r',
                           expectphrase=self.userdict['TimeCard'], check_received_string='true')

    def stop(self):
        self.timecard.send(f'curl -k https://[{self.host}]/api/stopmeasurement\r',
                           expectphrase=self.userdict['TimeCard'], check_received_string='true')

    def getdata(self, clock, plus_minus, datatype, ch, timeout):
        ch = ch if ch else self.Sentinal.ch
        group_name = lib.get_sync_container_name() if self.userdict['${SUITE_NAME}'] in ['BI', 'RDT'] else ''
        status, x, y = [], [], []
        with lib.RDB.lock(f'{group_name}::Lock Get Data Sentinel'):
            with lib.getconnections()['TimeCard'] as tc:
                for _ in range(60):
                    tc.send(f"curl -k https://[{self.host}]/api/getdata?'channel={ch}&datatype={datatype.lower()}&reset=true'\r",
                            expectphrase=self.userdict['TimeCard'], timeout=timeout)
                    if not re.search(r'\d+.+\[', tc.recbuf):
                        break
                _table = PrettyTable(['Time [hh:mm:ss]', f'{datatype}/s', 'Result'])
                _time = 0
                for i, (t, value) in enumerate(re.findall(r'(\S+),(\S+)', tc.recbuf)):
                    _time = float(t) if i <= 0 else _time
                    if (float(t) - _time) >= 80:
                        result = -float(plus_minus) <= float(value) <= float(plus_minus)
                        _table.add_row([formatted_seconds(int(float(t) - _time)), f'{float2si(value)}s',
                                        'PASS' if result else 'FAIL'])
                        status.append(result)
                        x.append(float(t) - _time)
                        y.append(float(value))

                # .............  Table  ..............
                log.message(f'{str(_table.get_string(title=f"Channel {ch} - {clock} [+/-{float2si(plus_minus)}s]"))}\r\r')
        # .............  Graph  ..............
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(x, y)
        ax.set_ylim([-float(plus_minus), float(plus_minus)])
        plt.grid()
        plt.xlabel('Time/s')
        plt.ylabel(datatype)
        plt.title(f'Channel {ch} - {clock}')
        plt.savefig(f'{BuiltIn().get_variable_value("${Raw_logs_path}")}/Channel_{ch}.jpg')
        plt.close(fig)
        lib.fail() if not status or not all(status) else None


def remove_antenna():
    lib.ask_questions(question=f'Please Remove Antenna',
                      picture_path='timecard_bft.jpg',
                      html='user_interaction.html',
                      timeout=10800)


@iss_service
def holdover(_time):
    count = 1
    with lib.TimeIt() as t:
        while t.duration <= int(_time):
            clear_row_file()
            log_message(f'Loop {count} [ {formatted_seconds(t.duration)} ]')
            messages_log(save_log=True)
            with HoldOver() as h:
                h.hpe_temp()
                h.meta_temp() if len(userdict['TC_SN']) == 13 else h.orolia_temp()
                h.mellanox_stress()
                h.mei_delete()
            time.sleep(120)
            count += 1


@iss_service
def orolia_holdover():
    profile = [{'temperature': 15, 'delay': 3600},
               {'temperature': 35, 'delay': 2400},
               {'temperature': 25, 'delay': 2100},
               {'temperature': 15, 'delay': 2100},
               {'temperature': 35, 'delay': 2100},
               {'temperature': 15, 'delay': 2100},
               {'temperature': 25, 'delay': 2400},
               {'temperature': 35, 'delay': 2400},
               {'temperature': 15, 'delay': 2100},
               {'temperature': 35, 'delay': 3840},
               {'temperature': 15, 'delay': 3840}]
    count = 1
    ch_count = 1
    for _ in range(4):
        for i in profile:
            with lib.TimeIt() as t:
                lib.sync_group(f'CHAMBER {ch_count}')
                with ChamberInterface() as cb:
                    cb.chamber_profile(temperature=i['temperature'], ramp_rate=5)
                while t.duration <= i['delay']:
                    clear_row_file()
                    log_message(f'Loop: {count}')
                    messages_log(save_log=True)
                    with HoldOver() as h:
                        h.hpe_temp()
                        h.orolia_temp()
                        h.mellanox_stress()
                        h.mei_delete()
                    time.sleep(120)
                    count += 1
                ch_count += 1
    lib.sync_group('CHAMBER')
    with ChamberInterface() as cb:
        cb.chamber_profile(temperature=25, ramp_rate=5)


class HoldOver(object):
    def __init__(self):
        self.userdict = lib.apdicts.userdict
        self.tc = lib.getconnections()['TimeCard']
        self.tc_diag = lib.getconnections()['TimeCard']

    def __del__(self):
        self.tc.close()
        self.tc_diag.close()

    def __enter__(self):
        self.tc.open()
        self.tc_diag.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tc.close()
        self.tc_diag.close()

    def hpe_temp(self):
        self.tc.send('ilorest serverinfo --thermals\r', expectphrase=self.userdict['TimeCard'])
        save_file(self.tc.recbuf, 'HPE_Thermals.log')

    def meta_temp(self):
        log_message('Meta Temperature')
        self.tc_diag.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        self.tc_diag.send('g', expectphrase='please select test option')
        self.tc_diag.send('a', expectphrase='Press Enter key to continue',
                          check_received_string=r'Test\s+all\s+items.+\[.+PASS.+\]')
        save_file(self.tc_diag.recbuf, 'Timecard_Senser.log')

    def orolia_temp(self):
        log_message('Orolia Monitoring')
        self.tc.send('art_monitoring_client -a 0.0.0.0 -p 2958\r', expectphrase=self.userdict['TimeCard'])
        if temp := re.search(r'(temperature:\s+\S+)', self.tc.recbuf):
            log.debug(f'Orolia Temp: {temp.group(1)} C')
            save_file(f'{temp.group(1)} C', 'Timecard_Temp.log')
            save_file(self.tc.recbuf, 'Timecard_Monitoring.log')
        else:
            lib.fail()

    def mellanox_stress(self):
        log_message('Mellanox NIC Stress')
        self.tc.send('iperf3 -6 -B fd00::10:1:1 -c fd00::20:0:1\r', expectphrase=self.userdict['TimeCard'],
                     check_not_received_string=['error', 'Cannot assign requested address'])
        save_file(self.tc.recbuf, 'Mellanox_NIC_Stress.log')

    def mei_delete(self):
        self.tc.send('\n\r', expectphrase=self.userdict['TimeCard'])
        self.tc.send('rm -rf /tmp/_MEI*\r', expectphrase=self.userdict['TimeCard'], timeout=300)


@iss_service
def holdover_pps_in_detected_mac():
    log_message('Get PpsInDetected')
    userdict = lib.apdicts.userdict
    model = len(userdict['TC_SN']) == 13
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"cat /etc/oscillatord.conf.{'timecard' if model else 'orolia'} > /etc/oscillatord.conf\r",
                expectphrase=userdict['TimeCard'])
        tc.send('cat /etc/oscillatord.conf\r', expectphrase=userdict['TimeCard'])


@iss_service
def oscillatord_config():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"ls -l /opt/oscillatord-{userdict['Oscillatord_Ver']}\r", expectphrase=userdict['TimeCard'])
        if re.search(r'No\s+such\s+file\s+or\s+directory', tc.recbuf):
            log.message(f"Oscillatord V{userdict['Oscillatord_Ver']} not found...")
            log.message(f"Need to download and recompile Oscillatord V{userdict['Oscillatord_Ver']}")
            tc.send(f"scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:/home/timecard/firmware/oscillatord/oscillatord-{userdict['Oscillatord_Ver']} /opt/\r",
                    expectphrase=['yes/no', 'password:'])
            tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
            tc.send(f"{lib.getconnections()['Server'].password}\r", expectphrase=userdict['TimeCard'])

            log.message("Build and Make pps-tool")
            tc.send(f"cd /opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/pps-tools\r",
                    expectphrase=userdict['TimeCard'])
            tc.send('make install\r', expectphrase=userdict['TimeCard'])

            log.message("Build and Make ubloxcfg")
            tc.send(f"cd /opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/ubloxcfg\r",
                    expectphrase=userdict['TimeCard'])
            tc.send('make libubloxcfg.so\r', expectphrase=userdict['TimeCard'])
            tc.send('make install-library\r', expectphrase=userdict['TimeCard'])

            log.message("Build and Make disciplining-minipod")
            tc.send(f"cd /opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/disciplining-minipod\r",
                    expectphrase=userdict['TimeCard'])
            tc.send('mkdir build\r', expectphrase=userdict['TimeCard'])
            tc.send('cd build\r', expectphrase=userdict['TimeCard'])
            tc.send('cmake ..\r', expectphrase=userdict['TimeCard'])
            tc.send('make install\r', expectphrase=userdict['TimeCard'])

            log.message("Build and Make Oscillatord")
            tc.send(f"cd /opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/\r",
                    expectphrase=userdict['TimeCard'])
            tc.send('mkdir build\r', expectphrase=userdict['TimeCard'])
            tc.send('cd build\r', expectphrase=userdict['TimeCard'])
            tc.send('cmake ..\r', expectphrase=userdict['TimeCard'])
            tc.send('cmake -D BUILD_UTILS=true ..\r', expectphrase=userdict['TimeCard'])
            tc.send('cmake -D BUILD_TESTS=true ..\r', expectphrase=userdict['TimeCard'])
            tc.send('make install\r', expectphrase=userdict['TimeCard'])

        model = len(userdict['TC_SN']) == 13
        tc.send(f"cat /opt/oscillatord-{userdict['Oscillatord_Ver']}/oscillatord/example_configurations/oscillatord_default.conf > /etc/oscillatord.conf\r",
                expectphrase=userdict['TimeCard'])
        if model:
            tc.send("sed -i 's/mRO50/sa5x/g' /etc/oscillatord.conf\r", expectphrase=userdict['TimeCard'])
            tc.send("sed -i 's/disciplining=true/disciplining=false/g' /etc/oscillatord.conf\r",
                    expectphrase=userdict['TimeCard'])
        tc.send('cat /etc/oscillatord.conf\r', expectphrase=userdict['TimeCard'])


@iss_service
def oscillatord_rpm_install():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('mkdir -p /root/firmware/oscillatord/rpm/\r', expectphrase=userdict['TimeCard'])
        for _, rpm in userdict['RPM_Oscillatord'].items():
            tc.send(f"ls -l /root/firmware/oscillatord/rpm/{rpm}\r", expectphrase=userdict['TimeCard'])
            if re.search(r'No\s+such\s+file\s+or\s+directory', tc.recbuf):
                log.message(f"RPM {rpm} not found...")
                log.message(f"Need to download and recompile RMP {rpm}")
                tc.send(f"scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
                        f"{lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:"
                        f"/home/timecard/firmware/oscillatord/rpm/{rpm} /root/firmware/oscillatord/rpm/\r",
                        expectphrase=['yes/no', 'password:'])
                tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
                tc.send(f"{lib.getconnections()['Server'].password}\r", expectphrase=userdict['TimeCard'])
        for i in ['ublox', 'disciplining', 'oscillatord']:
            tc.send(f"rpm -Uvh /root/firmware/oscillatord/rpm/{userdict['RPM_Oscillatord'][i]} --force\r",
                    expectphrase=userdict['TimeCard'])

        if len(userdict['TC_SN']) == 13:
            tc.send("sed -i 's/mRO50/sa5x/g' /etc/oscillatord.conf.rpmnew\r", expectphrase=userdict['TimeCard'])
            tc.send("sed -i 's/disciplining=true/disciplining=false/g' /etc/oscillatord.conf.rpmnew\r",
                    expectphrase=userdict['TimeCard'])
        tc.send('cat /etc/oscillatord.conf.rpmnew > /etc/oscillatord.conf\r', expectphrase=userdict['TimeCard'])
        tc.send('cat /etc/oscillatord.conf\r', expectphrase=userdict['TimeCard'])


@iss_service
def driver_update():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('rm -rf /root/git/Time-Appliance-Project\r', expectphrase=userdict['TimeCard'])
        tc.send(f"scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
                f"{lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:"
                f"/home/timecard/firmware/driver/{userdict['Timecard_DRV']}/* /root/git\r",
                expectphrase=['yes/no', 'password:'])
        tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
        tc.send(f"{lib.getconnections()['Server'].password}\r", expectphrase=userdict['TimeCard'], timeout=120)
        tc.send('cd /root/git/Time-Appliance-Project/Time-Card/DRV/\r', expectphrase=userdict['TimeCard'])
        tc.send('./remake\r', expectphrase=userdict['TimeCard'], timeout=150)


@iss_service
def cid():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('ilorest bootorder\r', expectphrase=userdict['TimeCard'])
        bootorder = []
        for i in [r'(\d+)\.\s+NIC.Slot.1.1.IPv6', r'(\d+)\.\s+HD.EmbSATA']:
            number = re.search(i, tc.recbuf)
            bootorder.append(number.group(1))
        tc.send(f"ilorest bootorder [{','.join(bootorder)}] --commit\r", expectphrase=userdict['TimeCard'])
        tc.send('ilorest bootorder\r', expectphrase=userdict['TimeCard'])
        tc.send('ilorest get SecureBootStatus --selector=Bios\r', expectphrase=userdict['TimeCard'],
                check_received_string='SecureBootStatus=Disabled')
        tc.send('ilorest list Name "PhysicalPorts/MacAddress" --selector=NetworkAdapter\r',
                expectphrase=userdict['TimeCard'])
        tc.send('ilorest get Controller/Status/State --selector=EmbeddedMedia\r', expectphrase=userdict['TimeCard'],
                check_received_string='State=Enabled')
        tc.send(f"mkdir -p /root/firmware/bios\r", expectphrase=userdict['TimeCard'])
        tc.send(f"ls -l /root/firmware/bios/{userdict['Python_Bios_Script']}\r", expectphrase=userdict['TimeCard'])
        if re.search(r'No\s+such\s+file\s+or\s+directory', tc.recbuf):
            tc.send(f"scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null {lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:/home/timecard/firmware/bios/{userdict['Python_Bios_Script']} /root/firmware/bios/\r",
                    expectphrase=['yes/no', 'password:'])
            tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
            tc.send('W400admin\r', expectphrase=userdict['TimeCard'])
        tc.send(f"chmod 755 /root/firmware/bios/{userdict['Python_Bios_Script']}\r", expectphrase=userdict['TimeCard'])
        tc.send(f"python3 /root/firmware/bios/{userdict['Python_Bios_Script']}\r", expectphrase=userdict['TimeCard'],
                check_received_string=r'is\s+going\s+to\s+restart,\s+after\s+reboot\s+rerun\s+this\s+script\s+to\s+confirm\s+bios\s+settings\s+are\s+correct')


@iss_service
def oscillatord_disable_antenna():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('monitoring_client -a 0.0.0.0 -p 2958 -r gnss_stop\r', expectphrase=userdict['TimeCard'])


@iss_service
def oscillatord(mode):
    """
    Param: (mode) [ start, stop, check, disable, disciplining]
    Return: None
    """
    mode = mode.lower()
    with Oscillatord() as osc:
        if 'config' == mode:
            osc.config()
        if 'start' == mode:
            osc.start()
        elif 'stop' == mode:
            osc.stop()
        elif 'check' == mode:
            osc.check_version()
        elif 'disable' == mode:
            osc.disable_antenna()
        elif 'disciplining' == mode:
            osc.disable_antenna()


class Oscillatord(object):
    def __init__(self):
        self.userdict = lib.apdicts.userdict
        self.timecard = lib.getconnections()['TimeCard']
        self.recbuf = ''

    def __del__(self):
        self.timecard.close()

    def __enter__(self):
        self.timecard.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timecard.close()

    def _send(self, command):
        self.timecard.send(command, expectphrase=self.userdict['TimeCard'])
        self.recbuf = self.timecard.recbuf

    def config(self):
        model = len(self.userdict['TC_SN']) == 13
        self._send(f'service oscillatord stop\r')
        self._send(f"sed -i 's/disciplining={str(model).lower()}/disciplining={str(not model).lower()}/g' /etc/oscillatord.conf\r")
        self._send(f"sed -i 's/{'mRO50/sa5x' if model else 'sa5x/mRO50'}/g' /etc/oscillatord.conf\r")
        self._send('cat /etc/oscillatord.conf\r')

    def start(self):
        self.config()
        self._send(f'date -u +"%Y-%m-%d %H:%M:%S"\r')
        if _time := re.search(r'(\d+-\d+-\d+\s+\d+:\d+:\d+)', self.recbuf):
            self._send(f'nohup journalctl -S "{_time.group(1)}" -f -u oscillatord > /tmp/oscillatord.log &\r')
            self._send(f'service oscillatord start\r')
        else:
            lib.fail()

    def stop(self):
        self._send(f'service oscillatord stop\r')

    def check_version(self):
        status = []
        for k, v in self.userdict['Oscillatord'].items():
            self._send(f'dnf list --installed | grep {k} | cat\r')
            status.append(self.timecard.check_received_string(v))
        lib.fail() if not status else None

    def disable_antenna(self):
        self._send('monitoring_client -a 0.0.0.0 -p 2958 -r gnss_stop\r')

    def disciplining(self, timeout):
        with lib.TimeIt() as t:
            while t.duration <= int(timeout):
                clear_row_file()
                log.message(f"\r{f' Checking Holdover Status ':*^100}")
                self.timecard.send("echo '{}' | nc 0.0.0.0 2958\r", expectphrase=userdict['TimeCard'], timeout=60,
                                   check_not_received_string=r'Ncat:\s+Connection\s+refused')
                if value := re.search(r'"ready_for_holdover":\s+"(\S+)"', self.timecard.recbuf):
                    log.message(f'Ready For Holdover: Expect "true", Actual: "{value.group(1)}"')
                    if 'true' in value.group(1):
                        return True
                else:
                    break
                time.sleep(60)
        lib.fail()


@iss_service
def pcie_delay():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('nohup ptp4l -i ens1f0np0 -f /root/unicast-master.cfg -m > /tmp/ptp4l.log &\r',
                expectphrase=userdict['TimeCard'])
        tc.send('nohup phc2sys -s /dev/ptp6 -c CLOCK_REALTIME -O 0 -m > /tmp/phc2sys.log &\r',
                expectphrase=userdict['TimeCard'])
        tc.send('nohup ts2phc -s generic -c ens1f0np0 -m -l 7 > /tmp/ts2phc.log &\r', expectphrase=userdict['TimeCard'])


@iss_service
def mellanox_nic_set_ip_config():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('ifconfig ens1f0np0 192.168.1.200 up\r', expectphrase=userdict['TimeCard'], wait_before_send=180)
        tc.send('ping 192.168.1.100 -c 3\r', expectphrase=userdict['TimeCard'])


@iss_service
def ntp_setup():
    userdict = lib.apdicts.userdict
    chrony = ''
    chrony += 'driftfile /var/lib/chrony/drift\n'
    chrony += 'makestep 1.0 3\n'
    chrony += 'rtcsync\n'
    chrony += 'hwtimestamp ens1f0np0\n'
    chrony += 'allow 192.168.1.50\n'
    chrony += 'keyfile /etc/chrony.keys\n'
    chrony += 'leapsectz right/UTC\n'
    chrony += 'logdir /var/log/chrony\n'
    chrony += 'clientloglimit 10485760\n'
    chrony += 'leapsecmode slew\n'
    chrony += 'maxslewrate 1000\n'
    chrony += 'smoothtime 400 0.001 leaponly\n'
    chrony += 'refclock PHC /dev/ptp6 tai poll 0 trust'

    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f'echo -e {repr(chrony)} > /etc/chrony.conf\r', expectphrase=userdict['TimeCard'])
        tc.send('service chronyd stop\r', expectphrase=userdict['TimeCard'])
        tc.send('service chronyd start\r', expectphrase=userdict['TimeCard'])
        tc.send('chronyc tracking\r', expectphrase=userdict['TimeCard'], wait_before_send=5)
        tc.send('chronyc sources\r', expectphrase=userdict['TimeCard'])


@iss_service
def ntp_chrony_stop():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('service chronyd stop\r', expectphrase=userdict['TimeCard'])


@iss_service
def ntp_check():
    userdict = lib.apdicts.userdict
    limit = 50e-3
    with lib.getconnections()['TimeCard'] as tc:
        tc.send(f"curl -k https://[{lib.getconnections()['Sentinal'].host}]/api/getdata?'channel=2&datatype=2WayTE&reset=true'\r",
                expectphrase=userdict['TimeCard'])
        m = re.findall(r',(\S+)', tc.recbuf)
        _min, _max = float(min(m)), float(max(m))
        value = abs(_max - _min)
        result = value <= limit
        _table = PrettyTable(['Maximum', 'Minimum', 'Result'])
        _table.add_row([f'{_max:.7f}', f'{_min:.7f}', f"{value:.7f}({float2si(value)}) [ {'PASS' if result else 'FAIL'} ]"])
        log.message(_table.get_string(title=f"NTP Limit: [(Maximum - Minimum) <= {limit}({float2si(limit)})]/s"))
        lib.fail() if not result else None


@iss_service
def timecard_ptp_set():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        for i in range(4, 6):
            tc.send(f'~/ptp/testptp -d /dev/ptp{i} -l\r', expectphrase=userdict['TimeCard'])
            tc.send(f'~/ptp/testptp -d /dev/ptp{i} -L 0,1\r', expectphrase=userdict['TimeCard'],
                    check_received_string='set pin function okay')
            tc.send(f'~/ptp/testptp -d /dev/ptp{i} -L 1,2\r', expectphrase=userdict['TimeCard'],
                    check_received_string='set pin function okay')
            tc.send(f'~/ptp/testptp -d /dev/ptp{i} -p 1000000000\r', expectphrase=userdict['TimeCard'],
                    check_received_string='periodic output request okay')
            tc.send(f'~/ptp/testptp -d /dev/ptp{i} -l\r', expectphrase=userdict['TimeCard'],
                    check_received_string=[r'name\s+mlx5_pps0\s+index\s+0\s+func\s+1\s+chan\s+0',
                                           r'name\s+mlx5_pps1\s+index\s+1\s+func\s+2\s+chan\s+0'])


@iss_service
def hdd_format():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('lsblk -S | grep ATA | cat\r', expectphrase=userdict['TimeCard'])
        if devices := re.search(r'(\S+).+sata', tc.recbuf):
            tc.send(f'dd if=/dev/zero of=/dev/{devices.group(1)} bs=8M status=progress\r',
                    expectphrase=userdict['TimeCard'], timeout=3600)
            return True
    lib.fail()


@iss_service
def logfile():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('rm -rf /root/.ssh/known_hosts\r', expectphrase=userdict['TimeCard'])
        tc.send(f"scp -r /tmp/*.log {lib.getconnections()['Server'].user}@[{lib.getconnections()['Server'].host}]:{userdict['${Raw_logs_path}']}/\r",
                expectphrase=['yes/no', 'password:'])
        tc.send('yes\r', expectphrase='password:') if 'yes/no' in tc.recbuf else None
        tc.send('W400admin\r', expectphrase=userdict['TimeCard'],
                check_not_received_string='No such file or directory')


class ChamberInterface(object):
    def __init__(self):
        self.cb = lib.getconnections()['Chamber']
        self.userdict = lib.apdicts.userdict

    def __del__(self):
        self.cb.close()

    def __enter__(self):
        self.cb.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cb.close()

    def chamber_profile(self, temperature, ramp_rate, margin=0.2, soak=None):
        self.identify()
        self.ramp_rate(rate=ramp_rate)
        self.ramp(temperature=temperature)
        self.monitor(temperature=temperature, delay=ramp_rate, margin=margin)
        self.soak(delay=soak) if soak else None

    def identify(self):
        self.cb.send('*IDN?\n', expectphrase='\n', check_received_string='29949|29951')

    def ramp(self, temperature):
        self.cb.send(f':SOURCE:CLOOP1:SPOINT {temperature}\n', expectphrase='\n', strip_ansi=False)
        self.cb.send(f':SOURCE:CLOOP1:SPOINT?\n', expectphrase='\n', wait_before_send=2)

    def ramp_rate(self, rate):
        self.cb.send(f':SOURCE:CLOOP1:RTIME {rate}\n', expectphrase='\n', strip_ansi=False)
        self.cb.send(f':SOURCE:CLOOP1:RTIME?\n', expectphrase='\n', wait_before_send=2)

    def monitor(self, temperature, delay, margin, timeout=None):
        temperature = float(temperature)
        margin = float(margin)
        with lib.TimeIt() as t:
            while True:
                self.cb.send(':SOURCE:CLOOP1:PVALUE?\n', expectphrase='\n')
                time.sleep(1)
                if temp := re.search(r'\s(\d+\.\d+|\d+)', self.cb.recbuf):
                    temp = float(temp.group(1))
                    log.debug(f'Chamber Temp: [ {temp} C ]')
                    save_file(f'{temp} C', 'Chamber_Temp.log')
                    if temperature - margin <= temp <= temperature + margin:
                        return True
                if timeout and t.duration >= int(timeout):
                    lib.fail()
                time.sleep(int(delay))

    @staticmethod
    def soak(delay):
        log.debug(f'Soak Time: {delay}')
        time.sleep(int(delay))


# ################## Diag #############################################################################################


@iss_service
def diag_pci_scan_test():
    with Diag('b') as tc:
        tc.menu('a', check_received_string=r'\[pcie\.test_check_pcie_dev\].+PASS')
        tc.menu('b', check_received_string=r'\[timecard\.test_i2c_device_scan\].+PASS', retry=3)


@iss_service
def system_version_information_test():
    userdict = lib.apdicts.userdict
    with Diag('c') as tc:
        tc.menu('b', check_received_string=r'\[sysinfo\.get_onie_version\].+PASS')
        tc.menu('c', check_received_string=r'\[sysinfo\.get_kernel_version\].+PASS')
        tc.menu('d', check_received_string=[fr"Unidiag\s+Version:\s+\[\s+{userdict['Diag_Ver']}\s+\]",
                                            r'\[sysinfo\.get_DIAG_version\].+PASS'])
        tc.menu('e', check_received_string=r'\[timecard\.test_fpga_version_show\].+PASS')
        tc.menu('f', check_received_string=r'\[timecard\.list_timecard\].+PASS')


@iss_service
def fpga_version_test():
    userdict = lib.apdicts.userdict
    with Diag('d') as tc:
        tc.menu('b', check_received_string=[fr"FW_Version\s+{userdict['Meta_FPGA_Ver']}",
                                            r'\[timecard\.test_fpga_core_version\].+PASS'])
    add_iss_data(tc_fpga_fw_version=userdict['Meta_FPGA_Ver'])


@iss_service
def fpga_eeprom_wp_test():
    with Diag('d') as tc:
        tc.menu('c', check_received_string=r'\[timecard\.test_get_eeprom_wp_status\].+PASS')


@iss_service
def mac_test():
    with Diag('e') as tc:
        tc.menu('a', check_received_string=[r'swrev.+=(.+)\]', r'serial.+=(.+)\]',
                                            r'\[timecard\.test_MAC_device_info\].+PASS'])
        mac = dict(re.findall(r'(serial|swrev).+=(.+)]', tc.recbuf))
        add_iss_data(mac_version=mac['swrev'], mac_serial_number=mac['serial'])
        tc.menu('b', check_received_string=r'\[timecard\.test_MAC_utc\].+PASS')
        tc.menu('c', check_received_string=r'\[timecard\.test_MAC_device_init\].+PASS')
        tc.menu('d', check_received_string=r'\[timecard\.test_MAC_baud_cfg\].+PASS')


@iss_service
def gps_module_information_test():
    with Diag('f') as tc:
        tc.menu('a', check_received_string=r'\[timecard\.test_GNSS_Ver_info\].+PASS')


@iss_service
def verify_gps_antenna_detected():
    with Diag('f') as tc:
        tc.menu('b', check_received_string=r'\[timecard\.test_GNSS_ANT_info\].+PASS', wait_before_send=5, retry=20)


@iss_service
def sensor_test():
    with Diag('g') as tc:
        tc.menu('b', check_received_string=r'\[timecard\.test_lm75b_sensor\].+PASS')
        tc.menu('c', check_received_string=r'\[timecard\.test_sht3x_sensor\].+PASS')
        tc.menu('d', check_received_string=r'\[timecard\.test_icp10100_sensor\].+PASS')
        tc.menu('e', check_received_string=r'\[timecard\.test_bno080_sensor\].+PASS', timeout=120)


@iss_service
def fpga_stress_test():
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        tc.send('k', expectphrase='please select test option')
        tc.send('a', expectphrase='Please input the correct format')
        tc.send('1\r', expectphrase='Press Enter key to continue',
                check_received_string=r'\[timecard\.test_stress_fpga\].+PASS')


@iss_service
def i2c_stress_test():
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        tc.send('k', expectphrase='please select test option')
        tc.send('b', expectphrase='Please input the correct format')
        tc.send('1\r', expectphrase='Press Enter key to continue', timeout=60,
                check_received_string=r'\[timecard\.test_stress_i2c\].+PASS')


@iss_service
def check_heartbeat_led():
    userdict = lib.apdicts.userdict
    with lib.getconnections()['TimeCard'] as tc:
        tc.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        tc.send('i', expectphrase='please select test option')
        for led, i in [('red', 'b'), ('green', 'c'), ('blue', 'd'), ('off', 'a')]:
            tc.send(i, expectphrase='Press Enter key to continue',
                    check_received_string=fr'\[timecard\.test_led_{led}\].+PASS')
            tc.send('\r', expectphrase='please select test option')
            for count_error in range(11):
                answer = lib.ask_questions(question=f'Please check the color of the SMA and USB-C ports on timecard',
                                           picture_path=f"LEDs{userdict['${SUITE_NAME}']}.jpg",
                                           html='system_leds_interaction.html',
                                           timeout=10800)
                if led == answer:
                    break
                elif i == 10 or 'fail' == answer:
                    lib.fail()
                log.warning(f'Wrong answer {count_error}nd time, Please answer again.')

    if userdict['${SUITE_NAME}'] in ['FCT']:
        if 'fail' == lib.ask_questions(question=f'Please Check GPS Antenna LED is blue',
                                       picture_path='GPS_Antenna_LED.jpg', html='user_interaction.html',
                                       timeout=10800):
            lib.fail()


# ###   HI-POT #########


@iss_service
def initial_hipot_device():
    userdict = lib.apdicts.userdict
    hipot = lib.getconnections()['HiPot']
    userdict['HIPOT'] = lib.HipotHandler(driver=hipot.model, connection=hipot)


@iss_service
def test_hipot(mode):
    userdict = lib.apdicts.userdict
    if mode == 'GND':
        userdict['HIPOT'].continuity_test(current=25,
                                          voltage=8,
                                          hi_limit=100,
                                          lo_limit=0,
                                          hi_limit_v=6,
                                          lo_limit_v=0,
                                          dwell=1,
                                          offset=0,
                                          offset_v=0,
                                          frequency=60,
                                          margin_test=False)
    else:
        userdict['HIPOT'].dc_hipot_test(voltage=1450,
                                        hi_limit=5000,
                                        lo_limit=0,
                                        ramp_up=3.5,
                                        dwell=1.5,
                                        ramp_down=1,
                                        charge_lo=0,
                                        arc_sense=5,
                                        offset=0,
                                        ramp_hi=0,
                                        arc_detect='ON',
                                        continuity='OFF',
                                        range='Auto',
                                        low_range='OFF',
                                        margin_test=False)


@iss_service
def psu_cable(psu):
    if 'fail' == lib.ask_questions(question=f'Please Confirm Plug PSU{psu}',
                                   picture_path=f'PS{psu}.jpg', html='user_interaction.html',
                                   timeout=10800):
        lib.fail()


# ##########################################################################################################

class Diag(object):
    def __init__(self, menu):
        self._menu = menu
        self.diag = lib.getconnections()['TimeCard']
        self.recbuf = ''

    def __enter__(self):
        self.diag.open()
        self.diag.send('unidiag\r', expectphrase=r'timecard\s+Diag.+Main\s+Test')
        self.diag.send(f'{self._menu}', expectphrase='please select test option')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.diag.close()

    def menu(self, menu, check_received_string, timeout=30, wait_before_send=None, retry=1):
        for i in range(retry):
            self.diag.send(f'{menu}', expectphrase='Press Enter key to continue',
                           timeout=timeout,
                           wait_before_send=wait_before_send)
            self.recbuf = self.diag.recbuf
            status = self.diag.check_received_string(check_received_string)
            self.diag.send('\r', expectphrase='please select test option')
            if status:
                return True
        lib.fail()


def formatted_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}'


def float2si(number):
    number = float(number)
    units = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z', 8: 'Y', 9: 'R', 10: 'Q',
             -1: 'm', -2: 'u', -3: 'n', -4: 'p', -5: 'f', -6: 'a', -7: 'z', -8: 'y', -9: 'r', -10: 'q'}
    mantissa, exponent = f'{number:e}'.split('e')
    unit = units.get(int(exponent) // 3, None)
    return f'{float(mantissa) * 10 ** (int(exponent) % 3):01.0f}{unit}' if unit else f'{number:.5e}'


def log_message(msg):
    log.message(f'\r{f" {msg} ":*^100}')


def add_iss_data(**kwargs):
    userdict = lib.apdicts.userdict
    log.debug(f'Add ISS Data:{kwargs}')
    with open(f"/opt/Robot/BOM/{userdict['${serial_number}']}.json", 'r') as f:
        data = json.load(f)
    data.update({'ISS_DATA': {}}) if not data.get('ISS_DATA') else None
    data['ISS_DATA'].update(kwargs)
    with open(f"/opt/Robot/BOM/{userdict['${serial_number}']}.json", 'w') as f:
        f.write(json.dumps(data))


def save_file(msg, file_name):
    userdict = lib.apdicts.userdict
    raw_path = f"{userdict['${Raw_logs_path}']}/{lib.get_variable('${TEST NAME}')}"
    os.makedirs(f'{raw_path}') if not os.path.isdir(f'{raw_path}') else None
    m = '\r'.join([f'[{datetime.now().isoformat(" ")[:-3]}] | {i}' for i in msg.splitlines()])
    with open(f'{raw_path}/{file_name}', 'a+', encoding="utf-8") as f:
        f.write(f'{m}\r')


def clear_row_file():
    userdict = lib.apdicts.userdict
    raw_path = userdict['${Raw_logs_path}']
    file_name = f"{raw_path}/{lib.get_variable('${TEST NAME}')}.raw"
    os.makedirs(f'{raw_path}') if not os.path.isdir(f'{raw_path}') else None
    os.remove(file_name) if os.path.exists(file_name) else None
