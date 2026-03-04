"""诗境漫游路由：/api/imagery/*"""
from fastapi import APIRouter
from app.services import imagery_service
from app.models import ImageryAnalyzeRequest
from app.utils import Result

router = APIRouter(prefix="/api/imagery", tags=["诗境漫游"])


@router.post("/analyze", summary="分析诗词意象")
async def analyze(req: ImageryAnalyzeRequest):
    data = await imagery_service.analyze(req)
    return Result.success(data)
