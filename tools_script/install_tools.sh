#!/bin/bash

#
# The script for install service ISS3.2.
# Modify by: Nuttapong Kaewnoi (nkaewnoi@celestica.com)

#install iss service
sudo cp iss /etc/init.d/
sudo chmod 777 /etc/init.d/iss
sudo mkdir /opt/Logs_ISS
sudo chmod 777 /opt/Logs_ISS
sudo ln -s /etc/init.d/iss /usr/bin/iss
sudo ln -s /etc/init.d/iss /etc/rc5.d/S02iss

#make folder for save log iss 
sudo cp create_logs.sh /usr/local/bin/
sudo chmod 777 /usr/local/bin/create_logs.sh

#write out current crontab
crontab -l > mycron
check_crontab=$(crontab -l | grep create_logs)
word_crontab='1 0 * * * /usr/local/bin/create_logs.sh'
if [[ -z $check_crontab ]]; then
    echo "Add crontab"
    echo "$word_crontab" >> mycron
    # install new cron file
    crontab mycron
else
    echo "crontab is there."
fi
rm mycron

echo "Done"