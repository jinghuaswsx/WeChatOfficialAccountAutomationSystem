from __future__ import annotations
from backend.plugins.base import (
    AIModelPlugin, PublisherPlugin, FormatterPlugin, ImageGeneratorPlugin, PluginBase,
)


class PluginRegistry:
    def __init__(self) -> None:
        self._ai_models: dict[str, AIModelPlugin] = {}
        self._publishers: dict[str, PublisherPlugin] = {}
        self._formatters: dict[str, FormatterPlugin] = {}
        self._image_generators: dict[str, ImageGeneratorPlugin] = {}

    def _register(self, store: dict[str, PluginBase], plugin: PluginBase) -> None:
        if plugin.name in store:
            raise ValueError(f"Plugin '{plugin.name}' already registered")
        store[plugin.name] = plugin

    def register_ai_model(self, plugin: AIModelPlugin) -> None:
        self._register(self._ai_models, plugin)

    def register_publisher(self, plugin: PublisherPlugin) -> None:
        self._register(self._publishers, plugin)

    def register_formatter(self, plugin: FormatterPlugin) -> None:
        self._register(self._formatters, plugin)

    def register_image_generator(self, plugin: ImageGeneratorPlugin) -> None:
        self._register(self._image_generators, plugin)

    def get_ai_model(self, name: str) -> AIModelPlugin | None:
        return self._ai_models.get(name)

    def get_publisher(self, name: str) -> PublisherPlugin | None:
        return self._publishers.get(name)

    def get_formatter(self, name: str) -> FormatterPlugin | None:
        return self._formatters.get(name)

    def get_image_generator(self, name: str) -> ImageGeneratorPlugin | None:
        return self._image_generators.get(name)

    def list_all(self) -> dict[str, list[str]]:
        return {
            "ai_models": list(self._ai_models.keys()),
            "publishers": list(self._publishers.keys()),
            "formatters": list(self._formatters.keys()),
            "image_generators": list(self._image_generators.keys()),
        }
