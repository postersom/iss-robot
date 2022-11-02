*** Settings ***
Documentation     Auto script test of W400 project.
Suite Setup       Initialize_Test_Suite
Suite Teardown    Final_Test_Suite
#Test Setup        Initialize_Test_case
#Test Teardown     Final_Test_case
Force Tags         ${slot_location}
Metadata           Location     ${slot_location}
Variables         ${CURDIR}${/}Config${/}configuration.py
Variables         ${CURDIR}${/}ODC_Script${/}BOM${/}${serial_number}.py
Variables          ${CURDIR}${/}Config${/}ConfigVariables.py   CONFIG    ${CURDIR}${/}Config${/}Test_Slot_Mapping_ST.cfg
Library           ${CURDIR}${/}Library${/}Common_Func.py
Library           String
Library           OperatingSystem
Library           DateTime
Library           Dialogs
Library           RequestsLibrary
Library           Collections
Resource          ${CURDIR}${/}Resources${/}keywords.robot
Resource          ${CURDIR}${/}Resources${/}variables.robot
Library           ${CURDIR}${/}Library${/}ReSerial.py    serialport=${com_port}    baudrate=${baudrate}
Library           ${CURDIR}${/}Library${/}Wti_ReSerial.py    serialport=/dev/ttyz08    baudrate=9600

*** Variables ***
${sharp}          \#
${scrip_version}    F5_W400_SY_V0.0.4
${package_path}     ${CURDIR}${/}Package${/}Products${/}W400${/}
${eeprom_path}     /mnt/data1/BMC_Diag/utility
${WTI_USERNAME}     super
${WTI_PASSWORD}     super
${time_out}         300
${hardware_name}     Wti

*** Test Cases ***
1.Start Testing
    [Documentation]    Sleep on 10 seconds and will power on Wti

    sleep    20 seconds

2.Check Queue to access Wti every 5 seconds
    [Documentation]    Check serial port can access before power on Wti. Interval 5 seconds

    Wait Until Keyword Succeeds    4 minutes   5 seconds        Request_access_serial_port    queue_type=request

3.Power On Wti
    [Documentation]    Test Keyword power on Wti All.

    Power_On_Wti    ${psu1_outlet} ${psu2_outlet}

4.Power Off Wti
    [Documentation]    Test Keyword power off Wti All.

    Power_Off_Wti    ${psu1_outlet} ${psu2_outlet}

5.Release Queue on finish used
    [Documentation]    Request to API for release queue access serial port.

    Wait Until Keyword Succeeds    2 minutes   2 seconds        Request_access_serial_port    queue_type=release

6.Sleep before sync point
    [Documentation]    Sleep on 2 seconds after release queue

    sleep     2 seconds 

6.End Testing
    [Documentation]    Sleep on 10 seconds and finish testing

    sleep    10 seconds

*** Keywords ***
Log_in_Wti
    [Documentation]   Login to Wti side.

    Log     send command: \n\r
    ${found}    ${response}=    Wti_ReSerial.send_expect_cmd    command=\n\r    expect=login:
    ...         time_out=10   max_retry=1

    Save_to_logs    msg=${response}\n
    Run Keyword If    ${found}    Log_in_Wti_sub_Normal
    ...    ELSE    Log_in_Wti_sub_1


Log_in_Wti_sub_1
    Log     send command: \n\r
    ${found}    ${response}=    Wti_ReSerial.send_expect_cmd    command=\n\r    expect=login:
    ...         time_out=10   max_retry=1

    Save_to_logs    msg=${response}\n
    Run Keyword If    ${found}    Log_in_Wti_sub_Normal
    ...    ELSE     Log_in_Wti_sub_2


Log_in_Wti_sub_2
    Log     send command: \n\r
    ${found}    ${response}=    Wti_ReSerial.send_expect_cmd    command=\n\r    expect=login:
    ...         time_out=10   max_retry=1

    Save_to_logs    msg=${response}\n
    Run Keyword If    ${found}    Log_in_Wti_sub_Normal
    ...    ELSE     Log_in_Wti_sub_3


Log_in_Wti_sub_3
    Log     send command: \n\r
    ${found}    ${response}=    Wti_ReSerial.send_expect_cmd    command=\n\r    expect=NPS\>
    ...         time_out=10   max_retry=1

    Save_to_logs    msg=${response}\n
    Run Keyword Unless    ${found}    Fail    Can not detect prompt: ${expect} !!!!


Log_in_Wti_sub_Normal
    [Documentation]   Normal Login to Wti side.
    Send_Expect_Prompt_Wti      command=${WTI_USERNAME}\n\r       expect=Password:    time_out=10
    Send_Expect_Prompt_Wti      command=${WTI_PASSWORD}\n\r       expect=NPS\>    time_out=10


Log_out_Wti
    [Documentation]   Logout Wti side.

    Send_Expect_Prompt_Wti      command=/x\n\r       expect=Exit Command Mode    time_out=10


Power_On_Wti
    [Documentation]   Login and power on Wti.

    [Arguments]     ${point}

    Wti_ReSerial.open
    Log_in_Wti
    Send_Expect_Prompt_Wti      command=/on ${point}\n\r       expect=Are you sure       time_out=10
    Send_Expect_Prompt_Wti      command=Y\n\r       expect=NPS\>      time_out=10
    Log_out_Wti
    Wti_ReSerial.close

Power_Off_Wti
    [Documentation]   Login and power off Wti.

    [Arguments]     ${point}

    Wti_ReSerial.open
    Log_in_Wti
    Send_Expect_Prompt_Wti      command=/off ${point}\n\r       expect=Are you sure       time_out=10
    Send_Expect_Prompt_Wti      command=Y\n\r       expect=NPS\>      time_out=10
    Log_out_Wti
    Wti_ReSerial.close


Power_Cycle_Wti
    [Documentation]   Login and power on Wti.

    [Arguments]     ${point}

    Wti_ReSerial.open
    Log_in_Wti
    Send_Expect_Prompt_Wti      command=/off ${point}\n\r       expect=Are you sure       time_out=10
    Send_Expect_Prompt_Wti      command=Y\n\r       expect=NPS\>      time_out=10
    sleep    2s
    Send_Expect_Prompt_Wti      command=/on ${point}\n\r       expect=Are you sure       time_out=10
    Send_Expect_Prompt_Wti      command=Y\n\r       expect=NPS\>      time_out=10
    Log_out_Wti
    Wti_ReSerial.close


Send_Expect_Prompt_Wti
    [Documentation]    For send command to Wti and expect prompt of Wti.

    [Arguments]     ${command}      ${expect}      ${time_out}=${20}       ${max_retry}=${1}

    Log     send command: ${command}
    #Save_to_logs    msg=${command}\n
    ${found}    ${response}=    Wti_ReSerial.send_expect_cmd    command=${command}    expect=${expect}
    ...         time_out=${time_out}   max_retry=${max_retry}

    Save_to_logs    msg=${response}\n
    Run Keyword Unless    ${found}    Fail    Can not detect prompt: ${expect} !!!!

    [Return]    ${found}        ${response}

Request_access_serial_port
    [Documentation]    Request to API for get permission on accessing serial port for using the Wti

    [Arguments]     ${queue_type}
    Create Session      create_url      http://localhost:8080/api
    &{data}=  Create Dictionary         serial_number=${serial_number}        timeout=${time_out}          type=${queue_type}      hardware_name=${hardware_name}
    &{header}=  Create Dictionary       Content-Type=application/json         Data-Type=application/json
    ${resp}=  Post Request        create_url        /queue_hardware      data=${data}       headers=${header}
    &{resp_json}=    Evaluate     json.loads($resp.content)    json
    Save_to_logs    msg=${resp}\n
    Should Be Equal       &{resp_json}[error]      ${False}

Sync_point_process
    [Documentation]    Wait other unit and go to next testing synchronous
    Create Session      create_url      http://localhost:8080/api
    &{data}=  Create Dictionary         serial_number=${serial_number}        timeout=${time_out}          slot_location=${slot_location}        setup=False
    &{header}=  Create Dictionary       Content-Type=application/json         Data-Type=application/json
    ${resp}=  Post Request        create_url        /sync_point      data=${data}       headers=${header}
    &{resp_json}=    Evaluate     json.loads($resp.content)    json
    Save_to_logs    msg=${resp}\n
    Should Be Equal       &{resp_json}[error]       ${None}