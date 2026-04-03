from __future__ import annotations
from backend.plugins.base import AIModelPlugin

class MockAIPlugin(AIModelPlugin):
    def __init__(self, responses: dict[str, str] | None = None) -> None:
        self._responses = responses or {}

    @property
    def name(self) -> str:
        return "mock"

    async def generate(self, prompt: str, **kwargs) -> str:
        if prompt in self._responses:
            return self._responses[prompt]
        for key, value in self._responses.items():
            if key in prompt:
                return value
        return f"[Mock AI] 收到: {prompt[:100]}"
