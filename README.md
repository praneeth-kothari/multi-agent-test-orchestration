# Multi-Agent Test Orchestration Harness

A hierarchical multi-agent workflow for AI-assisted quality engineering.

An orchestrator agent decomposes a test requirement and delegates work to role-specialised sub-agents that collaborate to produce reviewed, production-ready Playwright specifications.

## Architecture

```
Requirement
    │
    ▼
┌─────────────────────┐
│   ORCHESTRATOR      │
│   (manager agent)   │
└─────────┬───────────┘
          │ delegates
    ┌─────┴─────┬─────┴─────┬──────┐
    ▼           ▼           ▼      ▼
Requirement  Code Agent   Review   Healer
Analysis     (writes      Agent    Agent
(creates     Playwright)  (QA      (fixes
 test cases)              review)  failures)
```

## Agent team

| Agent | Role | Responsibility |
|-------|------|----------------|
| Orchestrator | Manager | Decomposes requirements, routes work, aggregates results |
| Requirement Analysis | Test designer | Converts user stories into concrete test cases |
| Code Agent | Automation author | Writes Playwright (TypeScript) specs with web-first assertions |
| Review Agent | QA reviewer | Enforces coding standards, flags anti-patterns before merge |
| Healer Agent | Triage analyst | Classifies failures into app defect / test defect / env / data |

## Quickstart

```bash
git clone https://github.com/praneethkothari82-Surya/multi-agent-test-orchestration.git
cd multi-agent-test-orchestration
python multiagent_test_harness.py "Checkout must reject an expired card"
```

No API key required — runs in offline mode with deterministic responses.

## Live mode

Set `OPENAI_API_KEY` and run with `--live`:

```bash
python multiagent_test_harness.py --live "Checkout must reject an expired card"
```

## Structure

```
├── agents/
│   ├── __init__.py
│   ├── llm_client.py
│   ├── canned_responses.json
│   ├── orchestrator_agent.py
│   ├── requirement_analysis_agent.py
│   ├── code_agent.py
│   ├── review_agent.py
│   └── healer_agent.py
├── multiagent_test_harness.py
├── demo_requirements.json
├── demo_output.json
├── requirements.txt
└── README.md
```

## License

MIT
