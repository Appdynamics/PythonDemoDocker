FROM ubuntu

MAINTAINER Jeff Morgan (jeff.morgan@appdynamics.com)

################## BEGIN INSTALLATION ######################

# Install packages
RUN apt-get update
RUN apt-get -y install postgresql
RUN apt-get -y install libpq-dev
RUN apt-get -y install postgresql-client

# Setup SSH
RUN apt-get -y install openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:welcome1' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Add startup script
RUN mkdir /appdynamics
ADD startup.sh /appdynamics/startup.sh
#ADD startup.sh /usr/local/bin/startup.sh
RUN chown postgres /appdynamics/startup.sh
#RUN chown postgres /usr/local/bin/startup.sh
RUN chmod 777 /appdynamics/startup.sh
#RUN chmod 777 /usr/local/bin/startup.sh

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN	/etc/init.d/postgresql start &&\
    psql --command "CREATE USER test WITH SUPERUSER PASSWORD 'test';" &&\
    createdb -O test AppDynamicsPostgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible. 
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

##################### INSTALLATION END #####################

# Expose Ports
EXPOSE 5432
EXPOSE 22

CMD /appdynamics/startup.sh
#CMD /usr/local/bin/startup.sh
