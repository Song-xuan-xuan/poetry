# 诗境漫游 — 沉浸式诗词意境探索

> 日期：2026-03-03
> 状态：已确认，待实施

## 问题

当前「诗词雅韵」功能齐全但创新不足：所有功能都是"输入→AI→输出"的工具逻辑，缺少用户与文化内容之间的深层连接。竞赛项目需要明确的文化创意创新叙事。

## 设计目标

在三个维度体现创新：
1. **交互体验**：意象图谱可视化探索，不是被动阅读
2. **AI 能力**：不是单纯"文生X"，而是结构化的文化知识抽取
3. **文化传播**：意象是中国诗词最独特的文化密码，功能直击本质

## 用户流程

```
选择/输入诗词 → AI 分析提取 3-6 个意象节点
→ 渲染「意境星图」（径向节点图）
→ 点击节点 → 展开面板：文化释义 / 关联诗句 / 意境配图
```

### 入口

- 诗词详情页底部「探索意境」按钮
- 首页功能入口 + 侧边栏独立入口
- URL: `/explore/imagery` 或 `/explore/imagery?poem=xxx`

## 后端设计

### 新增文件

- `backend/app/services/imagery_service.py` — 意象分析服务
- `backend/app/routers/imagery.py` — 路由
- `backend/app/models/request.py` — 新增 `ImageryAnalyzeRequest`

### API: `POST /api/imagery/analyze`

请求：
```json
{
  "poem_id": "optional-existing-poem-id",
  "poem_text": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
  "title": "静夜思",
  "author": "李白"
}
```

响应（`Result.data`）：
```json
{
  "poem_summary": "一首思乡之作，以月光起兴...",
  "imagery_nodes": [
    {
      "name": "月",
      "category": "天象",
      "significance": "全诗核心意象",
      "cultural_meaning": "月在唐诗中是最核心的意象之一...",
      "related_poems": [
        { "title": "月下独酌", "author": "李白", "dynasty": "唐", "quote": "举杯邀明月，对影成三人" }
      ],
      "connections": ["霜", "乡"]
    }
  ]
}
```

### 服务层

- 复用 `settings.LLM_*` 配置，惰性单例 AsyncOpenAI
- System prompt 要求 LLM 以 JSON 返回结构化意象分析
- 约束 3-6 个意象节点，每个含文化含义(200-300字)、2-3首关联诗句
- 异常降级：返回 fallback 基础分析

### 意境配图

不新增端点，复用现有 `POST /api/image/generate`，前端将意象描述作为 prompt 传入。

## 前端设计

### 新增文件

```
frontend/src/views/explore/ImageryView.vue       # 主页面
frontend/src/components/imagery/ImageryStarMap.vue # 星图可视化
frontend/src/components/imagery/ImageryDetail.vue  # 意象详情面板
frontend/src/api/imagery.js                        # API
```

### 意境星图可视化

- 纯 CSS/SVG 实现，不引入 D3.js
- 径向布局：中心放诗词主题，周围放意象节点
- SVG `<line>` 连接有关联的节点
- 节点大小根据重要性区分
- 颜色使用项目国风色板（金/朱砂/青矾绿/墨色）

### 交互

1. 页面加载：诗词文本 + 「开始探索」按钮
2. 分析中：骨架屏 + "正在解读意境..."
3. 星图呈现：节点依次 fade-in（0.3s 间隔）
4. 节点交互：
   - Hover：微放大 + 发光
   - Click：下方 slide-up 详情面板，3 个 Tab（文化含义/关联诗句/意境配图）
   - 关联诗句可跳转详情页
   - 意境配图 Tab 有「生成配图」按钮
5. 移动端：节点改竖向列表，详情改底部抽屉

### 路由注册

```js
{ path: '/explore/imagery', name: 'Imagery', component: ImageryView, meta: { title: '诗境漫游' } }
```

### 入口注册

- `SideNav.vue` — 鉴赏分组新增「诗境漫游」
- `HomeView.vue` — featureCards 新增入口
- `PoemDetailView.vue` — 赏析区域下方新增「探索意境」按钮

## 竞赛价值叙事

> 传统诗词教育以文本注释为主，学习者被动接收信息。「诗境漫游」通过 AI 结构化抽取诗词意象，构建可交互的意境图谱，让用户主动探索意象的文化含义与跨作品关联，实现从"读诗"到"悟诗"的体验升级。这是 AI 技术与传统文化深度融合的创新实践，而非简单的生成工具堆叠。

## 不做什么（YAGNI）

- 不做意象数据库持久化（首版每次实时分析）
- 不做用户收藏/分享功能
- 不做力导向图（径向布局足够）
- 不做意象间的语义相似度计算
