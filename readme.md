# Python Code Evaluation
This project attempts to address the requirements of a [Planet Labs](https://www.planet.com/) 
Python/Flask "Take Home Code Test".

## Project Structure
This project is structured as follows:

   * **Main app/Contollers** - The main app and the web service endpoint contollers are in `python-eval.py`
   * **Database** - You'll find a fake database layer and bootstrap data in `database/fake_db.py`
   * **Tests** - Tests are in the `tests/` directory.

#### Build
This Docker image is built in Travis CI:
<https://travis-ci.org/steasdal/python-eval>

#### Docker Hub
... and deployed to Docker Hub:
<https://hub.docker.com/r/steasdal/python-eval/>

## Running the web service

### Running with Python
To run this web service with python, you'll need to install the following packages via pip:

   * flask
   * flask-restful
   
Clone this repo, `cd` into the directory where you've cloned it and run Python thusly:

    python python-eval.py

and point your browser to <http://localhost:5000>


### Running with the `run-py3` script
If you've got Docker installed, feel free to try the `run-py3` bash script.  This script will 
pull a docker image with a preconfigured Python 3.5.0 environment, expose port 5000, map the 
current directory to a volume on the docker image and start the python-eval.py app with Python.

### Running the docker image
Perhaps the simplest method of running this web service is to pull and run the docker image.
This web service is rolled into a Docker image which is hosted on the official Docker Hub.  
If you've got docker installed, you can run the image with the following command:

    docker run -p 5000:5000 -d steasdal/python-eval
    
This image will, once pulled and running, start the python-eval web service with python on port 5000.

### Accessing the hosted web service
Even simpler yet, this web service is hosted on AWS and available at the following URL:

<http://ec2-54-175-118-93.compute-1.amazonaws.com:5000>

You might want to start with these endpoints:

   * Users:  <http://ec2-54-175-118-93.compute-1.amazonaws.com:5000/users>
   * Groups:  <http://ec2-54-175-118-93.compute-1.amazonaws.com:5000/groups>

Your first request may take a few seconds to execute if the web service hasn't
been accessed in a while (which is quite likely).  All subsequent requests, however,
should be nice 'n fast once the web service has spun up and shaken off the cobwebs.

## Testing the web service
All tests are run by pytest during [the build](https://travis-ci.org/steasdal/python-eval).

### Testing with pytest
The test suite is designed to be run with **pytest** which you'll need to install
via pip.  With pytest installed, run all tests by executing the following command
from the project's root directory:

    py.test
    
### Testing with the `test-py3` script
If you've got Docker installed, try running the `test-py3` script.  This'll pull
a docker image with a properly configured Python 3.5.0 environment with pytest
already installed and run the py.test command to kick off all discoverable tests.

## Endpoints
This web services provides the following endpoints for your perusal and enjoyment.
All responses are JSON.  POSTs and PUTs require a `Content-Type` header set to `application/json`

    GET /
        The root endpoint.  This'll return a greeting and some 
        HATEOAS style links for the `users` and `groups` endpoints.

    GET /users/
        Returns user records for all users.
        
    POST /users/
        Create a new user.  Set the Content-Type header to application/json.  
        The POST body will need to be in the following format:

        {
            "userid": "hsolo",
            "first_name": "Han",
            "last_name": "Solo",            
            "groups": ["users", "pirates"]
        }
        
        Possible errors:
            400 - One or more groups are invalid (do not currently exist)
            409 - you've attempted to create a user with an existing userid

    GET /users/<userid>
        Returns the user record for a particular user.
        
        Possible errors:
            404 - Unable to find user with this userid
           
    PUT /users/<userid>
        Update the user record for a particular user.  The body of the PUT request
        will be identical to the body for the /users/ POST request less the userid.  
        Set the Content-Type header to application/json.
        
        {
            "first_name": "Juan",
            "last_name": "Yolo",            
            "groups": ["users", "execs", "pirates"]
        }
        
        Possible errors:
            400 - One or more groups are invalid (do not currently exist)
            404 - Unable to find a user with this userid
        
    DELETE /users/<userid>
        Delete a user record for a user.
        
        Possible errors:
            404 - Unable to find a user with this userid
            
    GET /groups/
        Retrieve a list of all groups
        
    POST /groups/
        Create a new group record.  Set the Content-Type header to application/json.
        The body of the request will need to be in the following format:
        
        {
            "name": "scoundrels"
        }
       
        Possible errors:
            409 - A group with this name already exists.
            
    GET /groups/<group name>
        Return a list of userids for all users that are members of this group.
        
        Possible errors:
            404 - Unable to find a group with this group name
            
    PUT /groups/<group name>
        Update group membership.  Set the Content-Type header to application/json.
        The body of this PUT will be a list of userids that will, if this PUT is
        successful, now be members of this particular group.  The format of the
        PUT body will be formatted thusly:
        
        {
            "userids": [ 
                "jsmith", 
                "jjones", 
                "kwilliams"
            ]
        }
        
        Possible errors:
            404 - A group with this group name does not exist 
                  or one or more of the userids do not exist
                  
    DELETE /groups/<group name>
        Delete a group.  This will update group membership for all users that
        are currently members of this group.
        
        Possible errors:
            404 - A group with this group name does not exist
    
