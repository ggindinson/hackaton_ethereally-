FROM python:3.11 as compile-image

WORKDIR /sam_mj
COPY . /sam_mj
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y git
RUN python -m pip install --upgrade pip && \
	pip install poetry && \
	poetry config virtualenvs.create false && \
	poetry install
