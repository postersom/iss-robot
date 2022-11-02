import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from iss_libs.libs import lib


def iss_config():
    station = lib.get_station_configuration()
    for i in range(1, 3):
        conn = station.add_container(name=f'TS{i}')
        conn.add_connection(name='HiPot',
                            port='/dev/ttyUSB0',
                            baudrate=38400,
                            protocol='serial',
                            model='hypot_ultra')
