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
Library           ${CURDIR}/Library/timecard_config_bi.py
Library           ${CURDIR}/Library/timecard_lib.py


*** Variables ***
${odc_family}           Timecard
${ScriptPath}           ${CURDIR}

*** Test Cases ***
ISS_Info
    timecard_config_bi.iss_config
    timecard_lib.iss_info
    lib.add_sync_containers

Power_On_UUT
    timecard_lib.power_control          cycle
    timecard_lib.connection_check

Constant_Log_Clear
    timecard_lib.messages_delete

#Timecard_Driver_Update
#    timecard_lib.driver_update
#
#Timecard_Oscillatord_RPM_Install
#    timecard_lib.oscillatord_rpm_install

Power_Cycle_UUT
    timecard_lib.power_control          cycle
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp
    timecard_lib.mst_start

HPE_FRU_Info
    timecard_lib.hpe_fru_info

Timecard_EEPROM_Verify
    timecard_lib.eeprom_verify

Timecard_FPGA_Firmware_Verify
    timecard_lib.orolia_fpga_fw_verify

Mellanox_NIC_Info
    timecard_lib.mlx_nic_info

Mellanox_NIC_PCIe_Info
    timecard_lib.mlx_pcie_info

Mellanox_NIC_ETH_Ports_Link_Check
    timecard_lib.mlx_eth_ports_link_check

Mellanox_NIC_Loopback_Test
    timecard_lib.mlx_nic_loopback_test

Timecard_MAC_Set
    timecard_lib.set_sma                ch=sma4             clock=MAC

Timecard_Oscillatord_Version_Check
    timecard_lib.oscillatord            check

Timecard_Oscillatord_Start
    timecard_lib.oscillatord            start

Timecard_Disciplining
    timecard_lib.disciplining           32400
    lib.sync_group                      Disciplining        7200

Timecard_Oscillatord_Disable_Antenna
    timecard_lib.oscillatord            disable
    lib.sync_group                      disable_antenna     600

Sentinel_Start
    timecard_lib.start_sentinel

Holdover_Test
    timecard_lib.holdover               864000
    lib.sync_group                      Holdover_Test       36000

Sentinel_Stop
    timecard_lib.stop_sentinel

Timecard_Oscillatord_Stop
    timecard_lib.oscillatord            stop
    timecard_lib.logfile

Timecard_MAC_Verify
    timecard_lib.get_data_sentinel      clock=MAC           plus_minus=40e-6        timeout=3600

Power_Off_UUT
    timecard_lib.power_control          off
