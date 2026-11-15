"""Multi-Agent Test Orchestration Harness — entry point.

Run:
    python multiagent_test_harness.py "Checkout must reject an expired card"
"""

import argparse
import json
import time

from agents import Orchestrator
from agents.llm_client import OfflineLLM, OpenAILLM
from agents.requirement_analysis_agent import RequirementAnalysisAgent
from agents.code_agent import AutomationAuthorAgent
from agents.review_agent import CodeReviewerAgent
from agents.healer_agent import TriageAnalystAgent


def build_workers(llm) -> dict:
    """Assemble the specialist agents for the crew."""
    return {
        "designer": RequirementAnalysisAgent(llm),
        "author": AutomationAuthorAgent(llm),
        "reviewer": CodeReviewerAgent(llm),
        "triage": TriageAnalystAgent(llm),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the multi-agent test orchestration harness."
    )
    parser.add_argument(
        "requirement",
        nargs="?",
        default="Login must reject invalid credentials",
        help="Requirement / user story to process",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use a live LLM provider (requires OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--output",
        default="demo_output.json",
        help="Path to write the run output JSON",
    )
    args = parser.parse_args()

    llm = OpenAILLM() if args.live else OfflineLLM()
    crew = Orchestrator(llm=llm)
    workers = build_workers(llm)

    print("=" * 66)
    print("REQUIREMENT:", args.requirement)
    print("=" * 66)

    result = crew.run_crew(args.requirement, workers)

    for step in crew.log:
        print(
            f"  [{step.phase:>9}] {step.agent:<18} -> {step.chars} chars"
        )

    print("-" * 66)
    print(result["playwright_spec"])
    print("-" * 66)
    print(result["review"])
    print("-" * 66)
    print(result["triage_hooks"])
    print(f"\nArtifacts written: {args.output}")

    result["run_log"] = [
        {
            "phase": s.phase,
            "agent": s.agent,
            "role": s.role,
            "chars": s.chars,
        }
        for s in crew.log
    ]
    result["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)


if __name__ == "__main__":
    main()
