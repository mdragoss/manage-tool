FROM python:3.11-alpine AS builder

RUN apk update && apk add build-base

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv requirements > requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn


FROM python:3.11-alpine AS default

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

RUN apk add tk-dev

COPY . /app
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
