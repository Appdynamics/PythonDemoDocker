#!/bin/bash

if [ -z "${CONTROLLER}" ]; then
        export CONTROLLER="controller";
fi

if [ -z "${APPD_PORT}" ]; then
        export APPD_PORT=8090;
fi

if [ -z "${SSL}" ]; then
        export SSL="off";
fi

if [ -z "${APP_NAME}" ]; then
        export APP_NAME="PythonApp";
fi

if [ -z "${TIER_NAME}" ]; then
        export TIER_NAME="PythonApp-Tier";
fi

if [ -z "${NODE_NAME}" ]; then
        export NODE_NAME="PythonApp-Node";
fi

if [ -z "${ACCOUNT_NAME}" ]; then
        export ACCOUNT_NAME="customer1";
fi

if [ -z "${ACCESS_KEY}" ]; then
        export ACCESS_KEY="your-account-access-key";
fi

if [ -z "${CONFIG_FILE}" ]; then
        export CONFIG_FILE="appdynamics.cfg";
fi

if [ -z "${APP_FILE}" ]; then
        export APP_FILE="pythonapp.py";
fi

if [ -z "${PYTHON_APP}" ]; then
        export PYTHON_APP="localhost";
fi

if [ -z "${BUNDY_APP}" ]; then
        export BUNDY_APP="localhost";
fi
