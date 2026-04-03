from __future__ import annotations

import re

from backend.plugins.base import FormatterPlugin


class WeChatFormatter(FormatterPlugin):
    """微信公众号排版插件。将 Markdown 转为微信兼容的 HTML。"""

    @property
    def name(self) -> str:
        return "wechat_formatter"

    @property
    def platform(self) -> str:
        return "wechat"

    def format(self, markdown: str, images: list[str] | None = None) -> str:
        html = markdown

        # 标题
        html = re.sub(
            r"^### (.+)$",
            r'<h3 style="font-size:16px;font-weight:bold;margin:20px 0 10px;">\1</h3>',
            html,
            flags=re.MULTILINE,
        )
        html = re.sub(
            r"^## (.+)$",
            r'<h2 style="font-size:18px;font-weight:bold;margin:25px 0 10px;">\1</h2>',
            html,
            flags=re.MULTILINE,
        )
        html = re.sub(
            r"^# (.+)$",
            r'<h1 style="font-size:22px;font-weight:bold;margin:30px 0 15px;text-align:center;">\1</h1>',
            html,
            flags=re.MULTILINE,
        )

        # 加粗和斜体
        html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)

        # 段落
        paragraphs = html.split("\n\n")
        formatted = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith("<h"):
                p = f'<p style="margin:15px 0;line-height:1.8;font-size:15px;">{p}</p>'
            formatted.append(p)

        return "\n".join(formatted)
