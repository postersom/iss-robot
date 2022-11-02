*** Keywords ***
Initialize_Test_Suite
    No Operation

Final_Test_Suite
    No Operation

Verify_EEPROM_Program
    [Documentation]    For verify eeprom keyword in the text with regular expression.

    [Arguments]     ${eeprom_type}      ${text_util}      ${text_eeprom}     ${key_util}      ${key_eeprom}  
    ${status}       ${msg_list}=      verify_eeprom_util       eeprom_type=${eeprom_type}     text_util=${text_util}     
    ...             text_eeprom=${text_eeprom}      key_util=${key_util}     key_eeprom=${key_eeprom}  
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list} 

Check_Multi_Pass_Keywords_Test_All
    [Documentation]    For verify multi pass keyword in the text with regular expression.

    [Arguments]     ${text}      ${pattern}   
    ${status}       ${msg_list}=      verify_pass_keyword_in_test_all       text=${text}    pattern_list=${pattern}        
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list} 

Check_Multi_Pass_Keywords_Traffic_Test
    [Documentation]    For verify multi pass keyword in the text with regular expression.

    [Arguments]     ${text}        
    ${status}       ${msg_list}=      verify_traffic_port_keyword       text=${text}        
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list} 


Check_Set_Fan_Speed
    [Documentation]    For verify set all fan speed.

    [Arguments]     ${text}     ${speed}
    ${status}       ${msg_list}=      verify_fan_speed_keyword       text=${text}     speed=${speed}
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_Get_Fan_Speed
    [Documentation]    For verify set all fan speed.

    [Arguments]     ${text}     ${speed}
    ${status}       ${msg_list}=      verify_get_fan_speed_keyword       text=${text}     speed=${speed}
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_All_Port_Package_Count
    [Documentation]    For verify package count of all port should be equal.

    [Arguments]     ${text}     ${pattern}   ${min}    ${max}
    ${status}       ${msg_list}=      verify_all_port_package_regexp       text=${text}     pattern=${pattern}
    ...     min=${min}      max=${max} 
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_All_Port_Status
    [Documentation]    For verify all port status should be Up.

    [Arguments]     ${text}     ${check_mode}
    ${status}       ${msg_list}=      verify_all_port_up_regexp       text=${text}    check_mode=${check_mode} 
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_All_Port_Qsfp_Status_Passes
    [Documentation]    For verify all port status should be Passes.

    [Arguments]     ${text}   
    ${status}       ${msg_list}=      verify_all_port_qsfp_regexp       text=${text}    
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_Temperature
    [Documentation]    For verify all temperature monitor sensor.

    [Arguments]     ${text}      ${current_temp_range}     ${peak_temp_range}
    ${status}       ${msg_list}=      verify_temp_monitor       text=${text}    
    ...     current_temp_range=${current_temp_range}      peak_temp_range=${peak_temp_range}
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list}

Check_rtc_Datetime
    [Documentation]    For verify the rtc datetime with the current datetime on PC.

    [Arguments]     ${text}      ${pc_datetime}   
    ${status}       ${msg}=      check_rct_datetime       text_uut_time=${text}    pc_time=${pc_datetime}
    Run Keyword If    ${status}    Set_Pass     ${msg}
    ...    ELSE    Set_Fail     ${msg} 

Check_Multi_qsfp_Keywords
    [Documentation]    For verify multi pass keyword in the text with regular expression.

    [Arguments]     ${text}      ${pattern}   
    ${status}       ${msg_list}=      verify_qsfp_keyword_regexp       text=${text}    pattern=${pattern}
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list} 

Check_Multi_Pass_Keywords
    [Documentation]    For verify multi pass keyword in the text with regular expression.

    [Arguments]     ${text}      ${pattern}   
    ${status}       ${msg_list}=      verify_multi_keyword_regexp       text=${text}    pattern_list=${pattern}
    Run Keyword If    ${status}    Set_Pass     ${msg_list}
    ...    ELSE    Set_Fail_list     ${msg_list} 

Check_Pass_Keywords
    [Documentation]    For verify pass keyword in the text with regular expression.

    [Arguments]     ${text}      ${pattern}    ${pass_msg}      ${fail_msg}   
    ${status}=      verify_keyword_regexp       text=${text}    pattern=${pattern}
    Run Keyword If    ${status}    Set_Pass     ${pass_msg}
    ...    ELSE    Set_Fail     ${fail_msg} 

Check_Fail_Keywords
    [Documentation]    For verify fail keyword in the text with regular expression.

    [Arguments]     ${text}      ${pattern}    ${pass_msg}      ${fail_msg}   
    ${status}=      verify_keyword_regexp       text=${text}    pattern=${pattern}
    Run Keyword If    ${status}    Set_Fail     ${fail_msg}
    ...    ELSE    Set_Pass     ${pass_msg} 

Set_Pass
    [Documentation]    For save logs pass and set fail in robot.

    [Arguments]     ${pass_msg}
    Save_to_logs    PASSED:${SPACE * 2}${pass_msg}     verify=True

Set_Fail
    [Documentation]    For save logs fail and set fail in robot.

    [Arguments]     ${fail_msg}
    
    Save_to_logs    FAILED:${SPACE * 2}${fail_msg}     verify=True 
    Fail    ${fail_msg}

Set_Fail_list
    [Documentation]    For save logs fail and set fail in robot.

    [Arguments]     ${fail_msg_list}
    
    @{words_list}=	    Split String	${fail_msg_list}   ||
    : FOR    ${fail_msg}    IN    @{words_list}
    \   ${fail_msg_stripped}=	Strip String	${fail_msg}
    \    ${fail_msg_final}=     Set Variable    ${fail_msg_stripped}
    \    Save_to_logs    FAILED:${SPACE * 2}${fail_msg_stripped}     verify=True

    Fail    ${fail_msg_final}

Send_Expect_Prompt
    [Documentation]    For send command to UUT and expect prompt of UUT.

    [Arguments]     ${command}      ${expect}      ${time_out}=${20}       ${max_retry}=${1}

    Log     send command: ${command}
    #Save_to_logs    msg=${command}\n
    ${found}    ${response}=    ReSerial.send_expect_cmd    command=${command}    expect=${expect}    
    ...         time_out=${time_out}   max_retry=${max_retry}

    Save_to_logs    msg=${response}\n 
    Run Keyword Unless    ${found}    Set_Fail    Can not detect prompt: ${expect} !!!!

    [Return]    ${found}        ${response}
      
Initialize_Test_case
    [Documentation]    Initialize of all Test case.

    Run Keyword If    "${PREV TEST STATUS}" == "FAIL"    Fail    Skipping Testcase because the status of the previous test case is FAILED.

    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=${sharp * 25} SERIAL NUMBER: ${serial_number}${SPACE * 4}SCRIPT VERSION: ${scrip_version} ${sharp * 25}\n
    Save_to_logs    msg=${sharp * 25} ${TEST NAME} Start Test ${date_time} ${sharp * 25}\n\n\n
    ReSerial.open

Final_Test_case
    [Documentation]   End process of all Test case.

    #Run Keyword If    "${TEST STATUS}" == "FAIL"    Save_to_logs    FAILED:${SPACE * 2}${TEST MESSAGE}     verify=True

    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    Save_to_logs    msg=\n\n\n${sharp * 25} ${TEST NAME} End Test ${date_time} ${sharp * 25}\n\n\n
    ReSerial.close

Save_to_logs
    [Documentation]   Save the message to the raw logs of test case.

    [Arguments]     ${msg}      ${verify}=False

    Set Suite Variable    ${step_logs_path}    ${Raw_logs_path}${/}${TEST NAME}.txt
    Set Suite Variable    ${all_logs_path}    ${Raw_logs_path}${/}${serial_number}_All_Logs.txt 

    Run Keyword If    ${verify}    Verify_logs      ${msg}
    ...    ELSE    Raw_logs     ${msg}  

    
Raw_logs
    [Documentation]   Save the console message to the raw logs of test case.

    [Arguments]     ${msg}
    Append To File      ${step_logs_path}    ${msg}
    Append To File      ${all_logs_path}    ${msg}

Verify_logs 
    [Documentation]   Save the verify message to the raw logs of test case.

    [Arguments]     ${msg}

    ${date_time}=    Get Current Date    result_format=%Y%m%d-%H%M%S
    ${message}=     Set Variable    \n\n${date_time}${SPACE * 4}*****${SPACE * 2}${msg}${SPACE * 2}*****\n\n
    Append To File      ${step_logs_path}    ${message}
    Append To File      ${all_logs_path}    ${message}


Switch_BMC_to_CPU
    [Documentation]   Switch From BMC side to CPU side.

    [Arguments]     ${login}=False

    Run Keyword If    ${login}    Login_To_CPU
    ...    ELSE    No_Login_To_CPU

Switch_CPU_to_BMC
    [Documentation]   Switch From CPU side to BMC side.

    Send_Expect_Prompt      command= \n\n       expect=${prompt_cpu}    time_out=10
    #ReSerial.write        command=\x0C   no_lf=True
    #sleep    1s
    #ReSerial.write        command=x   no_lf=True
    #Send_Expect_Prompt      command=\n       expect=${prompt_bmc}    time_out=10


    : FOR    ${INDEX}    IN RANGE    10
    \    ${status} =    Exit_CPU
    \    Run Keyword If    ${status}    Exit For Loop
    \    Run Keyword Unless    ${status}    Continue For Loop

    Send_Expect_Prompt      command= \n       expect=${prompt_bmc}    time_out=10


Exit_CPU
    [Documentation]   Switch From CPU side to BMC side.

    ReSerial.write        command=\x0C   no_lf=True
    sleep    1s
    ReSerial.write        command=\x78   no_lf=True
    sleep    1s
    ReSerial.write        command=\x78   no_lf=True

    ${found}    ${response}=    Send_Expect_Prompt      command= \n       expect=root.*    time_out=10
    ${bmc_match} =	    Get Regexp Matches	    ${response}	    ${robot_prompt_bmc}
    ${bmc_length} =	    Get Length	    ${bmc_match}

    Run Keyword If    "${bmc_length}" == "1"    Return From Keyword    True
    ...     ELSE      Return From Keyword    False


Login_To_CPU
    [Documentation]   Switch From BMC side to CPU side.
    ...     and Login to CPU side.

    Send_Expect_Prompt      command=${sol_command}       expect=${login_prompt_cpu}    time_out=900
    Send_Expect_Prompt      command=${user_cpu}       expect=${password_prompt}    time_out=10
    Send_Expect_Prompt      command=${password_cpu}       expect=${prompt_cpu}    time_out=10
    Send_Expect_Prompt      command=dmesg -n 1          expect=${prompt_cpu}    time_out=10

No_Login_To_CPU
    [Documentation]   Switch From BMC side to CPU side.
    ...     and go to CPU side.

    Send_Expect_Prompt      command=${sol_command}       expect=${prompt_cpu}    time_out=60

Login_To_BMC
    [Documentation]   Reboot and Login to BMC side.

    [Arguments]     ${reboot}=False

    #Run Keyword If      ${reset}        Send_Expect_Prompt      command=wedge_power.sh reset -s 
    Run Keyword If      ${reboot}        Send_Expect_Prompt      command=reboot      
    ...                 expect=${login_prompt_bmc}    time_out=300
    ...    ELSE    Send_Expect_Prompt      command=\n       expect=${login_prompt_bmc}    time_out=240
    
    Send_Expect_Prompt      command=${user_bmc}       expect=${password_prompt}    time_out=10
    Send_Expect_Prompt      command=${password_bmc}       expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt      command=dmesg -n 1          expect=${prompt_bmc}    time_out=10

Reboot_To_CPU
    [Documentation]   Reboot and Login to BMC side.

    Send_Expect_Prompt      command=reboot      expect=${login_prompt_cpu}    time_out=300
    Send_Expect_Prompt      command=${user_cpu}       expect=${password_prompt}    time_out=10
    Send_Expect_Prompt      command=${password_cpu}       expect=${prompt_cpu}    time_out=10
    Send_Expect_Prompt      command=dmesg -n 1          expect=${prompt_cpu}    time_out=10

Reboot_NVMe_To_CPU
    [Documentation]     Reboot NVMe and Login to BMC side.

    Send_Expect_Prompt      command=reboot      expect=${login_prompt_nvme}     time_out=300
    Send_Expect_Prompt      command=${password_cpu}     expect=${prompt_cpu}    time_out=10
    Send_Expect_Prompt      command=dmesg -n 1          expect=${prompt_cpu}    time_out=10

 

Get_BMC_Version_and_mtd
    [Documentation]   Check the BMC version.

    #Check new version
    ${found}    ${response}=    Send_Expect_Prompt      command=cat /etc/issue       expect=${prompt_bmc}    time_out=10

    ${bmc_ver_str}=     Get Regexp Matches      ${response}      wedge400\-v(\\S+)    1
    ${bmc_ver_str_2}=      Set Variable     ${bmc_ver_str[0].replace(".", "")}
    ${stripped}=	Strip String	${bmc_ver_str_2}	mode=left   characters=0
    ${bmc_ver_unit} =	Convert To Integer	${stripped}

    #${bmc_ver_str_cfg}=     Get Regexp Matches      ${bmc_image_name}      wedge400\-v(\\S+)    1
    #${bmc_ver_str_cfg2}=      Set Variable     ${bmc_ver_str_cfg[0].replace(".", "")}
    #${stripped2}=	Strip String	${bmc_ver_str_cfg2}	mode=left   characters=0
    #${bmc_ver_cfg} =	Convert To Integer	${stripped2}

    ${mtd}=      Common_Func.set_mtd      bcm_ver_uut=${bmc_ver_unit}

    [Return]    ${mtd}

FCM_eeprom
    [Documentation]   Create EEPROM FCM config.

    Import Variables	${CURDIR}${/}..${/}Config${/}FCM_EEPROM_DATA_TEMP.py

    ${odc_fcm} =  Split String    ${odc_fcm}    ,

    #${magic_word} =   Set Variable   0xFBFB
    #${format_version} =   Set Variable   0x3
    #${product_name} =   Set Variable   WEDGE400-FCM
    #${top_level_product_part_number} =   Set Variable   N/A
    #${system_assembly_part_number} =   Set Variable    N/A
    #${facebook_pcba_part_number} =   Set Variable   13200009801
    #${facebook_pcb_part_number} =   Set Variable   13100007601
    #${odm_pcba_part_number} =   Set Variable   R1149G000301
    ${odm_pcba_serial_number} =   Set Variable   ${odc_fcm[1]}
    #${product_production_state} =   Set Variable   1
    #${product_version} =   Set Variable   2
    #${product_sub_version} =   Set Variable   0
    #${product_serial_number} =   Set Variable   N/A
    #${product_asset_tag} =   Set Variable   N/A
    #${system_manufacturer} =   Set Variable   CLS
    ${system_manufacturing_date} =  Get Current Date     result_format=%Y%m%d
    #${pcb_manufacturer} =   Set Variable   WUS
    #${assembled_at} =   Set Variable   CLS
    #${local_mac_address} =  Set Variable   N/A
    #${extended_mac_address_base} =  Set Variable   N/A
    #${extended_mac_address_size} =  Set Variable   0
    #${eeprom_location_on_fabric} =  Set Variable   FCM

    Send_Expect_Prompt    command=echo [fb] > ${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "magic_word\\t\\t\\t= ${magic_word}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "format_version\\t\\t\\t= ${format_version}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_name\\t\\t\\t= ${product_name}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "top_level_product_part_number\\t= ${top_level_product_part_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_assembly_part_number\\t= ${system_assembly_part_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcba_part_number\\t= ${facebook_pcba_part_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcb_part_number\\t= ${facebook_pcb_part_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_part_number\\t\\t= ${odm_pcba_part_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_serial_number\\t\\t= ${odm_pcba_serial_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_production_state\\t= ${product_production_state}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_version\\t\\t\\t= ${product_version}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_sub_version\\t\\t= ${product_sub_version}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_serial_number\\t\\t= ${product_serial_number}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_asset_tag\\t\\t= ${product_asset_tag}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturer\\t\\t= ${system_manufacturer}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturing_date\\t= ${system_manufacturing_date}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "pcb_manufacturer\\t\\t= ${pcb_manufacturer}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "assembled_at\\t\\t\\t= ${assembled_at}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "local_mac_address\\t\\t= ${local_mac_address}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_base\\t= ${extended_mac_address_base}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_size\\t= ${extended_mac_address_size}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "eeprom_location_on_fabric\\t= ${eeprom_location_on_fabric}">>${fcm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10

SCM_eeprom
    [Documentation]   Create EEPROM SCM config.

    Import Variables	${CURDIR}${/}..${/}Config${/}SCM_EEPROM_DATA_TEMP.py

    ${odc_scm} =  Split String    ${odc_scm}    ,

    #${magic_word} =   Set Variable   0xFBFB
    #${format_version} =   Set Variable   0x3
    #${product_name} =   Set Variable   WEDGE400-SCM
    #${top_level_product_part_number} =   Set Variable   N/A
    #${system_assembly_part_number} =   Set Variable   19001226
    #${facebook_pcba_part_number} =   Set Variable   13200010001
    #${facebook_pcb_part_number} =   Set Variable   13100007701
    #${odm_pcba_part_number} =   Set Variable   R1149G000201
    ${odm_pcba_serial_number} =   Set Variable   ${odc_scm[1]}
    #${product_production_state} =   Set Variable   1
    #${product_version} =   Set Variable   2
    #${product_sub_version} =   Set Variable   0
    ${product_serial_number} =   Set Variable   ${odc_sn}
    #${product_asset_tag} =   Set Variable   N/A
    #${system_manufacturer} =   Set Variable   CLS
    ${system_manufacturing_date} =  Get Current Date    result_format=%Y%m%d
    #${pcb_manufacturer} =   Set Variable   WUS
    #${assembled_at} =   Set Variable   CLS
    #${local_mac_address} =   Set Variable   N/A
    #${extended_mac_address_base} =   Set Variable   N/A
    #${extended_mac_address_size} =  Set Variable   0
    #${eeprom_location_on_fabric} =   Set Variable   SCM


    Send_Expect_Prompt    command=echo [fb] > ${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "magic_word\\t\\t\\t= ${magic_word}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "format_version\\t\\t\\t= ${format_version}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_name\\t\\t\\t= ${product_name}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "top_level_product_part_number\\t= ${top_level_product_part_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_assembly_part_number\\t= ${system_assembly_part_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcba_part_number\\t= ${facebook_pcba_part_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcb_part_number\\t= ${facebook_pcb_part_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_part_number\\t\\t= ${odm_pcba_part_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_serial_number\\t\\t= ${odm_pcba_serial_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_production_state\\t= ${product_production_state}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_version\\t\\t\\t= ${product_version}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_sub_version\\t\\t= ${product_sub_version}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_serial_number\\t\\t= ${product_serial_number}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_asset_tag\\t\\t= ${product_asset_tag}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturer\\t\\t= ${system_manufacturer}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturing_date\\t= ${system_manufacturing_date}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "pcb_manufacturer\\t\\t= ${pcb_manufacturer}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "assembled_at\\t\\t\\t= ${assembled_at}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "local_mac_address\\t\\t= ${local_mac_address}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_base\\t= ${extended_mac_address_base}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_size\\t= ${extended_mac_address_size}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "eeprom_location_on_fabric\\t= ${eeprom_location_on_fabric}">>${scm_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10

SMB_eeprom
    [Documentation]   Create EEPROM SMB config.

    Import Variables	${CURDIR}${/}..${/}Config${/}SMB_EEPROM_DATA_TEMP.py

    ${odc_smb} =  Split String    ${odc_smb}    ,

    ${EMAB} =	 Convert To Integer  	${odc_mac_id}	16
    ${EMAB} =  Set Variable    ${EMAB+1}
    ${EMAB} =	 Convert To Hex	  ${EMAB}
    ${length_mac} =	 Get Length 	${odc_mac_id}
    ${length_EMAB} =	 Get Length 	${EMAB}

    ${EMAB} =  Run Keyword If    ${length_mac}>${length_EMAB}   Sub_SMB_eeprom   ${length_mac}   ${length_EMAB}   ${EMAB}
        ...    ELSE     Set Variable    ${EMAB}

    #${magic_word} =   Set Variable   0xFBFB
    #${format_version} =   Set Variable   0x3
    #${product_name} =   Set Variable   WEDGE400-AC-F
    #${top_level_product_part_number} =   Set Variable   20002230
    #${system_assembly_part_number} =   Set Variable   N/A
    #${facebook_pcba_part_number} =   Set Variable   13200009401
    #${facebook_pcb_part_number} =   Set Variable   13100007201
    #${odm_pcba_part_number} =   Set Variable   R1149G000101
    ${odm_pcba_serial_number} =   Set Variable   ${odc_smb[1]}
    #${product_production_state} =   Set Variable   1
    #${product_version} =   Set Variable   1
    #${product_sub_version} =   Set Variable   0
    ${product_serial_number} =   Set Variable   ${odc_sn}
    ${product_asset_tag} =   Set Variable   ${odc_pro_ass_tag}
    #${system_manufacturer} =   Set Variable   CLS
    ${system_manufacturing_date} =   Get Current Date    result_format=%Y%m%d
    #${pcb_manufacturer} =   Set Variable   WUS
    #${assembled_at} =   Set Variable   CLS
    ${local_mac_address} =   Set Variable   ${odc_mac_id}
    ${extended_mac_address_base} =   Set Variable   ${EMAB}
    #${extended_mac_address_size} =   Set Variable   0x008F
    #${eeprom_location_on_fabric} =   Set Variable   SMB

    Send_Expect_Prompt    command=echo [fb] > ${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "magic_word\\t\\t\\t= ${magic_word}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "format_version\\t\\t\\t= ${format_version}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_name\\t\\t\\t= ${product_name}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "top_level_product_part_number\\t= ${top_level_product_part_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_assembly_part_number\\t= ${system_assembly_part_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcba_part_number\\t= ${facebook_pcba_part_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcb_part_number\\t= ${facebook_pcb_part_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_part_number\\t\\t= ${odm_pcba_part_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_serial_number\\t\\t= ${odm_pcba_serial_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_production_state\\t= ${product_production_state}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_version\\t\\t\\t= ${product_version}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_sub_version\\t\\t= ${product_sub_version}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_serial_number\\t\\t= ${product_serial_number}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_asset_tag\\t\\t= ${product_asset_tag}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturer\\t\\t= ${system_manufacturer}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturing_date\\t= ${system_manufacturing_date}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "pcb_manufacturer\\t\\t= ${pcb_manufacturer}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "assembled_at\\t\\t\\t= ${assembled_at}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "local_mac_address\\t\\t= ${local_mac_address}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_base\\t= ${extended_mac_address_base}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_size\\t= ${extended_mac_address_size}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "eeprom_location_on_fabric\\t= ${eeprom_location_on_fabric}">>${smb_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10

Sub_SMB_eeprom
    [Documentation]   Extended MAC Address.

    [Arguments]     ${length_mac}   ${length_EMAB}   ${EMAB}
    ${length} =  Set Variable   ${length_mac}-${length_EMAB}
    :FOR    ${i}    IN RANGE    ${length}
    \    ${EMAB} =  Set Variable	0${EMAB}
    Log    Exited
    [Return]    ${EMAB}

FAN_eeprom
    [Documentation]   Create EEPROM FAN config.

    [Arguments]     ${num_fan}

    Import Variables	${CURDIR}${/}..${/}Config${/}FAN_EEPROM_DATA_TEMP.py

    ${odc_fan} =  Split String    ${odc_fan${num_fan}}    ,

    ${odm_pcba_serial_number} =   Set Variable   ${odc_fan[1]}
    ${product_serial_number} =   Set Variable   ${odc_sn}
    ${system_manufacturing_date} =   Get Current Date    result_format=%Y%m%d


    Send_Expect_Prompt    command=echo [fb] > ${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "magic_word\\t\\t\\t= ${magic_word}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "format_version\\t\\t\\t= ${format_version}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_name\\t\\t\\t= ${product_name}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "top_level_product_part_number\\t= ${top_level_product_part_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_assembly_part_number\\t= ${system_assembly_part_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcba_part_number\\t= ${facebook_pcba_part_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "facebook_pcb_part_number\\t= ${facebook_pcb_part_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_part_number\\t\\t= ${odm_pcba_part_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "odm_pcba_serial_number\\t\\t= ${odm_pcba_serial_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_production_state\\t= ${product_production_state}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_version\\t\\t\\t= ${product_version}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_sub_version\\t\\t= ${product_sub_version}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_serial_number\\t\\t= ${product_serial_number}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "product_asset_tag\\t\\t= ${product_asset_tag}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturer\\t\\t= ${system_manufacturer}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "system_manufacturing_date\\t= ${system_manufacturing_date}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "pcb_manufacturer\\t\\t= ${pcb_manufacturer}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "assembled_at\\t\\t\\t= ${assembled_at}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "local_mac_address\\t\\t= ${local_mac_address}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_base\\t= ${extended_mac_address_base}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "extended_mac_address_size\\t= ${extended_mac_address_size}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10
    Send_Expect_Prompt    command=echo -e "eeprom_location_on_fabric\\t= ${eeprom_location_on_fabric}">>${fan_eeprom_cfg_path}eeprom.cfg    expect=${prompt_bmc}    time_out=10

Check_md5sum
    [Documentation]   Extended MAC Address.

    [Arguments]     ${pc_path}   ${uut_path}    ${uut_prompt}      ${uut_timeout}=60

    Save_to_logs    \n*** Run md5sum ${pc_path} in PC ***\n
    ${response} =	    Run	    md5sum ${pc_path}
    Save_to_logs    ${response}
    Check_Fail_Keywords	 text=${response}	    pattern=No such file or directory
    ...     pass_msg=${pc_path} is ready.
    ...     fail_msg=${pc_path} : No such file or directory.

    ${md5sum_pc_reg}=    Get Regexp Matches    ${response}    ([A-z0-9]{32})\\s+\\S+    1
    ${md5sum_pc}=    Set Variable    ${md5sum_pc_reg[0].strip()}

    ${found}    ${response}=    Send_Expect_Prompt    command=md5sum ${uut_path}       expect=${uut_prompt}    time_out=${uut_timeout}
    Check_Fail_Keywords	 text=${response}	    pattern=No such file or directory
    ...     pass_msg=${uut_path} is ready.
    ...     fail_msg=${uut_path} : No such file or directory.

    ${md5sum_uut_reg}=    Get Regexp Matches    ${response}    ([A-z0-9]{32})\\s+\\S+    1
    ${md5sum_uut}=    Set Variable    ${md5sum_uut_reg[0].strip()}

    Check_Pass_Keywords	 text=${md5sum_uut}	    pattern=${md5sum_pc}
    ...     pass_msg=Verify md5sum of ${md5sum_uut} is complete.
    ...     fail_msg=The md5sum mismatch : expect "${md5sum_pc}" but got "${md5sum_uut}".


Kill_PID_Process
    [Documentation]   Kill PID Process.

    [Arguments]     ${command}      ${uut_prompt}      ${retry}=3

    : FOR    ${INDEX}    IN RANGE    ${retry}
    \    ${found}    ${response}=    Send_Expect_Prompt    command=${command}    expect=${uut_prompt}     time_out=60
    \    ${status} =    Get_And_Kill_PID    text=${response}     uut_prompt=${uut_prompt} 
    \    Run Keyword If    ${status}    Exit For Loop
    \    Run Keyword Unless    ${status}    Continue For Loop

    Run Keyword If    ${status}    Set_Pass     kill process is complete.
    ...    ELSE    Set_Fail     kill process is Fail.

Get_And_Kill_PID
    [Documentation]   Switch From CPU side to BMC side.

    [Arguments]     ${text}        ${uut_prompt}
    ${pid}=    Get Regexp Matches    ${text}    (\\d+)\\s+\\S+\\s+\\d+\\s\\S+\\s+\\S+    1

    ${pid_length} =	    Get Length	    ${pid}

    Run Keyword If    "${pid_length}" == "0"    Return From Keyword    True

    : FOR    ${INDEX}    IN RANGE    ${pid_length}
    \    Send_Expect_Prompt    command=kill -9 ${pid[${INDEX}]}    expect=${uut_prompt}     time_out=60

    Return From Keyword    False
