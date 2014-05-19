FROM ubuntu:latest

RUN apt-get install -y python python-pip
RUN mkdir -p /var/www/flask
ADD src/ /var/www/flask/
ADD requirements.txt /var/www/flask/requirements.txt
RUN cd /var/www/flask; pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT python /var/www/flask/__init__.py
