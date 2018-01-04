#!/bin/bash
#script file used for setting up rpi for digital wastebin
#as well as run daily maintainance 


# https://www.raspberrypi.org/forums/viewtopic.php?t=158976 prevent screen from going out
#https://elinux.org/RPi_Debian_Auto_Login auto login
# https://unix.stackexchange.com/questions/129143/what-is-the-purpose-of-bashrc-and-how-does-it-work .bashrc
# https://raspberrypi.stackexchange.com/questions/43720/disable-wifi-wlan0-on-pi-3 turn off wifi at boot 

#https://www.raspberrypi.org/forums/viewtopic.php?t=185867 turn off wifi atboot

#https://developers.google.com/time/guides google ntp server to time syncing
MAIN_PY_FILE_DIR="test_new_format/" 
MAIN_PY_FILE="pygame_test"
#list of necessary software
SOFTWARE=" python3 python3-pygame python-serial ufw ntp "

if [ -e /home/dwb_installed ]
then
#if [-e /home/wifi_off ]
#dtoverlay=pi3-disable-wifi
#dtoverlay=pi3-disable-bt
#/boot/config.txt
ifconfig wlan0 up
sudo service ntp restart
sudo ufw enable
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo timedatectl set-timezone US/Pacific
ifconfig wlan0 down

cd DigitalWasteBins
python3 ${MAIN_PY_FILE_DIR}${MAIN_PY_FILE}
#sudo reboot -h 24:00

else
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo apt-get install ${SOFTWARE}
sudo ufw enable 
sudo ufw status
sudo timedatectl set-timezone US/Pacific
#python3 -m pip install pygame


#/etc/udev/rules.d/99-com.rules
#ACTION=="add",SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="SCALE"

#Create symlink for the scale
lsusb
echo "ACTION==\"add\",SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6001\", SYMLINK+=\"SCALE\"" >> /etc/udev/rules.d/99-com.rules


#touch ${HOME}/dwb_installed
#sudo reboot
fi