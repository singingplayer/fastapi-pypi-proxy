from fastapi_pypi_proxy import app
import uvicorn

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    uvicorn.run(app, host=host, port=port, log_level="info")