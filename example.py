# import os
# os.environ['PYPI_SOURCE'] = "https://pypi.doubanio.com"
# os.environ['PYPI_PROXY_PACKAGE_DIR'] = "your_packages_store_path"
# os.environ['PYPI_PROXY_LOG_DIR'] = "your_log_store_path"
# os.environ['PYPI_PROXY_LOG_LEVEL'] = "DEBUG"

import uvicorn
from fastapi_pypi_proxy import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
