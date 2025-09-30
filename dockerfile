FROM python:3.12


#install ssh client

RUN apt-get update && apt-get install -y openssh-client

#set enviroment variable

ENV PYTHONUNBUFFERED 1

#set the working directory

WORKDIR /apps

#copy requirements.txt file

COPY requirements.txt /apps/requirements.txt

#install python depencies

RUN pip install -r requirements.txt

# copy the application to the working directory
COPY ./apps /apps

#start the SSH tunnel

CMD python manage.py runserver 0.0.0.0:8000