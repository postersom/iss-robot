*** Settings ***
Documentation     This test profile for W400 Pre-FCT station.
Library           SSHLibrary
Library           OperatingSystem
Library           DateTime
Library           Process
Library           Diag_Message.py
Library           Collections
Library           ODCServer.py   10.196.100.17   elm
Force Tags        ${slot_location}
Metadata          Location   ${slot_location}
Test Teardown     Final_Test_case
Test Setup      Initialize_Test_case


*** Variables ***
${MTP_HOST}       10.196.9.49
${MTP_USERNAME}    tdcadmin
${MTP_PASSWORD}    Abc123admin
${user}           admin
${pass}           Abc123admin
${Log_path}       MTP_LOG/test_log.txt
@{serial_number}    ABC1   ABC2   ABC3 
${sharp}        \#


*** Test Cases ***
Get_Timestamp
    [Documentation]    Documentation Get_Timestamp
    Execute_Get_Timestamp
    Log    ${timestamp}

1.Current_directory
    [Documentation]    Documentation Get_Timestamp
    Execute_Get_Timestamp
    Log    ${timestamp}

2.list_file
    @{items} =	OperatingSystem.List Directory           ${CURDIR} 
    :FOR  ${item}  IN  @{items} 
    \     Append To File    ${Log_path}    ${item} 
    \     Save_to_logs    msg=${item}\n\n\n 

2.Check_process
    Execute_Upload_Diag

3.Test_command_1
    Wait Until Keyword Succeeds   30 seconds    5 seconds   Execute_cmd   pwd

3.Test_command_2
    Execute_cmd    ps aux

4.Get_serial_number
    Execute_get_serial_number    @{serial_number}[2]

*** Keywords ***
MTP_Login
    Open Connection    ${MTP_HOST}
    Login    ${MTP_USERNAME}    ${MTP_PASSWORD}

Execute_Check_ODC
    Connect
    Check Connection
    ${console} =  So Type Check   UAMCTH171800021
    Append To File    ${Log_path}    A : ${console}
    Append To File    ${Log_path}    \n
    ${console} =  get_profile_parameter   PRCCTH184100035   GET_LAST_MAC_PRM
    Append To File    ${Log_path}    B : ${console}
    Append To File    ${Log_path}    \n
    ${console} =  get_profile_parameter   PRCCTH184100035   CONTROL_MACID   &MACID=08:9E:08:E8:05:FD
    Append To File    ${Log_path}    C : ${console}
    Append To File    ${Log_path}    \n



Execute_Get_Timestamp
    ${timestamp} =  Get Current Date
    ${timestamp} =  Convert Date    ${timestamp}    result_format=%d%m%Y_%H%M%S
    Append To File    ${Log_path}    ${timestamp}
    Append To File    ${Log_path}    \n
    Set Global Variable    ${timestamp}

Execute_Upload_Diag
    ${console} =  Execute Command    lsb_release -a
    Append To File    ${Log_path}    ${console}
    Append To File    ${Log_path}    \n
    LOG    ${console}

Execute_cmd
    [Arguments]    ${cmd}
    Append To File    ${Log_path}    ${cmd}
    ${console} =  Execute Command    ${cmd}
    Append To File    ${Log_path}    ${console}
    Append To File    ${Log_path}    \n
    LOG    ${console}

Execute_get_serial_number
    [Arguments]    ${serial}
    Append To File    ${Log_path}    ${serial}
    Append To File    ${Log_path}    \n

Final_Test_case
    [Documentation]   End process of all Test case.

    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=\n\n\n${sharp * 25} ${TEST NAME} End Test ${date_time} ${sharp * 25}\n\n\n 

Save_to_logs
    [Documentation]   Save the message to the raw logs of test case.

    [Arguments]     ${msg}

    Append To File      ${Raw_logs_path}${/}${TEST NAME}.txt    ${msg}
    Append To File      ${Raw_logs_path}${/}${serial_number}.txt    ${msg}

Initialize_Test_case
    [Documentation]    Initialize of all Test case.

    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=${sharp * 25} ${TEST NAME} Start Test ${date_time} ${sharp * 25}\n\n\n 

