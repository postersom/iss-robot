import timecard_lib as timecard
from libs import lib

PROD = "userdict['test_mode'] in ['Production']"


def main():
    seq = lib.SequenceDefinition(name='Scan-In ODC')
    seq.add_step(timecard.iss_info, name='ISS Info')
    seq.add_step(timecard.get_data_odc, name='Get Data ODC')
    seq.add_step(timecard.check_station, name='Check Station',  condition=PROD)
    seq.add_step(timecard.request_ticket, name='Request Ticket',  condition=PROD)
    seq.add_step(timecard.create_bom, name='Create BOM')
    seq.add_step(timecard.add_iss_data, name='Add ISS Data')
    return seq


if __name__ == '__main__':
    main()
