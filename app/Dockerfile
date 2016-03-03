FROM ubuntu

MAINTAINER Jeff Morgan (jeff.morgan@appdynamics.com)

################## BEGIN INSTALLATION ######################

# Add appdynamics user
RUN groupadd -r appdynamics
RUN useradd --create-home --gid appdynamics appdynamics
RUN mkdir -p /appdynamics

#RUN chown -R appdynamics.appdynamics /appdynamics

# Deploy libpam fix (allows cron to work)
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get -y build-dep pam
RUN export CONFIGURE_OPTS=--disable-audit && cd /root && apt-get -b source pam && dpkg -i libpam-doc*.deb libpam-modules*.deb libpam-runtime*.deb libpam0g*.deb

# Install packages
RUN apt-get update
RUN apt-get install -y default-jre
RUN apt-get -y install postgresql
RUN apt-get -y install build-essential
RUN apt-get -y install locate
RUN updatedb
RUN apt-get -y install nmap
RUN apt-get -y install wget
RUN apt-get -y install zip
RUN apt-get -y install unzip
RUN apt-get -y install git
RUN apt-get -y install python-dev
RUN apt-get -y install postgresql
RUN apt-get -y install libpq-dev
RUN apt-get -y install postgresql-client
RUN apt-get -y install mysql-server
RUN apt-get -y install python-mysqldb
RUN apt-get -y install siege
ADD /distribute_setup.py /tmp/
RUN python /tmp/distribute_setup.py
RUN easy_install pip
RUN pip install virtualenv
RUN pip install httpretty
RUN pip install urllib3
RUN pip install flask
RUN pip install requests
RUN pip install datetime
RUN pip install psycopg2
RUN pip install flask-mysql
RUN pip install Flask-Cache
RUN pip install elasticsearch
RUN pip install rq
RUN pip install redis

# Add app bits
ADD /src /appdynamics/src

# Install Machine Agent
ENV MACHINE_AGENT_HOME /appdynamics/MachineAgent
ADD /MachineAgent.zip /appdynamics/
RUN mkdir /appdynamics/MachineAgent
RUN unzip -o -d /appdynamics/MachineAgent /appdynamics/MachineAgent.zip
ADD /startMachineAgent.sh /appdynamics/MachineAgent/
RUN chmod 777 /appdynamics/MachineAgent/startMachineAgent.sh
ADD /killMachineAgent.sh /appdynamics/MachineAgent/
RUN chmod 777 /appdynamics/MachineAgent/killMachineAgent.sh

# Add startup script
ADD /startup.sh /appdynamics/
RUN chmod 777 /appdynamics/startup.sh
ADD /env.sh /appdynamics/
RUN chmod 777 /appdynamics/env.sh

##################### INSTALLATION END #####################
# Expose Ports
EXPOSE 5000
EXPOSE 1080
EXPOSE 22

CMD /appdynamics/startup.sh && tail -F /var/log/dmesg
