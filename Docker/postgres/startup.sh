#!bin/bash

# Start ssh
sudo /etc/init.d/ssh start

# Start Postgres
service postgresql start
tail -f /var/log/postgresql/postgresql-9.3-main.log
