import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from iss_libs.libs import lib


def iss_config():
    station = lib.get_station_configuration()
    station.add_connection(name='Chamber',  host='192.168.10.222', protocol='telnet', port=5025, shared_conn=True)
    super_cont = station.add_super_container('CHAMBER', timeout=8)
    wti_plug = [1, 3, 5, 7] * 48
    wti_ip = [i for i in range(2, 7) for _ in range(4)]
    for group, conn_num in enumerate(range(1, 20, 5)):
        cont_objs = []
        for plug, slot in enumerate(range(conn_num, conn_num+5)):
            conn = super_cont.add_container(name=f'TS{slot}')
            conn.add_connection(name='Server',
                                host='fe00::1',
                                user='timecard',
                                password='W400admin',
                                protocol='ssh',
                                timeout=120)
            conn.add_connection(name='TimeCard',
                                host=f'fe00::{100+slot}',
                                user='root',
                                password='Abc123admin',
                                protocol='ssh',
                                timeout=120)
            conn.add_connection(name='Sentinal',
                                host=f'fe00::{123+group}',
                                protocol='ssh',
                                ch=['A', 'B', 'C', 'D', 'E', 'F'][plug])
            conn.add_connection(name='WTI',
                                host=f'192.168.10.{wti_ip[slot-1]}',
                                user='super',
                                password='super',
                                local_prompt='NPS>',
                                protocol='ssh',
                                model='wti',
                                plug=f'{wti_plug[slot-1]} {wti_plug[slot-1]+1}')
            cont_objs.append(conn)
        station.add_sync_group(name=f'Group {group+1}', containers=cont_objs, timeout=20)
