from __future__ import annotations

from backend.plugins.base import PublisherPlugin


class WeChatPublisher(PublisherPlugin):
    """微信公众号发布插件。基于 wechatpy（实际 API 调用在配置正确后启用）。"""

    def __init__(self, app_id: str = "", app_secret: str = "") -> None:
        self._app_id = app_id
        self._app_secret = app_secret
        self._client = None

    @property
    def name(self) -> str:
        return "wechat"

    @property
    def platform(self) -> str:
        return "wechat"

    def _get_client(self):
        """延迟初始化 wechatpy 客户端。"""
        if self._client is None:
            try:
                from wechatpy import WeChatClient

                self._client = WeChatClient(self._app_id, self._app_secret)
            except ImportError:
                raise RuntimeError("请安装 wechatpy: pip install wechatpy")
        return self._client

    async def authenticate(self) -> bool:
        try:
            client = self._get_client()
            client.fetch_access_token()
            return True
        except Exception:
            return False

    async def upload_image(self, image_path: str) -> str:
        client = self._get_client()
        with open(image_path, "rb") as f:
            result = client.material.add("image", f)
        return result.get("media_id", "")

    async def create_draft(self, title: str, content: str, images: list[str]) -> str:
        client = self._get_client()
        articles = [
            {
                "title": title,
                "content": content,
                "thumb_media_id": images[0] if images else "",
            }
        ]
        result = client.draft.add(articles)
        return result.get("media_id", "")

    async def publish(self, draft_id: str) -> bool:
        client = self._get_client()
        try:
            client.freepublish.submit(draft_id)
            return True
        except Exception:
            return False

    async def get_publish_status(self, draft_id: str) -> str:
        return "unknown"
