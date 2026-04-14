"""Generic multi-agent starter template for RankLab subprojects."""

import json
from datetime import datetime
from typing import Any

from agents import Agent, function_tool

PROJECT_NAME = "rank-budget"


@function_tool
def get_iso_timestamp() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


@function_tool
def build_task_checklist(goal: str, constraints: str = "", max_steps: int = 6) -> str:
    """Build a short execution checklist for a goal."""
    max_steps = max(2, min(max_steps, 10))
    constraints_text = constraints.strip() if constraints else "None provided"
    steps = [
        "Clarify the objective and output format.",
        "Identify required inputs and missing information.",
        "Produce a practical approach aligned to constraints.",
        "Draft the final output with concise structure.",
        "Validate output against user requirements.",
        "List immediate next actions.",
    ][:max_steps]
    return json.dumps(
        {
            "goal": goal.strip(),
            "constraints": constraints_text,
            "steps": steps,
        },
        indent=2,
    )


@function_tool
def evaluate_options(options_json: str, criteria_json: str) -> str:
    """Compare options against weighted criteria and return ranked JSON output."""
    options = json.loads(options_json)
    criteria = json.loads(criteria_json)

    if not isinstance(options, list) or not options:
        raise ValueError("options_json must be a non-empty JSON array.")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("criteria_json must be a non-empty JSON array.")

    totals: dict[str, float] = {str(opt): 0.0 for opt in options}

    for criterion in criteria:
        name = str(criterion.get("name", "unnamed"))
        weight = float(criterion.get("weight", 0))
        scores: dict[str, Any] = criterion.get("scores", {})
        if not isinstance(scores, dict):
            raise ValueError(f"Criterion '{name}' has invalid scores object.")
        for option in totals:
            raw = float(scores.get(option, 0))
            totals[option] += raw * weight

    ranking = sorted(
        [{"option": option, "score": round(score, 3)} for option, score in totals.items()],
        key=lambda x: x["score"],
        reverse=True,
    )
    return json.dumps({"ranking": ranking}, indent=2)


planner_agent = Agent(
    name="Task Planner Agent",
    handoff_description="Clarifies the user's goal, gathers missing inputs, and creates a concise plan.",
    instructions=f"""
You are the planner for the {PROJECT_NAME} app.

Responsibilities:
- Understand what the user is trying to accomplish.
- Ask clarifying questions only when required information is missing.
- Produce a short, concrete plan the other agents can execute.

Rules:
- Be concise and practical.
- Do not invent facts or user data.
- If requirements are ambiguous, ask for only the minimum details needed.
""",
    tools=[get_iso_timestamp, build_task_checklist],
)


analyst_agent = Agent(
    name="Domain Analyst Agent",
    handoff_description="Performs structured analysis, comparisons, and tradeoff evaluation.",
    instructions=f"""
You are the analyst for the {PROJECT_NAME} app.

Responsibilities:
- Break down the problem into structured observations.
- Compare options with explicit tradeoffs.
- Provide reasoning the user can validate quickly.

Rules:
- Prefer bullet points and clear structure.
- State assumptions when information is missing.
- Do not fabricate metrics, citations, or external facts.
""",
    tools=[evaluate_options],
)


writer_agent = Agent(
    name="Output Composer Agent",
    handoff_description="Turns analysis into user-ready output: recommendations, drafts, or action steps.",
    instructions=f"""
You are the output composer for the {PROJECT_NAME} app.

Responsibilities:
- Convert plans and analysis into final user-facing output.
- Keep language direct, concise, and actionable.
- Preserve factual accuracy from prior agent steps.

Rules:
- Do not add new claims that were not established earlier.
- Use checklists or numbered steps when useful.
- End with immediate next actions when appropriate.
""",
    tools=[get_iso_timestamp],
)
