# LLaMA Factory 启动手册

## 环境要求

- Python 3.11+（已安装 ml 依赖）
- Node.js 18+（前端 Vite 构建）
- 首次运行前执行：`pip install -e .`（已执行则跳过）

## 启动步骤

### 终端 1 — 后端管理 API

```bash
cd /Users/kyle/Documents/LLMSource/llamafactory-refactor
llamafactory-api
```

看到 `Management API running at http://localhost:8001` 即启动成功。

### 终端 2 — 前端开发服务器

```bash
cd /Users/kyle/Documents/LLMSource/llamafactory-refactor/frontend
npm run dev
```

看到 `http://localhost:5173/` 即启动成功。

### 浏览器访问

打开 `http://localhost:5173/`

| 页面 | 路由 | 功能 |
|------|------|------|
| 训练 | `/train` | 配置训练参数、启动训练、查看监控日志 |
| 评估 | `/eval` | 配置评估参数、运行评估 |
| 推理 | `/infer` | 加载模型、对话交互 |
| 导出 | `/export` | 模型导出、量化 |

## 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 管理 API | 8001 | REST API + WebSocket |
| 前端代理 | 5173 | Vite 开发服务器，`/api` 和 `/ws` 代理到 8001 |

## 常见问题

**Q: 不启动训练框架能用前端吗？**

可以。`llamafactory-api` 只启动 API 服务，不加载模型。训练/评估只在点击按钮时通过子进程调用 `llamafactory-cli`。

**Q: 切换语言？**

左侧边栏底部开关：亮色/暗色。语言通过 locale 文件配置（`frontend/src/i18n/zh.json`）。

**Q: API 认证？**

已移除。不设 API_KEY 时所有请求放行，适用于本地开发和测试。

**Q: 如何停止？**

两个终端分别 `Ctrl+C` 即可。
