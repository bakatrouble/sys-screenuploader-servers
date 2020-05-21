FROM python:3.6.4-alpine3.7

# RUN apk add --no-cache git

COPY req req

RUN pip3 install -r req/local_dir.txt

WORKDIR /opt

RUN mkdir -p sys-screenuploader-servers
WORKDIR /opt/sys-screenuploader-servers

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
