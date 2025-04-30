# Milk-V duo256M setup
## Create new user:
### Create home directory
```
mkdir /home
```
### Create user
```
adduser powerline
```
## Create init script that allow user write and read to the tty ports
```
vi /etc/init.d/S99devices_groups
```
insert text:
```
chgrp tty /dev/ttyS1
chmod g+wr /dev/ttyS1
chgrp tty /dev/ttyS2
chmod g+wr /dev/ttyS2
chgrp tty /dev/ttyS3
chmod g+wr /dev/ttyS3
chgrp tty /dev/ttyS4
chmod g+wr /dev/ttyS4
```
allow root execution
```
chmod u+rwx /etc/init.d/S99devices_groups
```
## Install python libraryes:
```
export MSGPACK_PUREPYTHON=true
pip install io minimalmodbus struct serial time os influxdb timeloop datetime sys
```
## Install program
```
su powerline
cd /home/powerline
```
download file from github modbus-influxdb.py

