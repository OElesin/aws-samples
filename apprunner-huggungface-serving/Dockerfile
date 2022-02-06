FROM deepset/haystack-cpu
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./src /opt/src
WORKDIR /opt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--port", "8000"]
