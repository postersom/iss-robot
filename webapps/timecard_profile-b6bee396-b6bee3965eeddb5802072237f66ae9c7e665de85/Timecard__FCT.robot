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
Library           ${CURDIR}/Library/timecard_config_fct.py
Library           ${CURDIR}/Library/timecard_lib.py



*** Variables ***
${odc_family}           Timecard
${ScriptPath}           ${CURDIR}

*** Test Cases ***
ISS_Info
    timecard_config_fct.iss_config
    timecard_lib.iss_info

Power_On_UUT
    timecard_lib.power_control                      cycle
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp

Timecard_EEPROM_Programming
   timecard_lib.eeprom_programming
   timecard_lib.eeprom_verify

Timecard_FPGA_Firmware_Update
    timecard_lib.fpga_firmware_update               02:00.0

Power_Cycle_UUT
    timecard_lib.power_control                      cycle
    timecard_lib.connection_check
    timecard_lib.modprobe_ptp_ocp

PCIE_Scan_Test
    timecard_lib.pci_scan_test

Timecatd_Driver_Verify
    timecard_lib.verify_timecard_driver

EEPROM_Verify
    timecard_lib.eeprom_verify

FPGA_Firmware_Verify
    timecard_lib.fpga_firmware_verify               aa000000

Verify_PCA9546_I2C_Bus
    timecard_lib.verify_pca9546_i2c_bus

Verify_GNSS_Module_and_Atomic_Clock_Present
    timecard_lib.verify_gnss_module_and_atomic_clock_present

Verify_Time_Card_GPS_Locked
   timecard_lib.verify_time_card_gps_locked

Verify_GPS_Device_in_Timing_Mode
   timecard_lib.verify_gps_device_in_timing_mode

Verify_MAC
   timecard_lib.verify_mac

Config_MAC
   timecard_lib.config_mac

EEPROM_I2C_Bus_Test
    timecard_lib.eeprom_i2c_bus_test

TauPps0_100_MAC_Config
    timecard_lib.config_mac             tau=100

SMA1_MAC_Set
    timecard_lib.set_sma                ch=sma1     clock=MAC

SMA2_10Mhz_Set
    timecard_lib.set_sma                ch=sma2     clock=10Mhz

SMA3_10Mhz_Set
    timecard_lib.set_sma                ch=sma3     clock=10Mhz

SMA4_MAC_Set
    timecard_lib.set_sma                ch=sma4     clock=MAC

Disciplining_10_Minute
    sleep                               600

SMA_All_Test
    timecard_lib.start_sentinel
    sleep                               120
    timecard_lib.stop_sentinel

SMA1_MAC_Verify
    timecard_lib.get_data_sentinel      clock=MAC       plus_minus=100e-9   ch=A

SMA2_10Mhz_Verify
    timecard_lib.get_data_sentinel      clock=10Mhz     plus_minus=100e-9   ch=B

SMA3_10Mhz_Verify
    timecard_lib.get_data_sentinel      clock=10Mhz     plus_minus=100e-9   ch=C

SMA4_MAC_Verify
    timecard_lib.get_data_sentinel      clock=MAC       plus_minus=100e-9   ch=D

Check_Heartbeat_LED
    timecard_lib.check_heartbeat_led

Power_Off_UUT
    timecard_lib.power_control          off
