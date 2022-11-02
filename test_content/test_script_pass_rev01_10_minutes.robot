*** Settings ***
Documentation     This test profile for W400 Pre-FCT station.
Library           SSHLibrary
Library           OperatingSystem
Library           DateTime
Library           Diag_Message.py
Library           ODCServer.py   10.196.100.17   elm
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
Wait_10_minutes
    Sleep       600

Get_Timestamp
    [Documentation]    Documentation Get_Timestamp 
    Log    ${timestamp}
 