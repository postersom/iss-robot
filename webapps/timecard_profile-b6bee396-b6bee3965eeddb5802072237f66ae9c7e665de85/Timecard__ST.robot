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

HPE_BIOS_iLO_and_CPLD_Firmware_Update
    timecard_lib.hpe_bios_ilo_and_cpld_fw_update

HPE_Power_Cycle_1
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp
    timecard_lib.mst_start

Timecard_FPGA_Firmware_Update
    timecard_lib.fpga_firmware_update               11:00.0

Mellanox_NIC_Firmware_Update
    timecard_lib.mlx_nic_firmware_update

Mellanox_NIC_Realtime_Clock_Enable
    timecard_lib.mlx_nic_realtime_clock_enable

Mellanox_NIC_PPS_Enable
    timecard_lib.mlx_nic_pps_enable

HPE_Power_Cycle_2
    timecard_lib.messages_delete
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

Timecard_EEPROM_Verify
    timecard_lib.eeprom_verify

Timecard_SMA_LEDs_Check
    timecard_lib.check_heartbeat_led

Timecard_USB_C_Verify
    timecard_lib.usb_c_verify

Timecard_Driver_Verify
    timecard_lib.verify_timecard_driver

System_Version_Information_Test
    timecard_lib.system_version_information_test

Timecard_PCIE_Scan_Test
    timecard_lib.diag_pci_scan_test

Timecard_Sensor_Test
    timecard_lib.sensor_test

Timecard_Verify_GPS_Antenna_Detected
    timecard_lib.verify_gps_antenna_detected

Timecard_Verify_GPS_Device_in_Timing_Mode
    timecard_lib.verify_gps_device_in_timing_mode

Timecard_MAC_Test
    timecard_lib.mac_test

Timecard_GPS_Module_Information_Test
    timecard_lib.gps_module_information_test

Timecard_FPGA_Version_Test
    timecard_lib.fpga_version_test

Timecard_FPGA_EEPROM_WP_Test
    timecard_lib.fpga_eeprom_wp_test

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

HPE_Power_Off
    timecard_lib.power_control                      off
