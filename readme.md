# Python Code Evaluation
This project attempts to meet the requirements of a Planet Labs Python/Flask "Take Home Code Test".

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



