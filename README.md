# fastapi-pypi-proxy
A pypi proxy using fastapi


## install
```
pip install fastapi-pypi-proxy
```

## server

```
from fastapi_pypi_proxy import Proxy
p = Proxy()
p.start()
```
or 

```
docker-compose up -d
```

## client
```
pip install package_name -i http://127.0.0.1:8000/simple 
```