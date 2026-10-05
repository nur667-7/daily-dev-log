from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Topic:
    name: str
    principle: str
    challenge: str


TOPICS = (
    Topic(
        "Small functions",
        "A function is easier to test when it has one clear responsibility and explicit inputs.",
        "Take one long function and identify a coherent operation that could become a pure helper.",
    ),
    Topic(
        "Boundary validation",
        "Validate data when it enters the system so internal code can rely on stronger invariants.",
        "List three invalid inputs for an endpoint or command and decide where each should be rejected.",
    ),
    Topic(
        "Idempotency",
        "An idempotent operation can be repeated without changing the final result after the first success.",
        "Design a retry-safe update using an idempotency key or a natural unique constraint.",
    ),
    Topic(
        "Readable errors",
        "A useful error explains what failed, preserves the cause, and suggests the next diagnostic step.",
        "Rewrite one vague error message so it includes the failed operation and relevant identifier.",
    ),
    Topic(
        "Dependency direction",
        "Core business rules stay easier to change when infrastructure depends on them instead of the reverse.",
        "Sketch the dependency arrows between one domain rule, its storage adapter, and its entry point.",
    ),
    Topic(
        "Data invariants",
        "An invariant is a condition that must remain true before and after every valid state transition.",
        "Choose one model and write down two invariants that its constructors and updates must preserve.",
    ),
    Topic(
        "Focused tests",
        "A valuable test protects observable behavior and fails for a meaningful regression.",
        "Replace one implementation-shaped assertion with an assertion about public behavior.",
    ),
    Topic(
        "Safe migrations",
        "Expand-and-contract migrations keep old and new application versions compatible during rollout.",
        "Outline an additive schema change, backfill, application switch, and later cleanup.",
    ),
    Topic(
        "Observability",
        "Logs, metrics, and traces are most useful when they answer a concrete operational question.",
        "Pick one failure mode and name the signal that would reveal it before a user reports it.",
    ),
    Topic(
        "Caching",
        "A cache trades freshness and complexity for latency or load reduction.",
        "Define the key, invalidation rule, and acceptable staleness for one cached value.",
    ),
    Topic(
        "Concurrency",
        "Shared mutable state needs an ownership or synchronization rule to avoid race conditions.",
        "Find one read-modify-write sequence and describe how concurrent execution could break it.",
    ),
    Topic(
        "API contracts",
        "Stable contracts specify behavior, errors, and compatibility expectations rather than implementation details.",
        "Write a compact contract for one endpoint including success, validation failure, and not-found behavior.",
    ),
)

REFLECTIONS = (
    "What assumption would be most expensive if it turned out to be false?",
    "Which part could be made easier to verify with a smaller interface?",
    "What evidence would convince you that the change works in production?",
    "Which edge case is currently handled only by convention?",
    "What can be removed while preserving the required behavior?",
    "Where is the boundary between a recoverable failure and a fatal one?",
    "What future change would this design make unnecessarily difficult?",
)


def stable_index(day: date, namespace: str, size: int) -> int:
    digest = hashlib.sha256(f"{namespace}:{day.isoformat()}".encode()).digest()
    return int.from_bytes(digest[:8], "big") % size


def render_entry(day: date) -> tuple[str, Topic, str]:
    topic = TOPICS[stable_index(day, "topic", len(TOPICS))]
    reflection = REFLECTIONS[stable_index(day, "reflection", len(REFLECTIONS))]
    content = f"""# Daily Dev Prompt — {day.isoformat()}

## {topic.name}

{topic.principle}

### Practice

{topic.challenge}

### Reflection

{reflection}

---

Generated deterministically for UTC date `{day.isoformat()}` by the repository's disclosed GitHub Actions workflow.
"""
    return content, topic, reflection


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def generate(day: date) -> list[Path]:
    content, topic, reflection = render_entry(day)
    entry_path = ROOT / "data" / "daily" / f"{day.isoformat()}.md"
    latest_path = ROOT / "data" / "latest.json"

    latest = {
        "date": day.isoformat(),
        "entry": entry_path.relative_to(ROOT).as_posix(),
        "topic": topic.name,
        "reflection": reflection,
    }

    changed: list[Path] = []
    if write_if_changed(entry_path, content):
        changed.append(entry_path)
    if write_if_changed(latest_path, json.dumps(latest, indent=2, ensure_ascii=False) + "\n"):
        changed.append(latest_path)
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one deterministic daily development prompt.")
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=datetime.now(timezone.utc).date(),
        help="UTC date in YYYY-MM-DD form; defaults to the current UTC date.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    changed = generate(args.date)
    if changed:
        for path in changed:
            print(f"updated {path.relative_to(ROOT).as_posix()}")
    else:
        print("nothing changed")


if __name__ == "__main__":
    main()
