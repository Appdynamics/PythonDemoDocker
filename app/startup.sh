#!/bin/bash

# This is a startup script for the Python Demo app

# Source env.sh
source /appdynamics/env.sh

# Set EC2 Region variable
source /appdynamics/env.sh && sed -i "/^host/c\host = ${CONTROLLER}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^port/c\port = ${APPD_PORT}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^ssl/c\ssl = ${SSL}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^account/c\account = ${ACCOUNT_NAME}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^accesskey/c\accesskey = ${ACCESS_KEY}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^app/c\app = ${APP_NAME}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^tier/c\tier = ${TIER_NAME}" /appdynamics/src/${CONFIG_FILE}
source /appdynamics/env.sh && sed -i "/^node/c\node = ${NODE_NAME}" /appdynamics/src/${CONFIG_FILE}

if [ ${APP_FILE} == pythonapp.py ]; then
	source /appdynamics/env.sh && sed -i "s/BUNDY_APP/${BUNDY_APP}/g" /appdynamics/src/${APP_FILE}
fi

if [ ${APP_FILE} == pythonapp2.py ]; then
	source /appdynamics/env.sh && sed -i "s/PYTHON_APP/${PYTHON_APP}/g" /appdynamics/src/${APP_FILE}
fi
#sed -i 's/localhost/python_mysql/g' /appdynamics/src/demo/config.py
#sed -i 's/127.0.0.1/python_postgres/g' /appdynamics/src/demo/config.py

# Setup virtualenv
#/usr/local/bin/virtualenv /appdynamics/src/env
#source /appdynamics/src/env/bin/activate
#pip install -U appdynamics
#/appdynamics/src/env/bin/pip install --allow-external mysql-connector-python -r /appd/Python-Demo-App/requirements.txt
#/appdynamics/src/env/bin/pip install -r /appd/Python-Demo-App/requirements.txt
#cd /appdynamics/src/mysql-connector-python && /appd/Python-Demo-App/env/bin/python ./setup.py build && /appd/Python-Demo-App/env/bin/python ./setup.py install

# Install appdynamics
pip install -U appdynamics
#pip install -U appdynamics\<4.2

# Start app
echo "Using ${CONFIG_FILE} and ${APP_FILE}" > /tmp/startup.log
#pyagent run -c /appdynamics/src/${CONFIG_FILE} python /appdynamics/src/${APP_FILE}
nohup pyagent run -c /appdynamics/src/${CONFIG_FILE} python /appdynamics/src/${APP_FILE} &

# Start Machine Agent
source $MACHINE_AGENT_HOME/startMachineAgent.sh

exit 0
