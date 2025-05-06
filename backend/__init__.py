import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
# 加载环境变量
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
    # CORS(app, resources={r"/*": {"origins": ["https://*.vercel.app", os.getenv("VERCEL_URL")]}})
    app.config.from_mapping(
        NOTION_TOKEN=os.getenv("NOTION_TOKEN"),
        DATABASE_ID=os.getenv('DATABASE_ID'),
        DATABASE=os.path.join(app.instance_path, 'notion.sqlite')
    )

    try:
        # 主要是为了存放 SQLite 数据，确保目录存在
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册数据库
    from . import db
    db.init_app(app)

    # 初始化 Notion 客户端
    from .notion_utils import NotionClient
    notion = NotionClient()
    notion.init_app(app)

    # 注册蓝图
    from .routes import bp as notion_bp
    app.register_blueprint(notion_bp)

    return app

