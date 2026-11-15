"""LLM abstraction for the multi-agent harness.

OfflineLLM is the default (no API key needed). OpenAILLM is the live
provider — set OPENAI_API_KEY to use it.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)

_CANNED_FILE = Path(__file__).parent / "canned_responses.json"


def _load_canned() -> dict:
    if _CANNED_FILE.exists():
        with open(_CANNED_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    logger.warning("canned_responses.json not found at %s", _CANNED_FILE)
    return {}


class LLMClient(ABC):
    @abstractmethod
    def complete(self, role: str, prompt: str) -> str:
        ...


class OfflineLLM(LLMClient):
    """Deterministic stub — loads canned responses from canned_responses.json."""

    def __init__(self):
        self._canned = _load_canned()

    def complete(self, role: str, prompt: str) -> str:
        template = self._canned.get(role)
        if not template:
            logger.warning("No canned response for role '%s'", role)
            return ""
        return template.replace("{prompt}", prompt)


class OpenAILLM(LLMClient):
    """Live OpenAI adapter. Set OPENAI_API_KEY before use."""

    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, role: str, prompt: str) -> str:
        # TODO: add retry with backoff for 429s
        backstories = {
            "manager": "You are an experienced QA architect. Decompose requirements into testable sub-tasks.",
            "test_designer": "You are a test design expert. Write concrete, reviewable test cases.",
            "automation_author": "You are a Playwright automation engineer. Write clean, production TypeScript specs.",
            "reviewer": "You are a senior QA engineer. Review automation code against coding standards.",
            "triage_analyst": "You are a failure-triage analyst. Classify test failures by root cause.",
        }
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": backstories.get(role, "You are a QA engineer.")},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return resp.choices[0].message.content or ""
        except Exception as exc:
            logger.error("LLM call failed for role=%s: %s", role, exc)
            raise RuntimeError(f"LLM completion failed for role '{role}'") from exc
