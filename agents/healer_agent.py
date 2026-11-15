"""Healer Agent — classifies failing runs into root-cause categories."""

from __future__ import annotations

from .llm_client import LLMClient


class TriageAnalystAgent:
    """Classifies test failures into app defect / test defect / environment / data."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.name = "Triage Analyst"
        self.role_key = "triage_analyst"
        self.output = ""

    def execute(self, llm: LLMClient, prompt: str) -> str:
        self.output = llm.complete(self.role_key, prompt)
        return self.output

    def triage(self, requirement: str) -> str:
        prompt = (
            "You are a failure-triage analyst. For the following requirement, "
            "define hooks to classify failing runs into: application defect, "
            "test defect, environment, or test-data cause. Return triage hooks "
            "with what to attach (trace, screenshot) on failure:\\n" + requirement
        )
        return self.execute(self.llm, prompt)
