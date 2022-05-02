FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/