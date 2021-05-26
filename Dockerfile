FROM python:3.8-slim

RUN adduser website

WORKDIR /home/website

COPY requirements.txt requirements.txt
RUN pip install -q -r requirements.txt

COPY shs-website.py .flaskenv ./

USER website

EXPOSE 5000

