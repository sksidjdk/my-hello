from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, TypedDict

from flask import Flask, abort, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_CATEGORIES = {"美食", "风景", "露营"}


@dataclass
class Post:
    title: str
    location: str
    category: str
    image_url: str
    note: str


class PostPayload(TypedDict):
    title: str
    location: str
    category: str
    image_url: str
    note: str


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "static"),
        template_folder=str(BASE_DIR / "templates"),
    )

    # Simple in-memory feed for demo purposes
    posts: List[Post] = [
        Post(
            title="夜宵烧烤拼盘",
            location="成都 · 窄巷子",
            category="美食",
            image_url="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200",
            note="碳火烤串配冰啤，一天的疲惫瞬间治愈。",
        ),
        Post(
            title="星空露营点",
            location="内蒙古 · 阿尔山",
            category="露营",
            image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200",
            note="草原边的高台观景位，能看清整片银河。",
        ),
        Post(
            title="海边步道",
            location="厦门 · 曾厝垵",
            category="风景",
            image_url="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200",
            note="日落时分的金色海面，走一走就不想回家。",
        ),
    ]

    @app.get("/")
    def home() -> str:
        return render_template("index.html")

    @app.get("/health")
    def health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/posts")
    def list_posts() -> Dict[str, List[Dict[str, str]]]:
        return jsonify({"items": [asdict(post) for post in posts]})

    @app.post("/api/posts")
    def create_post() -> Dict[str, str]:
        payload: PostPayload = request.get_json(force=True, silent=True) or {}
        missing = [
            field for field in ("title", "location", "category", "image_url") if not payload.get(field)
        ]
        if missing:
            abort(400, description=f"缺少字段: {', '.join(missing)}")

        category = payload["category"].strip()
        if category not in ALLOWED_CATEGORIES:
            abort(400, description="category 仅支持 美食/风景/露营")

        note = payload.get("note", "").strip()
        if len(note) > 240:
            abort(400, description="note 超过 240 字符")

        post = Post(
            title=payload["title"].strip(),
            location=payload["location"].strip(),
            category=category,
            image_url=payload["image_url"].strip(),
            note=note,
        )
        posts.insert(0, post)
        # 避免内存无限增长，只保留最新 120 条
        del posts[120:]
        return jsonify({"status": "ok"}), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
