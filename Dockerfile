FROM python:3.6-alpine
COPY . /fastapi_pypi_proxy
WORKDIR /fastapi_pypi_proxy
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/
