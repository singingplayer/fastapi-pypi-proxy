import traceback

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse


router = APIRouter()

@router.get("/ping", summary="测试网络", description="", response_class=PlainTextResponse)
def ping():
    return "pong"

@router.get("/simple", summary="", description="")
def simple_index():
    return {"msg": "success"}

@router.get("/simple/{package}", summary="某个包的列表", description="")
def simple_detail(package: str):
    return {"msg": "success"}

# @router.get("/packages/{path}", summary="某个包的某个版本", description="")
# def packages():
#     return {"msg": "success"}