FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE doc_managment.settings
ENV DJANGO_DEBUG 1
ENV RUN_BOT 1
RUN mkdir /doc_managment
WORKDIR /doc_managment
COPY requirements.txt /doc_managment/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /doc_managment/ 