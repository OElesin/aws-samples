FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY ./code /opt/app
WORKDIR /opt/app
RUN pip install -r /opt/app/requirements.txt


EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]