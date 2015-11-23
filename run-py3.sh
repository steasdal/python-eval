#!/bin/bash

docker run -it --rm \
    -p 5000:5000 \
    -v $PWD:/root/python-eval \
    steasdal/python3-dev python python-eval/python-eval.py