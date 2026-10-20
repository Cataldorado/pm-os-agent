"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations


from prompts import CRITIC_SYSTEM

VERDICT_TOOL = {
    "name": "submit_verdict",
    "description": "Submit your pass/fail verdict on the proposed output.",
    "input_schema": {"type": "object", "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "reasons": {"type": "array", "items": {"type": "string"}}},
        "required": ["verdict", "reasons"]},
}


def review(client, model: str, proposed_output: str, source_data: str) -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...]} for a proposed output."""
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        system=CRITIC_SYSTEM,
        messages=[
            {"role": "user", "content":
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}"},
        ],
        # Forced tool call = guaranteed structured verdict (no JSON-in-text parsing).
        tools=[VERDICT_TOOL],
        tool_choice={"type": "tool", "name": "submit_verdict"},
    )
    usage = resp.usage
    call = next((b for b in resp.content if b.type == "tool_use"), None)
    if call and call.input.get("verdict") in ("pass", "fail"):
        verdict = {"verdict": call.input["verdict"],
                   "reasons": call.input.get("reasons", [])}
    else:
        verdict = {"verdict": "fail", "reasons": ["critic returned no usable verdict"]}
    verdict["_usage"] = {"prompt": usage.input_tokens, "completion": usage.output_tokens}
    return verdict
