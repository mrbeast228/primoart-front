# node builder container
FROM node:21 as builder

COPY ./apps/static/assets/ /node_build/
WORKDIR /node_build

RUN npm install --ignore-scripts


# main python container
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV DEBUG True

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /primoart
WORKDIR /primoart

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

RUN rm -rf /primoart

# copy node_modules from builder
COPY --from=builder /node_build/node_modules/ /node_modules/
