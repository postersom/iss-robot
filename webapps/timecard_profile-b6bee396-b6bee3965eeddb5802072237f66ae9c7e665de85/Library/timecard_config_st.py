import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from iss_libs.libs import lib


def iss_config():
    station = lib.get_station_configuration()
    wti_plug = [1, 3, 5, 7] * 32
    wti_ip = [i for i in range(2, 8) for _ in range(4)]
    for wti, slot in enumerate(range(1, 13)):
        conn = station.add_container(name=f'TS{slot}')
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
        conn.add_connection(name='WTI',
                            host=f'192.168.10.{wti_ip[wti]}',
                            user='super',
                            password='super',
                            local_prompt='NPS>',
                            protocol='ssh',
                            model='wti',
                            plug=f'{wti_plug[wti]} {wti_plug[wti]+1}')