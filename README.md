# fastapi-pypi-proxy
A pypi proxy using fastapi


## install
```
pip install fastapi-pypi-proxy
```

## server

### command line
```
python example.py
```
or 

### docker
```
docker-compose up -d
```

## client
```
pip install package_name -i http://127.0.0.1:8000/simple 
```