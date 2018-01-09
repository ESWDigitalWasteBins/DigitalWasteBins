#!/bin/bash
#script file used for setting up rpi for digital wastebin
#as well as run daily maintainance 

#https://elinux.org/RPi_Debian_Auto_Login auto login

MAIN_PY_FILE_DIR="test_new_format" 
MAIN_PY_FILE="pygame_test.py"

#list of necessary software
SOFTWARE=" python3 python3-pygame python-serial ufw ntp python3-pip "

#time for the computer to sleep
REBOOT_TIME="24:00" 

#quit if there is any error
set -e 

if [ -e /home/${USER}/dwb_installed ]
then
sudo ifconfig wlan0 up
sudo service ntp restart
sudo ufw enable
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo timedatectl set-timezone US/Pacific
sudo ifconfig wlan0 down
shutdown -r ${REBOOT_TIME}
cd /home/${USER}/DigitalWasteBins
python3 ${MAIN_PY_FILE_DIR}/${MAIN_PY_FILE}



else
#change password from default
echo "Please enter password"
passwd

#update and install the necessary software
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo apt-get install ${SOFTWARE}
python3 -m pip install pyserial
#enable firewall
sudo ufw enable 
sudo ufw status

#set the correct timezone to California
sudo timedatectl set-timezone US/Pacific

#disable bluetooth after reboot
echo "dtoverlay=pi3-disable-bt" | sudo tee --append /boot/config.txt

#enable auto-login
# sed -i -e '/autologin-user/s/#//' -e '/autologin-user/s/$/pi' /etc/lightdm/lightdm.conf

#Create symlink for the scale, note that the ATTRS{idProduct} needs to be 
#changed for different scales
echo "ACTION==\"add\",SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6001\", SYMLINK+=\"SCALE\"" >> /etc/udev/rules.d/99-com.rules

echo "Setup done, the system will now reboot"

#touch ${HOME}/dwb_installed
sudo reboot
fi