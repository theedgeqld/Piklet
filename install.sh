#!/bin/sh

#Ensures script is run as root
if [ $(id -u) != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

#Variables
username="pi"

#Install dependancies
sudo apt-get -qq -y --force-yes install git screen python3-smbus python-smbus i2c-tools 

#Installs the Piklet code
cd /opt
sudo git clone https://github.com/theedgeqld/Piklet

#Enables I2C & SPI
sed -i.bak "/i2c-bcm2708/d" /etc/modules
sed -i.bak "/i2c-dev/d" /etc/modules
echo "i2c-bcm2708\ni2c-dev\n" >> /etc/modules

if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
  sed -i.bak "/blacklist i2c-bcm2708/d" /etc/modprobe.d/raspi-blacklist.conf
  sed -i.bak "/blacklist spi-bcm2708/d" /etc/modprobe.d/raspi-blacklist.conf
  echo "#blacklist spi-bcm2708\n#blacklist i2c-bcm2708" >> /etc/modprobe.d/raspi-blacklist.conf
else
  echo "Driver file not found"
fi

#Generates run_server.sh
echo "#!/bin/bash\nsudo screen -dmLS PikletServer sudo python3 $pythonDir/server.py && echo Started server. Check screenlog.0 for details." > run_server.sh
chmod 755 run_server.sh

#Generates stop_server.sh
echo "#!/bin/bash\nsudo screen -X -S PikletServer kill" > stop_server.sh
chmod 755 stop_server.sh

#Generates restart_server.sh
echo "#!/bin/bash\nsudo sh stop_server.sh && sudo sh run_server.sh" > restart_server.sh
chmod 755 restart_server.sh

#Adds startup hook. Runs run_server when the user specified in the variable username logs in.
sed -i.bak "/@lxterminal.*/d" /home/$username/.config/lxsession/LXDE-pi/autostart
echo "@lxterminal -e '$PWD/run_server.sh'" >> /home/$username/.config/lxsession/LXDE-pi/autostart

#Reboots
echo "Install finished. Rebooting in 3 seconds..."
sleep 3
#sudo reboot

