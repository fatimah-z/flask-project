# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /flask-project
COPY requirements.txt /flask-project/requirements.txt
RUN pip install -r /flask-project/requirements.txt
ADD . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
