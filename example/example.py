import uvicorn
from fastapi_pypi_proxy import app, host, port


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port, log_level="info")
