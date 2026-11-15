"""Configuration for the multi-agent test orchestration harness."""

import os

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "offline")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

DEFAULT_OUTPUT_FILE = os.environ.get("HARNESS_OUTPUT", "demo_output.json")
DEFAULT_REQUIREMENT = os.environ.get("HARNESS_REQUIREMENT", "Login must reject invalid credentials")

DEFAULT_TEST_TIMEOUT = int(os.environ.get("TEST_TIMEOUT", "30000"))
DEFAULT_RETRIES = int(os.environ.get("TEST_RETRIES", "1"))

TRIAGE_CATEGORIES = ["application_defect", "test_defect", "environment", "test_data"]
