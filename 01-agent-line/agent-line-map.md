# Agent Line Map: Cortex PM Chief-of-Staff Agent

> Module 1 · The Agent Line
>
> ✅ **What this validates:** every risky action has a clear owner, by the end you'll have proven an above/below-the-line map with HITL checkpoints, scored on reversibility, blast radius, and measurability.

## The workflow, decision by decision

List every discrete decision or action in your agent's workflow, then score each one and place it **above** the line (a human owns it) or **below** (the agent owns it). Borderline calls get an HITL checkpoint.

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull project state + activity | H | L | H | Below | No |
| Decide relevant context | H | M | M | Below | Yes: human checks the "Data relied on" list |
| Draft the update | H | L | H | Below | No (review happens at 8a/8b) |
| Decide tone | H | L | M | Below | Yes: until tone principles are written |
| Decide commitment level | L | H | M | Above | n/a: human owns it |
| Flag at-risk / escalation | H | M | M | Below | Yes: human confirms the status call |
| Choose what to escalate | H | M | M | Below | No (the recipient is the checkpoint) |
| Propose a story batch (capped) | H | L | M | Below | Yes: human approves the batch |
| Post / send the update | L | H | M | Above | n/a: human owns it |
| Approve a company-wide update | L | H | L | Above | n/a: human owns it |

## One-sentence justifications

1. **Pull project state + activity** sits **below** the line because it's **easy** to reverse, has a **low** blast radius, and is **easy** to verify; deciding factor: **reversibility** (it's read-only, so a wrong pull is simply discarded).
2. **Decide relevant context** sits **below** the line, with a human check, because it's **easy** to reverse, has a **medium** blast radius, and is **moderately** verifiable; deciding factor: **blast radius** (a confidential item slipping in is the worst case).
3. **Draft the update** sits **below** the line because it's **easy** to reverse, has a **low** blast radius, and is **easy** to verify; deciding factor: **measurability** (every claim traces to the pulled data).
4. **Decide tone** sits **below** the line, with a human check, because it's **easy** to reverse, has a **low** blast radius, and is only **moderately** verifiable; deciding factor: **measurability** (no written standard exists yet).
5. **Decide commitment level** sits **above** the line because it's **hard** to reverse, has a **high** blast radius, and is only **moderately** verifiable; deciding factor: **reversibility** (a promise to leadership can't be unsaid).
6. **Flag at-risk / escalation** sits **below** the line, with a human check, because it's **easy** to reverse, has a **medium** blast radius, and is only **moderately** verifiable; deciding factor: **measurability** (a missed flag leaves no trace).
7. **Choose what to escalate** sits **below** the line because it's **easy** to reverse, has a **medium** blast radius, and is only **moderately** verifiable; deciding factor: **reversibility** (an escalation is a message a human can dismiss, and it is the human checkpoint).
8. **Propose a story batch** sits **below** the line, with a human check, because it's **easy** to reverse, has a **low** blast radius, and is only **moderately** verifiable; deciding factor: **measurability** (sequencing and scope are judgment calls).
9. **Post / send the update** sits **above** the line because it's **hard** to reverse, has a **high** blast radius, and is only **moderately** verifiable; deciding factor: **blast radius** (it reaches leadership or the company all at once).
10. **Approve a company-wide update** sits **above** the line because it's **hard** to reverse, has a **high** blast radius, and is **hard** to verify; deciding factor: **measurability** (nothing tells you afterwards whether the approval was right).

## Agent anatomy (sketch)

- **Model:** `claude-haiku-5-5` as the default for drafting, because it's cheap and fast (about $0.03 per run). A stronger model acts as the independent critic, and Cortex escalates to it after repeat critic failures. _(Design intent: the build still uses Haiku for the critic until M3.)_
- **Tools:** read-only `get_project`, `get_activity`, `search_past_updates`, `get_roadmap`, `get_norms`, plus `propose_stories` (queues for approval only, capped at 10). **Deliberately absent:** post/send, approve company-wide, create/close/merge tickets or PRs, set dates, mark launch gates.
- **Memory:** persist references only, meaning norms, roadmap and past updates as read-only sources. Run state (tool outputs, scratch reasoning, drafts) is purged after each run. Confidential and customer-specific data are filtered at read time, never stored. Saving human corrections is deferred to M4.
- **Loop:** _placeholder, defined in M2 loop-spec.md_
- **Bounds:** _placeholder, defined in M5 bounds-and-evals.md_
- **Evals:** _placeholder, defined in M5 bounds-and-evals.md_

## The golden rule, applied

- **Decide commitment level:** stays human because a promise to leadership can't be unsaid (reversibility failed; blast radius is also high).
- **Post / send the update:** stays human because it reaches leadership or the company all at once (blast radius failed; reversibility is also low).
- **Approve a company-wide update:** stays human because nothing tells you afterwards whether the approval was right (measurability failed; reversibility is low and blast radius is high). The approval is the safety mechanism itself.

## Hardest call

**Choose what to escalate.** I first wanted Cortex to hold back, because I didn't want to send false flags for non-critical issues or ones without a proper explanation. When I compared the two mistakes, I realized a missed mistake costs more than a false alarm, so Cortex should always escalate when unsure. The axis that settled it was **blast radius**: a false alarm costs a human a minute, but a missed escalation can leave a real problem growing unseen. It stays below the line with no extra approval step, because the person receiving the escalation is the human checkpoint.
