# ISS Robot   
   
#Examples   
https://github.com/nmusatti/connexion-sqlalchemy-example   
https://realpython.com/flask-connexion-rest-api/   

### Docker ###
docker build -t robot-python .     
docker run -v ./robot/webapps/:/usr/src/app -v ./robot/test_content:/opt/Robot_Debug  -v ./robot/logs_content:/opt/Logs_Robot -it --rm --name robot-app -p 80:8080 robot-python /bin/bash    
python app.py    
- excecute docker  
docker exec -it robot-app /bin/bash  
    
### Manual Install ###   
- Program only run on user mode (no sudo run)    
- Set Permission log folders and another project that needs to create file with user permision (ex. BOM, Logs)   
  
-------  
   
How to deploy   
- set proxy   
[proxy for apt command]   
/etc/apt/apt.conf    
Acquire::http::proxy "http://USER:PASS@10.196.4.215:8080";   
Acquire::https::proxy "https://USER:PASS@10.196.4.215:8080";   
[proxy for pip and Internet]   
export http_proxy=http://USER:PASS@10.196.4.215:8080/   
export https_proxy=https://USER:PASS@10.196.4.215:8080/  
export no_proxy=localhost,127.0.0.0,127.0.1.1,127.0.1.1,local.home
- Install virtual-env for python   
sudo apt install python3-venv   
- Install python3-dev    
sudo apt install python3-dev   
## offline install 
[download python3-dev depends on python3 version on machine link ]
sudo dpkg -i FILE_PACKAGE.deb

- Create virtual Enviroment (default path: ~/)   
cd ~/   
python3 -m venv env   
- Activate virtual Enviroment    
source ~/env/bin/activate   
- Install python packages   
[move to git repo folder]   
pip install -r /PATH/TO/FILE/requirements.txt   

## offline install package   
pip install --no-deps --no-index --find-links=/DIR/DOWNLOAD/PACKAGE -r requirements.txt

- clone code from git (default path: ~/Documents/git/)  
mkdir ~/Documents/git/  
cd ~/Documents/git/  
git clone http://REPO_PATH_WEBAPPS iss-robot
git clone http://REPO_PATH_ROBOT_TEST_CONTENT Robot
sudo cp -R Robot /opt/

- create test structure in git and files to debug path (Linux: /opt/Robot_Debug)  
[move to git repo folder]  
sudo cp -R test_content /opt/Robot_Debug # copy all files in test_content to debug robot folder  

#Create Logs folder
[move to git repo folder]  
sudo cp -R logs_content /opt/Logs_Robot 

#change owner Logs folder   

sudo chown -R $USER:$USER /opt/Logs_Robot 
sudo chown -R $USER:$USER /opt/Robot_Debug
sudo chown -R $USER:$USER /opt/Robot/Logs

#Enable web-app config files  
[move to git repo folder]  
mv webapps/.env.example webapps/.env  
  
#git clone profile  
git clone http://issrobot:Abc123admin@110.164.64.68/celestica/iss-robot-sample-profile.git robot  
#Run webapp
[move to git repo folder]  
python webapps/app.py  
#service file run webapps
[systemd]
- copy  
sudo cp tools_script/iss-robot-d.service /etc/systemd/user  
- run cmd  
systemctl --user start|stop|restart|status iss-robot-d.service  
- view logs  
journalctl -r --user-unit iss-robot-d.service  
