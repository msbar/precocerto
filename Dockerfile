FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
RUN mkdir /precocerto
WORKDIR /precocerto

COPY requirements.txt /precocerto/
RUN pip install -r requirements.txt
ADD . /precocerto/

# Django service
EXPOSE 8000