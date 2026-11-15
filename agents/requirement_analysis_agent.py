"""Requirement Analysis agent — converts user stories into concrete test cases."""

from __future__ import annotations

from .llm_client import LLMClient
from .orchestrator_agent import AgentResult


class RequirementAnalysisAgent:
    """Turns acceptance criteria / user stories into concrete test cases."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.name = "Test Designer"
        self.role_key = "test_designer"
        self.output = ""

    def execute(self, llm: LLMClient, prompt: str) -> str:
        self.output = llm.complete(self.role_key, prompt)
        return self.output

    def design(self, requirement: str) -> str:
        prompt = (
            "You are a test design expert. Turn the following requirement into "
            "concrete test cases: happy path, negative path, boundary values, "
            "and assertion targets. Return ONLY the cases:\\n" + requirement
        )
        return self.execute(self.llm, prompt)
