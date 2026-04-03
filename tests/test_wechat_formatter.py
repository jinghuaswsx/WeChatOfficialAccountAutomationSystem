import pytest


def test_wechat_formatter_implements_interface():
    from backend.plugins.formatters.wechat_formatter import WeChatFormatter
    from backend.plugins.base import FormatterPlugin

    formatter = WeChatFormatter()
    assert isinstance(formatter, FormatterPlugin)
    assert formatter.platform == "wechat"


def test_wechat_formatter_wraps_markdown():
    from backend.plugins.formatters.wechat_formatter import WeChatFormatter

    formatter = WeChatFormatter()
    result = formatter.format("# 标题\n\n这是正文内容。")
    assert "标题" in result
    assert "正文内容" in result
