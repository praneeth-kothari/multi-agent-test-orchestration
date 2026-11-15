"""Review Agent — enforces QA coding standards on generated specs."""

from __future__ import annotations

from .llm_client import LLMClient


class CodeReviewerAgent:
    """Reviews automation code against QE coding standards."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.name = "Code Reviewer"
        self.role_key = "reviewer"
        self.output = ""

    def execute(self, llm: LLMClient, prompt: str) -> str:
        self.output = llm.complete(self.role_key, prompt)
        return self.output

    def review(self, spec: str) -> str:
        prompt = (
            "You are a senior QA engineer. Review the following Playwright spec "
            "against coding standards: web-first assertions, no hard-coded waits, "
            "role-based locators, clear test naming. Return PASS/FAIL with brief "
            "notes:\\n" + spec
        )
        return self.execute(self.llm, prompt)
