import pytest
from abc import ABC


def test_ai_model_plugin_is_abstract():
    from backend.plugins.base import AIModelPlugin
    with pytest.raises(TypeError):
        AIModelPlugin()


def test_publisher_plugin_is_abstract():
    from backend.plugins.base import PublisherPlugin
    with pytest.raises(TypeError):
        PublisherPlugin()


def test_formatter_plugin_is_abstract():
    from backend.plugins.base import FormatterPlugin
    with pytest.raises(TypeError):
        FormatterPlugin()


def test_image_generator_plugin_is_abstract():
    from backend.plugins.base import ImageGeneratorPlugin
    with pytest.raises(TypeError):
        ImageGeneratorPlugin()


def test_concrete_ai_model_plugin():
    from backend.plugins.base import AIModelPlugin

    class MockAI(AIModelPlugin):
        @property
        def name(self) -> str:
            return "mock"

        async def generate(self, prompt: str, **kwargs) -> str:
            return "mock response"

    plugin = MockAI()
    assert plugin.name == "mock"


def test_concrete_publisher_plugin():
    from backend.plugins.base import PublisherPlugin

    class MockPublisher(PublisherPlugin):
        @property
        def name(self) -> str:
            return "mock"

        @property
        def platform(self) -> str:
            return "mock_platform"

        async def authenticate(self) -> bool:
            return True

        async def upload_image(self, image_path: str) -> str:
            return "url"

        async def create_draft(self, title: str, content: str, images: list[str]) -> str:
            return "draft_id"

        async def publish(self, draft_id: str) -> bool:
            return True

        async def get_publish_status(self, draft_id: str) -> str:
            return "published"

    plugin = MockPublisher()
    assert plugin.platform == "mock_platform"


def test_concrete_formatter_plugin():
    from backend.plugins.base import FormatterPlugin

    class MockFormatter(FormatterPlugin):
        @property
        def name(self) -> str:
            return "mock"

        @property
        def platform(self) -> str:
            return "mock_platform"

        def format(self, markdown: str, images: list[str] | None = None) -> str:
            return f"<p>{markdown}</p>"

    plugin = MockFormatter()
    assert plugin.format("hello") == "<p>hello</p>"


def test_concrete_image_generator_plugin():
    from backend.plugins.base import ImageGeneratorPlugin

    class MockImageGen(ImageGeneratorPlugin):
        @property
        def name(self) -> str:
            return "mock"

        async def generate(self, prompt: str, **kwargs) -> str:
            return "/path/to/image.png"

    plugin = MockImageGen()
    assert plugin.name == "mock"
