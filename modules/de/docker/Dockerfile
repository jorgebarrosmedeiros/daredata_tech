FROM python:3.8
USER root

COPY requirements.txt /tmp/requirements.txt
COPY airflow_connections.json /tmp/airflow_connections.json

COPY setup.sh /setup.sh
RUN chmod +x /setup.sh
RUN /setup.sh
RUN rm /tmp/requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]