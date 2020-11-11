FROM docker-infra.cian.ru/python-web-build:3.8-v1 AS builder
FROM docker-infra.cian.ru/python-web-runtime:3.8-v1

# install ru_RU.UTF-8 locale
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e "s/# ru_RU\.UTF-8.*/ru_RU\.UTF-8 UTF-8/" /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV APPLICATION_NAME my-offers
