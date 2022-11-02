#!/bin/bash

#
# The script to the backup logs ISS3.2.
# Modify by: Nuttapong Kaewnoi (nkaewnoi@celestica.com)


#set path
logs_path=/opt/Logs_ISS
logs_name=$(date -d "yesterday 13:00" '+%Y-%m-%d')
delete_log=$(date -d "-5 days" '+%Y-%m-%d')

cp $logs_path/logs.out $logs_path/$logs_name.out
echo "Start" > $logs_path/logs.out

if [[ -n $(ls $logs_path/$delete_log.out) ]]; then
    rm -rf $logs_path/$delete_log.out
    echo "remove $delete_log.out"
fi

echo "Done"