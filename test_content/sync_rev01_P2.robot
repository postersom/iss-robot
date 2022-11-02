*** Settings ***
Documentation     Auto script test of W400 project.
Metadata          Script Version    *0.0.1 test*
Library           String
Library           OperatingSystem
Library           DateTime
Library           BuiltIn
Library           RequestsLibrary
Library           Collections
Force Tags        ${slot_location}
Metadata          Location    ${slot_location}
Test Setup        Final_Test_case
Test Teardown       Initialize_Test_case

*** Variables ***
${Log_path}           MTP_LOG/test_log.txt
${sharp}              \#
${serial_number}
${time_out}           60
${queue_type}
${url}             http://localhost:8080/api

*** Test Cases ***
<<<<<<< HEAD
1.SYNC_POINT_INTERVAL_2s
[Documentation]    test sync point process with request to API on every 2 second
    Sleep           5 seconds
    Wait Until Keyword Succeeds    2 minutes   2 seconds        SYNC_POINT
    sleep           5 seconds
    
*** Keywords ***
Initialize_Test_case
    [Documentation]    Save the message to the raw logs of test case.
    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=${sharp * 25} %{TEST NAME} Start Test ${date_time} ${sharp * 25}\n\n\n
=======
SLEEP_20s
    [Documentation]    Documentation Get_Timestamp
    Execute_Get_Timestamp
    Log    ${timestamp}
    Sleep               ${test_time}

SYNC_POINT_INTERVAL_2s
    [Documentation]    test Core profile
    Wait Until Keyword Succeeds    2 minutes    2 seconds        POST_API_TEST_CORE

Get_Timestamp2
    [Documentation]    Documentation Get_Timestamp
    Execute_Get_Timestamp
    Log    ${timestamp}

*** Keywords *** 
POST_API_TEST_CORE
    Create Session      createcar       http://127.0.0.1:${port_api}/api
    &{data}=  Create Dictionary    serial_number=${serial_number}     slot_location=${slot_location}     setup=True        timeout=60
    &{header}=  Create Dictionary     Content-Type=application/json     Data-Type=application/json
    ${resp}=  Post Request      createcar       /sync_point     data=${data}       headers=${header} 
    Should Contain      ${resp.text}        false

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
>>>>>>> b21b40427045a8d7bf092c2609abed190964978a

Final_Test_case
    [Documentation]    End process of all Test case.
    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=\n\n\n${sharp * 25} ${TEST NAME} End Test ${date_time} ${sharp * 25}\n\n\n

REQUEST_ACCESS_HARDWARE
    Create Session      create_url      http://localhost:8080/api
    &{data}=  Create Dictionary         serial_number=${serial_number}        timeout=${time_out}          type=${queue_type}
    &{header}=  Create Dictionary       Content-Type=application/json         Data-Type=application/json
    ${resp}=  Post Request        create_url        /queue_hardware      data=${data}       headers=${header}
    &{test1}=    Evaluate     json.loads($resp.json())    json
    Log to console        &{test1}[error] 
    Should Be Equal       &{test1}[error]    ${False}

SYNC_POINT
    Create Session      createcar       ${url}
    &{data}=  Create Dictionary    serial_number=${serial_number}     slot_location=${slot_location}      setup=False        timeout=${time_out}
    &{header}=  Create Dictionary     Content-Type=application/json     Data-Type=application/json
    ${resp}=  Post Request      createcar       /sync_point     data=${data}       headers=${header}
    &{res_json}=    Evaluate    json.loads($resp.content)    json 
    Should Be Equal      &{res_json}[error]        ${None}

Save_to_logs
    [Documentation]   Save the message to the raw logs of test case.
    [Arguments]     ${msg}
    Append To File      ${Raw_logs_path}${/}${TEST NAME}.txt    ${msg}
    Append To File      ${Raw_logs_path}${/}${serial_number}.txt    ${msg}


