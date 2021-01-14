import traceback
import os
from io import BytesIO, BufferedReader

import requests
from loguru import logger
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.responses import PlainTextResponse, HTMLResponse, StreamingResponse, FileResponse, RedirectResponse

# config
host = os.environ.get("PYPI_PROXY_HOST", "0.0.0.0")
port = int(os.environ.get("PYPI_PROXY_PORT", 8080))

root_dir = os.environ.get("PYPI_PROXY_ROOT_DIR") or os.path.abspath(os.path.dirname(__file__))
log_dir = os.environ.get("PYPI_PROXY_LOG_DIR") or os.path.join(root_dir, "log")
log_file = os.path.join(log_dir, "pypi_proxy.log")
log_level = os.environ.get("PYPI_PROXY_LOG_LEVEL", "ERROR")
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> \n<level>{message}</level>"
log_rotation = "00:00"
log_retention = "7 days"
log_enqueue = True

pypi_source = os.environ.get("PYPI_SOURCE", "https://pypi.org")  # 官方
# pypi_source = os.environ.get("PYPI_SOURCE", "https://pypi.doubanio.com")  # 豆瓣
# pypi_source = os.environ.get("PYPI_SOURCE", "https://mirrors.aliyun.com/pypi")  # 阿里
# pypi_source = os.environ.get("PYPI_SOURCE", "https://mirrors.cloud.tencent.com/pypi")  # 腾讯

# log
logger.add(
    log_file, 
    rotation=log_rotation,
    retention=log_retention,
    format=log_format,
    enqueue=log_enqueue, 
    level=log_level
)

# fastapi
app = FastAPI()

def write_html(package_name: str, text: str):
    try:
        parent_dir = os.path.join(root_dir, "simple")
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)
        with open(os.path.join(parent_dir, package_name + ".html"), "w")as f:
            f.write(text)
    except:
        logger.error(traceback.format_exc())


def write_file(full_path, response):
    try:
        parent_dir = os.path.dirname(full_path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)
        with open(full_path, "wb")as f:
            for item in response.iter_content(1024 * 1024):
                f.write(item)
                yield item
    except:
        os.remove(full_path)
        logger.error(traceback.format_exc())

@app.get("/ping", summary="测试网络", description="")
def ping():
    return PlainTextResponse("pong")

@app.get("/")
def index():
    return RedirectResponse("../simple")

@app.get("/simple", summary="某个包的缓存版本展示页", description="")
def package_list():
    try:
        package_list = []
        catalog = os.path.join(root_dir, "simple")
        if os.path.isdir(catalog):
            for each in os.listdir(catalog):
                package_name = each.replace(".html", "")
                package_list.append(f'<a href="../simple/{package_name}">{package_name}</a><br>')
        package_list = "".join(package_list)
        return HTMLResponse(f"""<html><head><title>Simple index</title></head><body>{package_list}</body></html>""")
    except:
        logger.error(traceback.format_exc())
        return PlainTextResponse("Package not found", status_code=404)

@app.get("/simple/{package_name}", summary="获取某个包的完整版本（最新）", description="")
def file_list(package_name: str, background_tasks: BackgroundTasks):
    try:
        url = f"{pypi_source}/simple/{package_name}"
        logger.debug(f"Get package list of {package_name}, from url: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            text = response.text.replace("https://files.pythonhosted.org", "../..")
            background_tasks.add_task(write_html, package_name, text)
            return HTMLResponse(text)
        else:
            return PlainTextResponse("Page not found", status_code=404)
    except:
        logger.error(traceback.format_exc())
        return PlainTextResponse("Page not found", status_code=404)

@app.get("/simple/cache/{package_name}", summary="获取某个包的完整版本（缓存）", description="")
def file_list_cache(package_name: str):
    try:
        html_cache = os.path.join(root_dir, "simple", package_name + ".html")
        if os.path.exists(html_cache):
            with open(html_cache)as f:
                return HTMLResponse(f.read())
        else:
            return PlainTextResponse("Page not found", status_code=404)
    except:
        logger.error(traceback.format_exc())
        return PlainTextResponse("Page not found", status_code=404)

@app.get("/packages/{p1}/{p2}/{p3}/{package_name}", summary="某个包的某个版本", description="")
def file_download(p1: str, p2: str, p3: str, package_name: str, background_tasks: BackgroundTasks):
    try:
        file_path = os.path.join(root_dir + '/packages', p1, p2, p3, package_name).replace("\\", "/")
        if os.path.exists(file_path):
            logger.debug(f"Found local file in repository for: {package_name}")
            return FileResponse(file_path, filename=package_name)
        else:
            url = f"{pypi_source}/packages/{p1}/{p2}/{p3}/{package_name}"
            logger.debug(f"Download start: {package_name}, from url: {url}")

            # response = requests.get(url)
            # if response.status_code == 200:
            #     content = response.content
            #     background_tasks.add_task(write_file, file_path, content)
            #     logger.debug(f"Download finished: {package_name}")
            #     return StreamingResponse(BytesIO(response.content))
            # else:
            #     logger.warning(f"Download error: {package_name}, fail reason: {response.text}")
            #     return PlainTextResponse("File not found", status_code=404)

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                return StreamingResponse(write_file(file_path, response))
            else:
                logger.warning(f"Download error: {package_name}, fail reason: {response.text}")
                return PlainTextResponse("File not found", status_code=404)
    except:
        logger.error(traceback.format_exc())
        return PlainTextResponse("File not found", status_code=404)
