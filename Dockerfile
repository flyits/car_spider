FROM python
MAINTAINER "flyits 1424071037@qq.com"

RUN mkdir /workspace && pip install --upgrade pip
RUN pip install scrapy \
    && cd /workspace \
    && scrapy startproject car \
    && pip install selenium \
    && pip install scrapy_selenium \
    && pip install scrapy_splash \
    && pip install PyMySQL \
    && pip install js2xml

VOLUME /workspace

WORKDIR /workspace