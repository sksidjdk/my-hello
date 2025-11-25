# my-hello

一个适配移动端的 Flask Web 应用示例，并可直接部署到 Vercel。主题是「城市美食与风景分享」，可以发布美食、风景、露营地的地点与照片。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 本地运行（默认监听 5000 端口）
python -m flask --app api/index run --port 5000
```

打开 <http://localhost:5000> 即可在浏览器（含手机调试模式）预览。模板和样式放在 `templates/` 与 `static/` 目录。

### API
- `GET /api/posts`：获取当前展示的推荐列表（内存保存示例）。
- `POST /api/posts`：提交一条新的推荐，需包含 `title`、`location`、`category`（美食/风景/露营）、`image_url`，可附加 `note`（上限 240 字）。
- `GET /health`：健康检查。

## 部署到 Vercel

1. 安装并登录 [Vercel CLI](https://vercel.com/docs/cli)。
2. 运行 `vercel`，选择本仓库所在目录并使用默认配置。
3. 首次部署后，Vercel 会识别 `vercel.json`，使用 Python 运行时构建 `api/index.py` 并暴露页面与 API 路由。

完成后即可在手机浏览器访问你的 Vercel 域名，直接发布和浏览推荐。
