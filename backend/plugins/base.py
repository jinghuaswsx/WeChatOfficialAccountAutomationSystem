from abc import ABC, abstractmethod


class PluginBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...


class AIModelPlugin(PluginBase):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str: ...


class PublisherPlugin(PluginBase):
    @property
    @abstractmethod
    def platform(self) -> str: ...

    @abstractmethod
    async def authenticate(self) -> bool: ...

    @abstractmethod
    async def upload_image(self, image_path: str) -> str: ...

    @abstractmethod
    async def create_draft(self, title: str, content: str, images: list[str]) -> str: ...

    @abstractmethod
    async def publish(self, draft_id: str) -> bool: ...

    @abstractmethod
    async def get_publish_status(self, draft_id: str) -> str: ...


class FormatterPlugin(PluginBase):
    @property
    @abstractmethod
    def platform(self) -> str: ...

    @abstractmethod
    def format(self, markdown: str, images: list[str] | None = None) -> str: ...


class ImageGeneratorPlugin(PluginBase):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str: ...
