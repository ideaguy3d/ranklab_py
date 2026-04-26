"""Generic reusable agents and tools for RankLab subprojects."""

import json
from datetime import datetime
from typing import Any

from agents import Agent, function_tool


@function_tool
def get_iso_timestamp() -> str:
    """Return current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


@function_tool
def build_task_checklist(goal: str, constraints: str = "", max_steps: int = 6) -> str:
    """Return a short JSON checklist for executing a goal."""
    max_steps = max(2, min(max_steps, 10))
    steps = [
        "Clarify objective and output format.",
        "Identify required inputs and missing details.",
        "Generate plan aligned to constraints.",
        "Draft user-facing output.",
        "Validate output against requirements.",
        "Provide immediate next actions.",
    ][:max_steps]
    return json.dumps(
        {
            "goal": goal.strip(),
            "constraints": constraints.strip() if constraints else "None provided",
            "steps": steps,
        },
        indent=2,
    )


@function_tool
def evaluate_options(options_json: str, criteria_json: str) -> str:
    """Return weighted ranking for options in JSON form."""
    options = json.loads(options_json)
    criteria = json.loads(criteria_json)
    totals: dict[str, float] = {str(opt): 0.0 for opt in options}

    for criterion in criteria:
        weight = float(criterion.get("weight", 0))
        scores: dict[str, Any] = criterion.get("scores", {})
        for option in totals:
            totals[option] += float(scores.get(option, 0)) * weight

    ranking = sorted(
        [{"option": option, "score": round(score, 3)} for option, score in totals.items()],
        key=lambda x: x["score"],
        reverse=True,
    )
    return json.dumps({"ranking": ranking}, indent=2)


planner_agent = Agent(
    name="Task Planner Agent",
    handoff_description="Clarifies goals and creates concise execution plans.",
    instructions="""
Clarify user goals and produce practical short plans.
Ask only the minimum required follow-up questions.
""",
    tools=[get_iso_timestamp, build_task_checklist],
)


analyst_agent = Agent(
    name="Domain Analyst Agent",
    handoff_description="Analyzes options and tradeoffs with explicit reasoning.",
    instructions="""
Break problems into structured observations and compare tradeoffs.
State assumptions when required information is missing.
""",
    tools=[evaluate_options],
)


writer_agent = Agent(
    name="Output Composer Agent",
    handoff_description="Packages analysis into concise user-ready output.",
    instructions="""
Convert analysis into direct, actionable output.
Do not introduce unsupported claims.
""",
    tools=[get_iso_timestamp],
)


router_agent = Agent(
    name="General Router Agent",
    instructions="""
Route to planner for scoping, analyst for comparison/deep reasoning,
and writer for final packaging.
""",
    handoffs=[planner_agent, analyst_agent, writer_agent],
    model="gpt-5.1",
)

