#!bin/bash

# Start ssh
/etc/init.d/ssh start

# Start Postgres
su - postgres -c 'service postgresql restart'
tail -f /var/log/postgresql/postgresql-9.3-main.log
