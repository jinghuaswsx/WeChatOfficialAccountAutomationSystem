import pytest
from backend.plugins.base import AIModelPlugin, PublisherPlugin, FormatterPlugin, ImageGeneratorPlugin


class FakeAI(AIModelPlugin):
    @property
    def name(self) -> str:
        return "fake_ai"
    async def generate(self, prompt: str, **kwargs) -> str:
        return "fake"


class FakePublisher(PublisherPlugin):
    @property
    def name(self) -> str:
        return "fake_pub"
    @property
    def platform(self) -> str:
        return "fake"
    async def authenticate(self) -> bool:
        return True
    async def upload_image(self, image_path: str) -> str:
        return "url"
    async def create_draft(self, title: str, content: str, images: list[str]) -> str:
        return "draft"
    async def publish(self, draft_id: str) -> bool:
        return True
    async def get_publish_status(self, draft_id: str) -> str:
        return "ok"


class FakeFormatter(FormatterPlugin):
    @property
    def name(self) -> str:
        return "fake_fmt"
    @property
    def platform(self) -> str:
        return "fake"
    def format(self, markdown: str, images: list[str] | None = None) -> str:
        return markdown


class FakeImageGen(ImageGeneratorPlugin):
    @property
    def name(self) -> str:
        return "fake_img"
    async def generate(self, prompt: str, **kwargs) -> str:
        return "/fake.png"


def test_register_and_get_ai_model():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    plugin = FakeAI()
    registry.register_ai_model(plugin)
    assert registry.get_ai_model("fake_ai") is plugin


def test_register_and_get_publisher():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    plugin = FakePublisher()
    registry.register_publisher(plugin)
    assert registry.get_publisher("fake_pub") is plugin


def test_register_and_get_formatter():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    plugin = FakeFormatter()
    registry.register_formatter(plugin)
    assert registry.get_formatter("fake_fmt") is plugin


def test_register_and_get_image_generator():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    plugin = FakeImageGen()
    registry.register_image_generator(plugin)
    assert registry.get_image_generator("fake_img") is plugin


def test_get_nonexistent_plugin_returns_none():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    assert registry.get_ai_model("nonexistent") is None


def test_list_plugins():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    registry.register_ai_model(FakeAI())
    registry.register_publisher(FakePublisher())
    registry.register_formatter(FakeFormatter())
    registry.register_image_generator(FakeImageGen())
    all_plugins = registry.list_all()
    assert all_plugins == {
        "ai_models": ["fake_ai"],
        "publishers": ["fake_pub"],
        "formatters": ["fake_fmt"],
        "image_generators": ["fake_img"],
    }


def test_duplicate_register_raises():
    from backend.plugins.registry import PluginRegistry
    registry = PluginRegistry()
    registry.register_ai_model(FakeAI())
    with pytest.raises(ValueError, match="already registered"):
        registry.register_ai_model(FakeAI())
