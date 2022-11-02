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
Library           ${CURDIR}/Library/timecard_config_st.py
Library           ${CURDIR}/Library/timecard_lib.py


*** Variables ***
${odc_family}           Timecard
${ScriptPath}           ${CURDIR}

*** Test Cases ***

ISS_Info
    timecard_config_st.iss_config
    timecard_lib.iss_info

HPE_Power_On
    timecard_lib.power_control                      cycle
    timecard_lib.connection_check

Constant_Log_Clear
    timecard_lib.messages_delete

HPE_Power_Cycle
    timecard_lib.power_control                      cycle
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp
    timecard_lib.mst_start

POST_Test
   timecard_lib.messages_log

HPE_Server_Info
   timecard_lib.hpe_server_info

HPE_FRU_Info
   timecard_lib.hpe_fru_info

HPE_Thermals_Health
   timecard_lib.hpe_thermals_health

HPE_Mac_Address
   timecard_lib.hpe_mac_address

HPE_Asset_Tag_Check
   timecard_lib.hpe_asset_tag_check

HPE_HDD_Check
   timecard_lib.hpe_hdd_check

Timecard_FPGA_Firmware_Verify
  timecard_lib.orolia_fpga_fw_verify

Timecard_EEPROM_Verify
   timecard_lib.eeprom_verify

Timecard_Driver_Verify
  timecard_lib.orolia_driver_verify

Timecard_PCIE_Scan_Test
   timecard_lib.pci_scan_test

Timecard_Oscillatord_Version_Check
    timecard_lib.oscillatord            check

Timecard_Oscillatord_Config
#    timecard_lib.oscillatord_config
    timecard_lib.oscillatord            config

Timecard_Integration_Test
   timecard_lib.integration_test

Mellanox_NIC_Firmware_Verify
    timecard_lib.mlx_nic_firmware_verify

Mellanox_NIC_Info
    timecard_lib.mlx_nic_info

Mellanox_NIC_PCIe_Info
    timecard_lib.mlx_pcie_info

Mellanox_NIC_ETH_Ports_Link_Check
    timecard_lib.mlx_eth_ports_link_check

Mellanox_NIC_Realtime_Clock_Verify
   timecard_lib.mlx_nic_realtime_clock_verify

Mellanox_NIC_PPS_Verify
    timecard_lib.mlx_nic_pps_verify

Mellanox_NIC_Loopback_Test
    timecard_lib.mlx_nic_loopback_test

Constant_Log_Check
    timecard_lib.messages_log

HPE_CID_Config_And_Verify
    timecard_lib.cid

HPE_Format_HDD
    timecard_lib.hdd_format

User_Interaction_Check_Cable_Before_PXE
    timecard_lib.user_interaction_pre_pxe

PXE_Boot
    timecard_lib.power_control                cycle
    sleep                                     480

User_Interaction_Check_PXE_Installation
    timecard_lib.user_interaction_post_pxe

HPE_Power_Off
   timecard_lib.power_control                   off
