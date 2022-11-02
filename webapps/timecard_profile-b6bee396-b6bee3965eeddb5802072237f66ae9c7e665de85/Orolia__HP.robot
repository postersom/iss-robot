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
#Variables         /opt/Robot/BOM/${serial_number}.py
Library           /opt/iss_libs/libs/lib.py
Library           ${CURDIR}/Library/timecard_config_hp.py
Library           ${CURDIR}/Library/timecard_lib.py



*** Variables ***

${odc_family}           Timecard
${ScriptPath}           ${CURDIR}

*** Test Cases ***
ISS_Info
    timecard_config_hp.iss_config
    timecard_lib.iss_info

Initial_HIPOT
    timecard_lib.initial_hipot_device

Confirm_Cable_PSU_0
    timecard_lib.psu_cable              1

Test_Ground_Bond_PSU_0
    timecard_lib.test_hipot            GND

Test_DC_Withstanding_Voltage_PSU_0
    timecard_lib.test_hipot            Voltage

Confirm_Cable_PSU_1
    timecard_lib.psu_cable              2

Test_Ground_Bond_PSU_1
    timecard_lib.test_hipot            GND

Test_DC_Withstanding_Voltage_PSU_1
    timecard_lib.test_hipot            Voltage
