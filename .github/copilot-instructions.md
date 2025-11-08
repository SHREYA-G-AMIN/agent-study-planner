## Quick context for AI contributors

This repo is an AI-assisted study-planner implemented in Python. Key runtime flows are JSON-driven and agent-backed. Before editing agents, read these files to understand intent and constraints:

- `README.md` and `HOW_TO_USE.md` — user-facing entry points and CLI instructions (run `python interactive_planner.py`).
- `json_manager.py` and `student_study_data.json` — canonical data model and persistence (primary integration point).
- `agents/*.py` — `PlannerAgent`, `TrackerAgent`, `MotivatorAgent` (each accepts an optional `data_manager` for JSON integration).
- `config/settings.py` — central config for OPENAI_API_KEY and model/temperatures.
- `firebase_config.py`, `firebase_upload.py` — optional Firebase upload flow using `firebase_key.json`.

## Important architectural notes

- Two complementary modes exist: programmatic/JSON (primary, stable) and AI/agent-driven (experimental). The JSON-mode is production-ready for data operations; AI agents add natural-language planning/insights.
- Agents are simple wrappers around an LLM (`langchain_openai.ChatOpenAI` + `langchain_core.prompts.ChatPromptTemplate`) and expect `data_manager` for JSON workflows. Methods follow both a pure-LLM API (e.g. `create_schedule`) and JSON-integrated helpers (e.g. `create_schedule_from_json`).
- The codebase was written against a LangChain 0.x style chaining API (e.g. `prompt | llm`). The repo includes a note about LangChain 1.x incompatibility in `LANGCHAIN_SOLUTION.md`. Do not assume modern LangChain 1.x AgentExecutor semantics unless you update imports and tests accordingly.

## Local developer workflows (practical commands)

- Run interactive CLI: `python interactive_planner.py` (see `HOW_TO_USE.md`).
- Run the main demo: `python main.py` (initializes StudyPlannerSystem, memory + JSON modes).
- Enable JSON persistence when instantiating system objects: `StudyPlannerSystem(use_json=True)` or pass a `StudentDataManager` to agents.
- Tests: run the test suite with pytest from the repo root: `pytest -q` (tests are in `tests/` and root-level `test_*.py`).

## Project-specific patterns and examples

- JSON-first pattern: prefer calling `StudentDataManager` methods for loading/saving state and let agents operate on the constructed syllabus/schedule. Example: `PlannerAgent.create_schedule_from_json()` builds a syllabus from `study_plan` and saves `generated_schedule` back into `student_study_data.json`.
- Agent signatures: each agent is constructed roughly as:

  - `PlannerAgent(data_manager=None)` — use `create_schedule`, `adjust_schedule` (LLM), or `create_schedule_from_json`, `adjust_schedule_from_json` (JSON helpers).
  - `TrackerAgent(data_manager=None)` — use `track_progress`, `track_from_json`, `mark_topics_completed_from_list`.
  - `MotivatorAgent(data_manager=None)` — use `daily_motivation`, `motivate_from_json`, `weekly_summary`.

- Config usage: secrets are loaded from environment via `python-dotenv`. The OpenAI key expected is `OPENAI_API_KEY` and model settings live in `config/settings.py`.

## Compatibility & dependency notes

- `requirements.txt` pins early `langchain` and `langchain-openai` packages (0.x). The code uses the older chaining API — if you update LangChain, also update agents to use the new API or replace agents with small direct LLM calls using `langchain_openai.ChatOpenAI` and `ChatPromptTemplate` as the code currently does.
- Firebase integration exists but requires `firebase_key.json` and replacement of the `databaseURL` in `firebase_upload.py`.

## What to change when editing agents

1. Preserve JSON helpers: keep `*_from_json` methods intact (tests and main app expect them).
2. If you change LLM interfaces, update `config/settings.py` and all agent imports; update `LANGCHAIN_SOLUTION.md` to reflect the new approach.
3. Avoid hard-coding model names/keys — read from `config/settings.py` or environment.

## Examples to copy/paste

- Create a schedule programmatically using the stable JSON flow:

  ```py
  from json_manager import StudentDataManager
  from agents.planner_agent import PlannerAgent

  dm = StudentDataManager()
  planner = PlannerAgent(data_manager=dm)
  planner.create_schedule_from_json(exam_date="2025-11-20", available_hours=3)
  ```

- Run the demo with JSON persistence:

  ```bash
  python main.py  # or: python -c "from main import StudyPlannerSystem; StudyPlannerSystem(use_json=True).run_daily_workflow()"
  ```

## Where to look for examples/tests

- `interactive_planner.py`, `main.py` — end-to-end flows.
- `tests/` and `test_*.py` at repo root — quick regression checks.

If anything here is unclear or you want the agents migrated to a LangChain 1.x / direct-LLM approach, tell me which agent(s) to update and I'll provide a minimal, tests-first rewrite.  
