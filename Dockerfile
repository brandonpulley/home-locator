FROM python:3.6

RUN mkdir -p /srv/home-locator
WORKDIR /srv/home-locator

COPY . .
RUN apt-get -y update
RUN pip install -r requirements.txt
CMD ./start_server.sh
