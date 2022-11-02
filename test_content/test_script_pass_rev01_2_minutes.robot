*** Settings ***
Documentation     This test profile for W400 Pre-FCT station.
Library           SSHLibrary
Library           OperatingSystem
Library           DateTime
Force Tags        ${slot_location}
Metadata          Location   ${slot_location}
*** Variables ***
${MTP_HOST}       10.196.9.49
${MTP_USERNAME}    tdcadmin
${MTP_PASSWORD}    Abc123admin
${user}           admin
${pass}           Abc123admin
${Log_path}       MTP_LOG/test_log.txt
@{serial_number}    ABC1   ABC2   ABC3

*** Test Cases ***
Wait_2_minutes
    Sleep       120

Get_Timestamp
    [Documentation]    Documentation Get_Timestamp 
    Log    ${timestamp}
 
