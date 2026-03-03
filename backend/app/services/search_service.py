"""检索服务"""
import re
from typing import List, Optional, Tuple
from app.database import poems_collection
from app.models import Poem


async def search_poems(q: Optional[str] = None, page: int = 1, page_size: int = 18) -> Tuple[List[Poem], int]:
    """通用检索：按诗句/诗名/作者/关键词模糊检索，带分页"""
    if not q or not q.strip():
        return await find_all_poems(page, page_size)

    term = re.escape(q.strip())
    # 使用 MongoDB $or + $regex 在服务端过滤
    query_filter = {
        "$or": [
            {"title": {"$regex": term}},
            {"author.name": {"$regex": term}},
            {"content": {"$regex": term}},
            {"tags": {"$regex": term}},
        ]
    }
    total = await poems_collection.count_documents(query_filter)
    skip = (page - 1) * page_size
    cursor = poems_collection.find(query_filter).skip(skip).limit(page_size)
    poems = []
    async for doc in cursor:
        doc["id"] = doc.pop("_id", doc.get("id"))
        poems.append(Poem(**doc))
    return poems, total


async def find_all_poems(page: int = 1, page_size: int = 18) -> Tuple[List[Poem], int]:
    """获取所有诗词（分页，按 sort_order 随机顺序）"""
    total = await poems_collection.count_documents({})
    skip = (page - 1) * page_size
    cursor = poems_collection.find().sort("sort_order", 1).skip(skip).limit(page_size)
    poems = []
    async for doc in cursor:
        doc["id"] = doc.pop("_id", doc.get("id"))
        poems.append(Poem(**doc))
    return poems, total


async def find_poem_by_id(poem_id: str) -> Optional[Poem]:
    """根据 ID 查找诗词"""
    doc = await poems_collection.find_one({"_id": poem_id})
    if not doc:
        return None
    doc["id"] = doc.pop("_id")
    return Poem(**doc)


async def find_poems_by_author(name: str, page: int = 1, page_size: int = 18) -> Tuple[List[Poem], int]:
    """根据作者名检索（分页）"""
    if not name or not name.strip():
        return await find_all_poems(page, page_size)

    term = re.escape(name.strip())
    query_filter = {"author.name": {"$regex": term}}
    total = await poems_collection.count_documents(query_filter)
    skip = (page - 1) * page_size
    cursor = poems_collection.find(query_filter).skip(skip).limit(page_size)
    poems = []
    async for doc in cursor:
        doc["id"] = doc.pop("_id", doc.get("id"))
        poems.append(Poem(**doc))
    return poems, total
