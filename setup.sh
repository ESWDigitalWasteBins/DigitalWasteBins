#!/bin/bash
#script file used for setting up rpi for digital wastebin

#list of necessary software
SOFTWARE=" python3 python3-pygame python-serial "
sudo apt-get update
sudo apt-get dist-upgrade -y 
sudo apt-get install ${SOFTWARE}
#python3 -m pip install pygame

lsusb
cd /lib/udev/rules.d/
ACTION=="add", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="my_uart"
