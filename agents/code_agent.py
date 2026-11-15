"""Code Agent — writes Playwright (TypeScript) specs from test cases."""

from __future__ import annotations

from .llm_client import LLMClient


class AutomationAuthorAgent:
    """Generates production Playwright specs from test cases."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.name = "Automation Author"
        self.role_key = "automation_author"
        self.output = ""

    def execute(self, llm: LLMClient, prompt: str) -> str:
        self.output = llm.complete(self.role_key, prompt)
        return self.output

    def author(self, test_cases: str) -> str:
        prompt = (
            "You are a Playwright automation engineer. Write a production "
            "Playwright (TypeScript) spec from the following test cases. Use "
            "web-first assertions, role-based locators, no hard-coded waits, "
            "and return ONLY the spec code:\\n" + test_cases
        )
        return self.execute(self.llm, prompt)
