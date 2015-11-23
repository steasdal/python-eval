# Python Code Evaluation
This project attempts to meet the requirements of a Planet Labs Python/Flask "Take Home Code Test".

## Build
This Docker image is built in Travis CI:
<https://travis-ci.org/steasdal/python-eval>

## Docker Hub
... and deployed to Docker Hub:
<https://hub.docker.com/r/steasdal/python-eval/>

## Running with Python
To run this app with python, you'll need to install the following packages via pip:

   * flask
   * flask-restful
   
Clone this repo and `cd` into the directory where you've cloned it.  Run `python python-eval.py` 
and point your browser to <http://localhost:5000>

## Running with the `run-py3` script
If you've got Docker installed, feel free to try the `run-py3` bash script.  This script will 
pull a docker image with a preconfigured Python 3.5.0 environment, expose port 5000, map the 
current directory to a volume on the docker image and start the python-eval.py app with Python.

## Running the docker image
Perhaps the simplest method of running this application is to pull and run the docker image.
This app is rolled into a Docker image which is hosted on the official Docker Hub.  If you've got
docker installed, you can run the image with the following command:

    docker run -p 5000:5000 -d steasdal/python-eval
    
This image will, once pulled and running, start the python-eval app with gunicorn on port 5000.






