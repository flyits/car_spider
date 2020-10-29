FROM alpine
LABEL maintainer="flyits"
LABEL Email="1424071037@qq.com"

ARG ALIYUN_SOURCE="https://mirrors.aliyun.com/pypi/simple/"

RUN mkdir /workspace && cd /workspace \
    && echo "http://mirrors.aliyun.com/alpine/latest-stable/main/" > /etc/apk/repositories \
    && echo "http://mirrors.aliyun.com/alpine/latest-stable/community/" >> /etc/apk/repositories\
    && apk update \
    && apk add --no-cache python3 python3-dev py3-pip gcc openssl-dev openssl libressl libc-dev linux-headers libffi-dev libxml2-dev libxml2 libxslt-dev openssh-client openssh-sftp-server \
    && echo "nameserver 114.114.114.114" > /etc/resolv.conf \
    && pip install wheel -i $ALIYUN_SOURCE\
    && pip install scrapy -i $ALIYUN_SOURCE\
    && pip install scrapy_splash -i $ALIYUN_SOURCE\
    && pip install pymysql -i $ALIYUN_SOURCE \
    && pip install chompjs -i $ALIYUN_SOURCE \
    && pip install js2xml -i $ALIYUN_SOURCE \
    && scrapy startproject car

VOLUME /workspace

WORKDIR /workspace