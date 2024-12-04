FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -  
RUN apt install -y nodejs