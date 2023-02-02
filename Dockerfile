# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /flaskProject
COPY requirements.txt /flaskProject/requirements.txt
RUN pip install -r /flaskProject/requirements.txt
ADD . /flaskProject
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
