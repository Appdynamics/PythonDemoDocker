source localEnv.sh

docker run -d -e PYTHON_HOST=${PYTHON_HOST} appdynamics/python-load
