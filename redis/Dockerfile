FROM ubuntu:14.04

MAINTAINER Jeff Morgan (jeff.morgan@appdynamics.com)

################## BEGIN INSTALLATION ######################

# Install Redis
RUN apt-get update && apt-get install -y redis-server

##################### INSTALLATION END #####################

# Expose Ports
EXPOSE 6379

# Start Redis
ENTRYPOINT  ["/usr/bin/redis-server"]
