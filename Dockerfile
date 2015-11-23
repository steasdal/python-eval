FROM steasdal/python3-dev

MAINTAINER Sam Teasdale <samuel.teasdale@gmail.com>

COPY python-eval.py /root/python-eval/

WORKDIR python-eval

# CMD ["gunicorn", "-b", "0.0.0.0:5000", "python-eval:app" ]
CMD ["python", "python-eval.py"]