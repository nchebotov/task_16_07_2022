# syntax=docker/dockerfile:1
# pull official base image
FROM python:3.10.2-slim

MAINTAINER Chebotov Nikita 'nikitacebotov0@gmail.com'
COPY ./ .
# set work directory
WORKDIR ./app

EXPOSE 80

# install dependencies
RUN -m pip install --upgrade pip
COPY /templates/req.txt .
RUN pip3 install -r req.txt

CMD [ "python", "./__main__.py" ]