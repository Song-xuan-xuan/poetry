# 诗词雅韵

中国古典诗词学习与创作平台，支持诗词检索、鉴赏、AI 创作、飞花令、答题闯关、诗画互生等功能。

## 技术栈

- **前端**: Vue 3 + Vite 5 + Tailwind CSS 3 + Vant 4
- **后端**: Python FastAPI + Uvicorn + Motor (异步 MongoDB 驱动)
- **数据库**: MongoDB
- **AI**: OpenAI 兼容接口 (文本生成 / 图像生成 / 视觉理解)
- **部署**: Docker Compose + Nginx 反向代理

## 功能模块

| 模块 | 说明 |
|------|------|
| 诗词检索 | 按诗名、作者、诗句、意象模糊搜索，分页浏览 |
| 诗词鉴赏 | 原文、白话译文、赏析、文化拓展、作者简介 |
| AI 创作 | 根据场景/情感/风格/意象生成古典诗词 |
| 诗词润色 | 对已有诗词进行 AI 润色优化 |
| 仿写工坊 | 参考原诗，AI 仿写新篇 |
| 飞花令 | 诗词接龙挑战，支持 AI 语义验证 |
| 答题闯关 | 自动生成诗词填空题 |
| 诗画互生 | 诗词生成水墨配图 / 图片生成诗词 |

## 快速开始 (本地开发)

### 前置要求

- Node.js >= 18
- Python >= 3.10
- MongoDB >= 6

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env         # 编辑 .env 填入 API Key
python run.py
```

后端运行在 `http://localhost:8081`，API 文档: `http://localhost:8081/docs`

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`

## Docker 部署

### 1. 克隆代码

```bash
git clone https://github.com/your-username/poetry.git
cd poetry
```

### 2. 配置环境变量

```bash
cp .env.example .env
vi .env    # 填入 LLM_API_KEY 等
```

### 3. 一键部署

```bash
bash deploy.sh first
```

### 4. 导入数据

从本地 MongoDB Compass 导出 `poems` 集合为 JSON 后：

```bash
# 上传数据文件到服务器
scp poems.json user@server:~/poetry/

# 导入到 Docker 中的 MongoDB
docker compose cp poems.json poetry-mongo:/tmp/poems.json
docker compose exec poetry-mongo mongoimport \
  --db poetrydb --collection poems \
  --file /tmp/poems.json --jsonArray --drop
```

### 5. 验证

```bash
# 查看服务状态
bash deploy.sh status

# 查看日志
bash deploy.sh logs
```

访问 `http://服务器IP` 即可使用。

## 部署架构

```
用户浏览器 :80
    │
    ▼
  Nginx (poetry-web)
  ├── /        → Vue SPA 静态文件
  └── /api/*   → 反向代理
                    │
                    ▼
              FastAPI (poetry-api) :8081
                    │
                    ▼
              MongoDB (poetry-mongo) :27017
```

## 常用命令

```bash
bash deploy.sh first    # 首次部署
bash deploy.sh update   # 更新部署 (git pull + rebuild)
bash deploy.sh stop     # 停止服务
bash deploy.sh logs     # 查看日志
bash deploy.sh status   # 查看状态
```



## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/search?q=明月` | 通用检索 |
| GET | `/api/poems?page=1` | 诗词列表 |
| GET | `/api/poems/{id}` | 诗词详情 |
| GET | `/api/poems/author/{name}` | 按作者查询 |
| POST | `/api/generate` | AI 生成诗词 |
| POST | `/api/generate/optimize` | 润色诗词 |
| POST | `/api/generate/mimic` | 仿写诗词 |
| GET | `/api/challenge/chain/next?line=...` | 飞花令下句 |
| POST | `/api/challenge/chain/validate` | 验证接龙 |
| GET | `/api/challenge/quiz?count=5` | 生成题目 |
| POST | `/api/image/poem-to-image` | 诗词生成配图 |
| POST | `/api/image/image-to-poem` | 图片生成诗词 |

## 环境变量

参见 [.env.example](.env.example)

## License

MIT
