# fastapi-pypi-proxy
A pypi proxy using fastapi


## 服务端

* 模块安装
```
pip install fastapi-pypi-proxy
```

* 脚本运行
```
from fastapi_pypi_proxy import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
```

* docker 部署
```
docker-compose up -d
```

## 客户端
```
pip install package_name -i http://127.0.0.1:8000/simple 
```