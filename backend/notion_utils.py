from flask import current_app
from notion_client import Client


class NotionClient:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.client = Client(auth=app.config["NOTION_TOKEN"])
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['notion'] = self

    @property
    def get_client(self):
        if self.client is None:
            raise RuntimeError('NotionClient not initialized')
        return self.client


def get_notion_client():
    return current_app.extensions['notion'].get_client


def query_database(query_data=None):
    if query_data is None:
        raise RuntimeError('database_id is required')
        # return notion.databases.query(**{
        #     "database_id": current_app.config["DATABASE_ID"]
        # })
    else:
        notion = get_notion_client()
        # 获取 databases 所有数据信息
        return notion.databases.query(**query_data)
        # 获取 databases 的元信息
        # return notion.databases.retrieve(**query_data)


def query_page(page_id=None, page_size=None):
    if page_id is None:
        raise RuntimeError('page_id is required')
    else:
        notion = get_notion_client()
        return notion.blocks.children.list(page_id)
