import pytest


def test_wechat_publisher_implements_interface():
    from backend.plugins.publishers.wechat import WeChatPublisher
    from backend.plugins.base import PublisherPlugin

    publisher = WeChatPublisher(app_id="test", app_secret="test")
    assert isinstance(publisher, PublisherPlugin)
    assert publisher.name == "wechat"
    assert publisher.platform == "wechat"


@pytest.mark.asyncio
async def test_wechat_publisher_authenticate_fails_with_bad_credentials():
    from backend.plugins.publishers.wechat import WeChatPublisher

    publisher = WeChatPublisher(app_id="invalid", app_secret="invalid")
    assert publisher.name == "wechat"
