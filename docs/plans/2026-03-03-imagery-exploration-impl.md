# 诗境漫游 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an interactive poetry imagery exploration feature that uses AI to extract imagery nodes from poems and renders them as an explorable star map.

**Architecture:** New backend `imagery_service` + `imagery` router following the existing service/router pattern (lazy singleton AsyncOpenAI, Result wrapper). Frontend: new `ImageryView` page with `ImageryStarMap` (pure CSS/SVG radial layout) and `ImageryDetail` (tabbed detail panel). No new dependencies.

**Tech Stack:** FastAPI + AsyncOpenAI (backend), Vue 3 + Tailwind CSS + inline SVG (frontend)

---

### Task 1: Backend — Add ImageryAnalyzeRequest model

**Files:**
- Modify: `backend/app/models/request.py` (append new class)
- Modify: `backend/app/models/__init__.py` (add to imports + __all__)

**Step 1: Add model to request.py**

Append to the end of `backend/app/models/request.py`:

```python
class ImageryAnalyzeRequest(BaseModel):
    """意象分析请求"""
    poem_text: str = Field(..., min_length=1, max_length=2000, description="诗词文本")
    title: str = Field("", description="诗词标题")
    author: str = Field("", description="作者")
    poem_id: Optional[str] = Field(None, description="已有诗词 ID（可选）")
```

**Step 2: Export from models/__init__.py**

Add `ImageryAnalyzeRequest` to the import line and `__all__` list in `backend/app/models/__init__.py`, following the existing pattern.

**Step 3: Commit**

```bash
git add backend/app/models/request.py backend/app/models/__init__.py
git commit -m "feat(imagery): add ImageryAnalyzeRequest model"
```

---

### Task 2: Backend — Create imagery_service.py

**Files:**
- Create: `backend/app/services/imagery_service.py`
- Modify: `backend/app/services/__init__.py` (add import)

**Step 1: Create the service**

Create `backend/app/services/imagery_service.py` following the `assistant_service.py` pattern:

```python
"""诗境漫游 — 意象分析服务"""
import json
import logging
from typing import Optional
from openai import AsyncOpenAI
from app.config import settings
from app.models.request import ImageryAnalyzeRequest

logger = logging.getLogger(__name__)

_client: Optional[AsyncOpenAI] = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )
    return _client


IMAGERY_SYSTEM_PROMPT = """你是一位古典诗词意象分析专家。用户会给你一首诗词，你需要分析其中的核心意象并以 JSON 格式返回。

要求：
1. 提取 3-6 个核心意象节点（如月、霜、雁、柳等具象事物或意境）
2. 每个意象节点包含：
   - name: 意象名称（1-3字）
   - category: 分类（天象/地理/植物/动物/气象/人事/器物/情感）
   - significance: 该意象在本诗中的作用（一句话）
   - cultural_meaning: 该意象在中国古典文学中的文化含义与演变（200-300字）
   - related_poems: 包含同一意象的其他 2-3 首名篇，每首含 title/author/dynasty/quote
   - connections: 与本诗中其他意象的关联（名称列表）
3. 提供 poem_summary: 全诗概述（2-3句话）

严格按以下 JSON 格式返回，不要添加任何其他文字：
{
  "poem_summary": "...",
  "imagery_nodes": [
    {
      "name": "月",
      "category": "天象",
      "significance": "...",
      "cultural_meaning": "...",
      "related_poems": [
        {"title": "...", "author": "...", "dynasty": "...", "quote": "..."}
      ],
      "connections": ["霜", "乡"]
    }
  ]
}

注意：related_poems 必须是真实存在的诗词，不确定的请标注"(待核实)"。"""


async def analyze(req: ImageryAnalyzeRequest) -> dict:
    """分析诗词意象"""
    poem_desc = req.poem_text
    if req.title:
        poem_desc = f"《{req.title}》" + (f" — {req.author}" if req.author else "") + f"\n{req.poem_text}"

    try:
        client = _get_client()
        resp = await client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": IMAGERY_SYSTEM_PROMPT},
                {"role": "user", "content": f"请分析以下诗词的意象：\n\n{poem_desc}"},
            ],
            temperature=0.4,
            max_tokens=3000,
        )
        raw = (resp.choices[0].message.content or "").strip()

        # 解析 JSON — 处理 markdown 代码块包裹的情况
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            raw = raw.rsplit("```", 1)[0]
        raw = raw.strip()

        data = json.loads(raw)
        # 校验基本结构
        if "imagery_nodes" not in data or not isinstance(data["imagery_nodes"], list):
            raise ValueError("invalid response structure")

        return data

    except json.JSONDecodeError as e:
        logger.warning("Imagery analysis JSON parse failed: %s", e)
        return _fallback_analysis(req)
    except Exception as e:
        logger.warning("Imagery analysis failed: %s", e)
        return _fallback_analysis(req)


def _fallback_analysis(req: ImageryAnalyzeRequest) -> dict:
    """降级：返回基础分析框架"""
    return {
        "poem_summary": f"「{req.title or '此诗'}」意境深远，值得细细品味。（AI 分析暂时不可用）",
        "imagery_nodes": [
            {
                "name": "全诗",
                "category": "情感",
                "significance": "诗词整体意境",
                "cultural_meaning": "中国古典诗词讲究意境营造，通过具象事物表达抽象情感，形成独特的审美体验。建议您在 AI 恢复后重新分析。",
                "related_poems": [],
                "connections": [],
            }
        ],
        "fallback": True,
    }
```

**Step 2: Register in services/__init__.py**

Add `imagery_service` to the import and `__all__` in `backend/app/services/__init__.py`.

**Step 3: Commit**

```bash
git add backend/app/services/imagery_service.py backend/app/services/__init__.py
git commit -m "feat(imagery): add imagery_service with LLM analysis"
```

---

### Task 3: Backend — Create imagery router + wire to main.py

**Files:**
- Create: `backend/app/routers/imagery.py`
- Modify: `backend/app/routers/__init__.py`
- Modify: `backend/app/main.py`

**Step 1: Create router**

Create `backend/app/routers/imagery.py`:

```python
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
```

**Step 2: Register in routers/__init__.py**

Add `from .imagery import router as imagery_router` and update `__all__`.

**Step 3: Include in main.py**

Add `imagery_router` to the import line and add `app.include_router(imagery_router)`.

**Step 4: Commit**

```bash
git add backend/app/routers/imagery.py backend/app/routers/__init__.py backend/app/main.py
git commit -m "feat(imagery): add /api/imagery/analyze endpoint"
```

---

### Task 4: Frontend — Create api/imagery.js

**Files:**
- Create: `frontend/src/api/imagery.js`

**Step 1: Create API module**

Create `frontend/src/api/imagery.js`:

```javascript
import request from './index'

/**
 * 分析诗词意象
 * @param {{ poem_text: string, title?: string, author?: string, poem_id?: string }} params
 * @returns {{ poem_summary: string, imagery_nodes: Array }}
 */
export function analyzeImagery(params) {
  return request.post('/imagery/analyze', params, { timeout: 60000 })
}
```

**Step 2: Commit**

```bash
git add frontend/src/api/imagery.js
git commit -m "feat(imagery): add frontend imagery API"
```

---

### Task 5: Frontend — Create ImageryStarMap.vue component

**Files:**
- Create: `frontend/src/components/imagery/ImageryStarMap.vue`

**Step 1: Create the star map visualization component**

This is the core visual component. It receives `imagery_nodes` as a prop and renders:
- A center node (poem title)
- Surrounding imagery nodes in radial layout
- SVG lines connecting related nodes
- Click handler emits `select` event

Key implementation details:
- Compute node positions using `Math.cos/sin` with even angle distribution
- SVG overlay for connection lines
- Staggered fade-in animation via `transition-delay`
- On desktop: radial layout. On mobile (detected via container width): vertical list
- Node colors cycle through project palette: gold (#c8851a), vermilion (#e54d42), cyan (#12aa9c), bamboo (#5b6e4b)
- Selected node gets a glow ring

Props: `{ nodes: Array, title: String }`
Emits: `select(node)`

**Step 2: Commit**

```bash
git add frontend/src/components/imagery/ImageryStarMap.vue
git commit -m "feat(imagery): add ImageryStarMap visualization component"
```

---

### Task 6: Frontend — Create ImageryDetail.vue component

**Files:**
- Create: `frontend/src/components/imagery/ImageryDetail.vue`

**Step 1: Create the detail panel component**

A slide-up panel that shows when a node is selected. Contains 3 tabs:
1. **文化含义** — Shows `cultural_meaning` text
2. **关联诗句** — Lists `related_poems` with clickable items (emit `go-poem` event)
3. **意境配图** — Has a "生成配图" button that calls the existing image generation API

Props: `{ node: Object }` (the selected imagery node)
Emits: `close`, `go-poem(poem)`

Key details:
- Tab switching with animated underline indicator
- Related poems show title/author/dynasty/quote
- Image generation uses existing `/api/image/generate` with a prompt derived from the imagery name + cultural meaning
- Slide-up animation, click-outside-to-close

**Step 2: Commit**

```bash
git add frontend/src/components/imagery/ImageryDetail.vue
git commit -m "feat(imagery): add ImageryDetail panel component"
```

---

### Task 7: Frontend — Create ImageryView.vue page

**Files:**
- Create: `frontend/src/views/explore/ImageryView.vue`

**Step 1: Create the main page**

Page structure:
1. Header with title "诗境漫游" + subtitle
2. Input area: textarea for poem text + title/author fields + "开始探索" button
3. Loading state: skeleton + "正在解读意境..."
4. Result state: `<ImageryStarMap>` + `<ImageryDetail>` (conditional)

The page also reads `route.query.poem` and `route.query.title` / `route.query.author` to auto-populate from poem detail page navigation.

Key flow:
```
input → click "开始探索" → loading=true → call analyzeImagery() → loading=false → show star map
→ click node → selectedNode = node → show ImageryDetail
→ click related poem → router.push(`/poem/${id}`) or search
```

**Step 2: Commit**

```bash
git add frontend/src/views/explore/ImageryView.vue
git commit -m "feat(imagery): add ImageryView main page"
```

---

### Task 8: Frontend — Register route + navigation entries

**Files:**
- Modify: `frontend/src/router/index.js`
- Modify: `frontend/src/components/common/SideNav.vue`
- Modify: `frontend/src/views/learn/HomeView.vue`

**Step 1: Add route**

In `frontend/src/router/index.js`, add before the 404 catch-all:

```javascript
{
  path: '/explore/imagery',
  name: 'Imagery',
  component: () => import('@/views/explore/ImageryView.vue'),
  meta: { title: '诗境漫游' }
},
```

**Step 2: Add SideNav entry**

In `frontend/src/components/common/SideNav.vue`, add an icon component for imagery (use a compass/star SVG) and add to the "鉴赏" section items:

```javascript
{ name: '诗境漫游', path: '/explore/imagery', icon: IconCompass }
```

**Step 3: Add HomeView feature card entry**

In `frontend/src/views/learn/HomeView.vue`, add a new entry to `featureCards` array (add a compass icon):

```javascript
{ name: '诗境漫游', icon: IconCompass, path: '/explore/imagery', iconBg: 'icon-bg-vermilion', iconClass: 'text-accent', cardClass: '' },
```

**Step 4: Commit**

```bash
git add frontend/src/router/index.js frontend/src/components/common/SideNav.vue frontend/src/views/learn/HomeView.vue
git commit -m "feat(imagery): register route + nav entries for 诗境漫游"
```

---

### Task 9: Frontend — Add "探索意境" button to PoemDetailView

**Files:**
- Modify: `frontend/src/views/learn/PoemDetailView.vue`

**Step 1: Add exploration button**

In `PoemDetailView.vue`, after the `<AnalysisPanel>` component, add a button that navigates to the imagery page with the current poem's data:

```html
<div class="content-container pb-4">
  <button
    class="explore-btn"
    @click="goImagery"
  >
    探索意境
  </button>
</div>
```

Add the `goImagery` function:
```javascript
function goImagery() {
  const text = poem.value?.content?.join('\n') || ''
  const title = poem.value?.title || ''
  const author = poem.value?.author?.name || ''
  router.push({
    path: '/explore/imagery',
    query: { poem: text, title, author }
  })
}
```

**Step 2: Commit**

```bash
git add frontend/src/views/learn/PoemDetailView.vue
git commit -m "feat(imagery): add explore button to poem detail page"
```

---

### Task 10: Final integration commit

**Step 1: Verify all files**

Check that all new files exist and all modifications are saved:
- `backend/app/models/request.py` — has `ImageryAnalyzeRequest`
- `backend/app/models/__init__.py` — exports it
- `backend/app/services/imagery_service.py` — exists
- `backend/app/services/__init__.py` — exports it
- `backend/app/routers/imagery.py` — exists
- `backend/app/routers/__init__.py` — exports it
- `backend/app/main.py` — includes router
- `frontend/src/api/imagery.js` — exists
- `frontend/src/components/imagery/ImageryStarMap.vue` — exists
- `frontend/src/components/imagery/ImageryDetail.vue` — exists
- `frontend/src/views/explore/ImageryView.vue` — exists
- `frontend/src/router/index.js` — has route
- `frontend/src/components/common/SideNav.vue` — has nav entry
- `frontend/src/views/learn/HomeView.vue` — has feature card
- `frontend/src/views/learn/PoemDetailView.vue` — has explore button

**Step 2: Final commit if any unstaged changes remain**

```bash
git add -A
git commit -m "feat: 诗境漫游 — 沉浸式诗词意象探索完整功能"
```
