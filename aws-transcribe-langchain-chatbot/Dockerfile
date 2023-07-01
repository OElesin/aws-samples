FROM python:3.9.17-slim

USER root

COPY ./app /opt/app
RUN pip install -r /opt/app/requirements.txt
WORKDIR /opt/app

EXPOSE 8080
#CMD ["python", "/opt/app/webapp.py"]
ENTRYPOINT python /opt/app/webapp.py
