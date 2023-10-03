FROM python:3.11


EXPOSE 8000

RUN mkdir /opt/app

WORKDIR /opt/app

COPY . .


RUN python3 -m pip install pipenv

RUN pipenv install --system


ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]


