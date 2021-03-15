import traceback
import os
from io import BytesIO, BufferedReader

import requests
from loguru import logger
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import PlainTextResponse, HTMLResponse, StreamingResponse, FileResponse, RedirectResponse

def create_app(package_dir="", log_dir="", log_level="ERROR", 
                pypi_source="https://pypi.doubanio.com"):
        root_dir = os.path.join(os.path.expanduser('~'), ".fastapi_pypi_proxy")

        package_dir = os.environ.get("PYPI_PROXY_PACKAGE_DIR", package_dir)
        print(package_dir, os.path.isdir(package_dir))
        if package_dir != "":
            package_dir = package_dir
        else:
            package_dir = os.path.join(root_dir, "packages")
        html_dir = os.path.join(package_dir, "simple")

        log_dir = os.environ.get("PYPI_PROXY_LOG_DIR", log_dir)
        if log_dir != "":
            log_dir = log_dir
        else:
            log_dir = os.path.join(root_dir, "logs")
        log_file = os.path.join(log_dir, "fastapi_pypi_proxy.log")
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> \n<level>{message}</level>"
        log_rotation = "00:00"
        log_retention = "7 days"
        log_enqueue = True
        log_level = os.environ.get("PYPI_PROXY_LOG_LEVEL", log_level)

        # pypi_source = os.environ.get("PYPI_SOURCE", "https://pypi.org")  # 官方
        # pypi_source = os.environ.get("PYPI_SOURCE", "https://mirrors.aliyun.com/pypi")  # 阿里
        # pypi_source = os.environ.get("PYPI_SOURCE", "https://mirrors.cloud.tencent.com/pypi")  # 腾讯
        pypi_source = os.environ.get("PYPI_SOURCE", pypi_source)  # 豆瓣

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
                if not os.path.isdir(html_dir):
                    os.makedirs(html_dir)
                with open(os.path.join(html_dir, package_name + ".html"), "w")as f:
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

        @app.get("/favicon.ico")
        def favicon():
            return

        @app.get("/simple", summary="某个包的缓存版本展示页", description="")
        def package_list():
            try:
                package_list = []
                if os.path.isdir(html_dir):
                    for each in os.listdir(html_dir):
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
                html_cache = os.path.join(html_dir, package_name + ".html")
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
                file_path = os.path.join(package_dir, p1, p2, p3, package_name)
                if os.path.isfile(file_path):
                    logger.debug(f"Found local file in repository for: {package_name}")
                    return FileResponse(file_path, filename=package_name)
                else:
                    url = f"{pypi_source}/packages/{p1}/{p2}/{p3}/{package_name}"
                    logger.debug(f"Download start: {package_name}, from url: {url}")

                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        return StreamingResponse(write_file(file_path, response))
                    else:
                        logger.warning(f"Download error: {package_name}, fail reason: {response.text}")
                        return PlainTextResponse("File not found", status_code=404)
            except:
                logger.error(traceback.format_exc())
                return PlainTextResponse("File not found", status_code=404)

        return app
    # def run(self):
    #     uvicorn.run(app, host=host, port=port)
