FROM alpine:3.17 as builder

RUN apk add --no-cache python3 py3-pip libpq postgresql-client curl
RUN adduser -D mtaa

USER mtaa

WORKDIR /home/mtaa

COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD /home/mtaa/.local/bin/uvicorn app.__main__:app --reload --host 0.0.0.0
