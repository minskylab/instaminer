FROM python:3.9-alpine

WORKDIR /app

RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add postgresql-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "run.py"]
