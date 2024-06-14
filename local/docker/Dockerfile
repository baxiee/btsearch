FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && apt-get install -y \
  python python-pip mysql-server libmysqlclient-dev && apt-get clean

COPY src/deploy/requirements.txt deploy/requirements.txt
RUN pip install -r deploy/requirements.txt

COPY local/docker/entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT ["sh", "/scripts/entrypoint.sh"]

EXPOSE 8000

WORKDIR /var/code
