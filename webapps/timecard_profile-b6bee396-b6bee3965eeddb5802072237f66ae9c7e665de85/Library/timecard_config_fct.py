import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from iss_libs.libs import lib


def iss_config():
    station = lib.get_station_configuration()
    for i in range(1, 3):
        conn = station.add_container(name=f'TS{i}')
        conn.add_connection(name='Server',
                            host='192.168.10.1',
                            user='timecard',
                            password='W400admin',
                            protocol='ssh',
                            timeout=120)
        conn.add_connection(name='TimeCard',
                            host=f'fe00::{100+i}',
                            user='root',
                            password='Abc123admin',
                            protocol='ssh')
        conn.add_connection(name='Sentinal',
                            host='fe00::123',
                            protocol='ssh')
        conn.add_connection(name='WTI',
                            host='192.168.10.2',
                            user='super',
                            password='super',
                            local_prompt='NPS>',
                            protocol='ssh',
                            model='wti',
                            plug=i)
