FROM python:3.6-alpine
COPY . /fastapi_pypi_proxy
WORKDIR /fastapi_pypi_proxy
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache --virtual .build-deps g++ \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/ \
    && apk del .build-deps g++ \
    && find /usr/local/lib/python3.6 -name '*.pyc' -delete \
    && rm -f /sbin/apk \
    && rm -rf /etc/apk \
    && rm -rf /lib/apk \
    && rm -rf /usr/share/apk \
    && rm -rf /var/lib/apk 
ENTRYPOINT uvicorn fastapi_pypi_proxy:create_app --host=0.0.0.0 --port=8000
