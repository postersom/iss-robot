*** Settings ***
Documentation     Auto script test of W400 project.
Metadata          Script Version    *0.0.1 test*

Library           String
Library           OperatingSystem
Library           DateTime
Library           BuiltIn
Library           RequestsLibrary
Force Tags        ${slot_location}
Metadata          Location   ${slot_location}
Resource          ${CURDIR}${/}Resources${/}keywords.robot

*** Variables ***
${test_time}        10
${serial_number}


*** Test Cases ***
Wait_0.5_minutes
    Sleep       30

Wait_1_minutes
    Sleep       60

1.TEST_CREATE
    USER_INTERACTION        title=FAN TRAY 4 LEDs BLUE COLOR CHECK
    ...             question_msg=Please check all 4 Fan_tray LEDs of the UUT should be Blue.
    ...             image_name=Fan_Tray_4_LEDS_Test_Blue.jpg      retry=3h      retry_interval=2s
    ...             pass_msg=Test Fan_tray 4 LEDs (Blue) is PASSES.
    ...             fail_msg=Test Fan_tray LEDs (Blue) is FAILED.
    Sleep      2
 
Wait_0.5_minutes_2
    Sleep       30

list_file
    @{items} =	OperatingSystem.List Directory           ${CURDIR} 
    :FOR  ${item}  IN  @{items} 
    \     Append To File    ${Log_path}    ${item} 
    \     Save_to_logs    msg=${item}\n\n\n 


*** Keywords ***
USER_INTERACTION
    [Documentation]    USER INTERACTION.

    [Arguments]     ${title}    ${question_msg}      ${image_name}      ${retry}      ${retry_interval}
    ...             ${pass_msg}      ${fail_msg}

    CREATE_USER_INTERACTION     title=${title}    question_msg=${question_msg}      image_name=${image_name}
    Sleep      2

    ${answer}     ${reason} =     Wait Until Keyword Succeeds    ${retry}     ${retry_interval}        CHECK_USER_INTERACTION
    Run Keyword If    "${answer}" == "pass"    Set_Pass     ${pass_msg}
    ...    ELSE     Set_Fail_USER_INTERACTION     ${fail_msg}     ${reason}

CREATE_USER_INTERACTION
    [Documentation]    CREATE USER INTERACTION.

    [Arguments]     ${title}    ${question_msg}      ${image_name}

    Create Session      create_url      http://localhost:${port_api}/api
    &{data}=  Create Dictionary         slot_location_no=${slot_location}        message=${question_msg}
    ...     timeout=100        picture=${image_name}        title=${title}
    &{header}=  Create Dictionary       Content-Type=application/json         Data-Type=application/json
    ${resp}=  Post Request        create_url        /user_interaction      data=${data}       headers=${header}
    Should Contain        ${resp.text}        interaction complete

CHECK_USER_INTERACTION
    Create Session      create_session      http://localhost:${port_api}/api
    &{data}=  Create Dictionary       slot_location_no=${slot_location}
    &{header}=  Create Dictionary       Content-Type=application/json         Data-Type=application/json
    ${resp}=  Get Request        create_session        /user_interaction     params=${data}    headers=${header}
    Log to console       ${resp.text}
    Should Contain       ${resp.text}       "answer":

    ${match}	${answer} =
    ...	    Should Match Regexp	    ${resp.text}	    \\"answer\\"\\:\\s+\\"(\\S+)\\"

    ${match}	${reason} =
    ...	    Should Match Regexp	    ${resp.text}	    \\"reason\\"\\:\\s+\\"(.*)\\"

    [Return]    ${answer}     ${reason}

Set_Fail_USER_INTERACTION
    [Documentation]    SET FAIL USER INTERACTION.

    [Arguments]     ${fail_msg}     ${reason}

    Save_to_logs    FAILED:${SPACE * 2}${fail_msg} : ${reason}     verify=True
    Fail    ${fail_msg} : ${reason}

 
Save_to_logs
    [Documentation]   Save the message to the raw logs of test case.

    [Arguments]     ${msg}      ${verify}=False

    Set Suite Variable    ${step_logs_path}    ${Raw_logs_path}${/}${TEST NAME}.txt
    Set Suite Variable    ${all_logs_path}    ${Raw_logs_path}${/}${serial_number}_All_Logs.txt

    Run Keyword If    ${verify}    Verify_logs      ${msg}
    ...    ELSE    Raw_logs     ${msg}
 
