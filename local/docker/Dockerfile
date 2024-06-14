FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY src/deploy/requirements.txt deploy/requirements.txt
RUN pip install -r deploy/requirements.txt

COPY src/deploy/requirements-dev.txt deploy/requirements-dev.txt
RUN pip install -r deploy/requirements-dev.txt

COPY local/docker/entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT ["sh", "/scripts/entrypoint.sh"]

EXPOSE 8000

WORKDIR /var/code
