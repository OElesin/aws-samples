FROM node:16.3-alpine3.12 as build
WORKDIR /app
COPY ./ /app

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools && pip install -r requirements.txt

RUN cd frontend && npm run build 

WORKDIR /app/api

EXPOSE 8000

CMD [ "uvicorn", "search:app", "--host", "0.0.0.0", "--port", "8000" ]