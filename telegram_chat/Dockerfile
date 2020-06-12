FROM python:3.6.4

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /opt

RUN mkdir -p sys-screenuploader-tc
WORKDIR /opt/sys-screenuploader-tc

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
