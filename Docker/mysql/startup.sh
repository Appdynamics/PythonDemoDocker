#!/bin/bash

# This is a script to start Eric's MySQL server

# Start ssh
sudo /etc/init.d/ssh start

# Start MySQL
service mysql start

# Configure MySQL
sudo mysql -uroot -e "grant all on *.* to 'root'@'%'"
sudo mysql -uroot -e "create database AppDynamics"
mysql -uroot -e "FLUSH PRIVILEGES"

# Restart MySQL
service mysql restart
tail -f /var/log/mysql/error.log

