"""Orchestrator agent — decomposes requirements and routes to specialists."""

import logging
from dataclasses import dataclass
from typing import List

from .llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    agent: str
    role: str
    output: str
    chars: int
    phase: str


class Orchestrator:
    """Coordinates the multi-agent crew for a given requirement."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.log: List[AgentResult] = []

    def decompose(self, requirement: str) -> str:
        prompt = (
            "Break the following requirement into ordered sub-tasks for a "
            "multi-agent QE crew. Return ONLY the sub-task list:\\n" + requirement
        )
        output = self.llm.complete("manager", prompt)
        self._log("Orchestrator", "manager", output, "decompose")
        return output

    def run_crew(self, requirement: str, workers: dict) -> dict:
        decomposition = self.decompose(requirement)
        design = self._run(workers["designer"], requirement, "design")
        spec = self._run(workers["author"], design, "author")
        review = self._run(workers["reviewer"], spec, "review")
        triage = self._run(workers["triage"], requirement, "triage")

        return {
            "requirement": requirement,
            "decomposition": decomposition,
            "test_cases": design,
            "playwright_spec": spec,
            "review": review,
            "triage_hooks": triage,
            "handoffs": len(self.log),
            "run_log": self.log,
        }

    def _run(self, agent, prompt: str, phase: str) -> str:
        logger.debug("Running %s (phase=%s)", agent.name, phase)
        try:
            output = agent.execute(self.llm, prompt)
        except Exception:
            logger.exception("Agent %s failed during %s phase", agent.name, phase)
            raise
        self._log(agent.name, agent.role_key, output, phase)
        return output

    def _log(self, name: str, role: str, output: str, phase: str) -> None:
        self.log.append(AgentResult(agent=name, role=role, output=output, chars=len(output), phase=phase))
