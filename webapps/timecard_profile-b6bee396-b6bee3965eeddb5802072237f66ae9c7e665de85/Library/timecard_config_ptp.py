import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from iss_libs.libs import lib


def iss_config():
    station = lib.get_station_configuration()
    for slot, plug in enumerate(list(range(1, 5)) * 3):
        slot = slot + 1
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
        conn.add_connection(name='Sentinal',
                            host='fe00::123',
                            protocol='ssh',
                            ch=1)
        conn.add_connection(name='WTI',
                            host=f'192.168.10.{2 if slot <= 4 else 3}',
                            user='super',
                            password='super',
                            local_prompt='NPS>',
                            protocol='ssh',
                            model='wti',
                            plug=f'{(plug*2)-1} {plug*2}')
