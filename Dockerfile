FROM python:3.6-alpine
COPY . /fastapi_pypi_proxy
WORKDIR /fastapi_pypi_proxy
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps g++ \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/
