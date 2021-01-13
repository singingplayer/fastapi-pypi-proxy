import traceback

from fastapi import APIRouter


router = APIRouter()

@router.get("/ping", summary="测试网络连接", description="")
def ping():
    return {"msg": "pong"}

@router.get("/simple", summary="测试网络连接", description="")
def ping():
    return {"msg": "pong"}

@router.get("/packages", summary="测试网络连接", description="")
def ping():
    return {"msg": "pong"}