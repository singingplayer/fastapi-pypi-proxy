import os
os.environ['PYPI_PROXY_HOST'] = "127.0.0.1"
os.environ['PYPI_PROXY_PORT'] = "9090"
os.environ['PYPI_SOURCE'] = "https://pypi.doubanio.com"
os.environ['PYPI_PROXY_ROOT_DIR'] = r"C:\Users\xyzou\Desktop"
os.environ['PYPI_PROXY_LOG_LEVEL'] = "DEBUG"
import uvicorn

from fastapi_pypi_proxy import app, host, port


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port, log_level="error")
