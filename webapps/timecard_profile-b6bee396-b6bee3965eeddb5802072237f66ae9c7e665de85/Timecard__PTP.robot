*** Settings ***
Documentation     Auto script test of Timecard project.
Suite Setup       lib.test_suite
Suite Teardown    lib.final_test_suite
Test Setup        lib.test_case
Test Teardown     lib.final_test_case
Metadata          Script Version    *${script_version}*
Metadata          Author:    *TDE*
Force Tags        ${slot_location}
Metadata          Location     ${slot_location}
Library           /opt/iss_libs/libs/lib.py
Library           ${CURDIR}/Library/timecard_config_ptp.py
Library           ${CURDIR}/Library/timecard_lib.py

*** Variables ***
${odc_family}           Timecard
${ScriptPath}           ${CURDIR}

*** Test Cases ***

ISS_Info
    timecard_config_ptp.iss_config
    timecard_lib.iss_info

HPE_Power_On
    timecard_lib.power_control          cycle
    timecard_lib.connection_check

Constant_Log_Clear
    timecard_lib.messages_delete

HPE_Power_Cycle
    timecard_lib.power_control          cycle
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp
    timecard_lib.mst_start

POST_Test
    timecard_lib.messages_log

HPE_FRU_Info
    timecard_lib.hpe_fru_info

Mellanox_NIC_Set_IP_Config
    timecard_lib.mellanox_nic_set_ip_config

Timecard_NTP_Set
    timecard_lib.ntp_setup
    sleep                               480

Timecard_NTP_Test
    timecard_lib.start_sentinel
    sleep                               1200
    timecard_lib.stop_sentinel

Timecard_NTP_Verify
    timecard_lib.ntp_chrony_stop
    timecard_lib.ntp_check

Mellanox_NIC_PTP_Set
    timecard_lib.timecard_ptp_set

Mellanox_NIC_PCIe_Delay_Test
    timecard_lib.pcie_delay

Timecard_MAC_Set
    timecard_lib.set_sma                ch=sma3         clock=MAC
    timecard_lib.set_sma                ch=sma4         clock=MAC

#Timecard_Config_MAC
#    timecard_lib.config_mac             tau=100

Timecard_Oscillatord_Version_Check
    timecard_lib.oscillatord            check

Timecard_Oscillatord_Start
    timecard_lib.oscillatord            start

Timecard_Disciplining
    sleep                               1200

Timecard_PTP_Test
    timecard_lib.start_sentinel
    sleep                               1200
    timecard_lib.stop_sentinel

Timecard_PTP_Verify
    timecard_lib.get_data_sentinel      clock=PTP      datatype=2WayTE     plus_minus=5e-6

Constant_Log_Check
    timecard_lib.messages_log
    timecard_lib.logfile

TS2PHC_Offset_Check
    timecard_lib.ts2phc_offset_check     1200

HPE_Power_Off
    timecard_lib.power_control           off
