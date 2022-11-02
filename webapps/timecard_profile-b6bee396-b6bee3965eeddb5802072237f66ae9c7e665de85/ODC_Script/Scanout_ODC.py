import sys
import json
import timecard_lib as timecard
from libs import lib

PROD = "userdict['test_mode'] in ['Production'] and userdict['result'] not in ['F']"


def main():
    seq = lib.SequenceDefinition(name='Scan-Out ODC')
    seq.add_step(timecard.iss_info, name='ISS Info')
    seq.add_step(timecard.check_station, name='Check Station',  condition=PROD)
    seq.add_step(timecard.check_ticket, name='Check Ticket', condition=PROD)
    seq.add_step(timecard.get_xml_data, name='Create XML', condition=PROD)
    seq.add_step(timecard.put_data, name='Put Data ODC', condition=PROD)
    seq.add_step(timecard.remove_bom, name='Remove BOM')
    seq.add_step(timecard.finalization, name='Finalization')
    return seq


if __name__ == '__main__':
    main()
