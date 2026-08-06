#!/usr/bin/env python3
"""Local lifecycle wrapper for Cua Driver trajectory recording and replay."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path.home() / ".hermes" / "recordings"
SKILLS = Path.home() / ".hermes" / "skills"
DAEMON_LOG = Path.home() / ".hermes" / "logs" / "cua-record-replay.log"


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not cleaned:
        raise SystemExit("Workflow name must contain letters or numbers.")
    return cleaned


def ensure_daemon() -> None:
    status = subprocess.run(["cua-driver", "status"], capture_output=True, text=True)
    if status.returncode == 0 and "not running" not in status.stdout.lower():
        return
    DAEMON_LOG.parent.mkdir(parents=True, exist_ok=True)
    log = DAEMON_LOG.open("a")
    subprocess.Popen(
        ["cua-driver", "serve"],
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    for _ in range(30):
        time.sleep(0.1)
        status = subprocess.run(["cua-driver", "status"], capture_output=True, text=True)
        if status.returncode == 0 and "not running" not in status.stdout.lower():
            return
    raise SystemExit(f"Cua Driver daemon did not start. Check {DAEMON_LOG}")


def call(tool: str, payload: dict) -> dict:
    ensure_daemon()
    proc = subprocess.run(
        ["cua-driver", "call", tool, json.dumps(payload)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip())
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(proc.stdout.strip())
        return {}


def workflow_dir(name: str) -> Path:
    path = ROOT / slug(name)
    if not path.is_dir():
        raise SystemExit(f"Recording not found: {path}")
    return path


def start(args: argparse.Namespace) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / slug(args.name)
    if path.exists() and any(path.iterdir()):
        raise SystemExit(f"Recording already exists: {path}")
    path.mkdir(parents=True, exist_ok=True)
    meta = {
        "name": args.name,
        "slug": slug(args.name),
        "created_at": datetime.now().astimezone().isoformat(),
        "video": args.video,
        "training_mode": args.training_mode or False,
    }
    (path / "workflow.json").write_text(json.dumps(meta, indent=2) + "\n")
    payload = {"output_dir": str(path), "record_video": args.video}
    if args.training_mode == "browser-use":
        payload["capture_selectors"] = True
        payload["capture_dom"] = True
        payload["capture_interaction_type"] = True
    result = call("start_recording", payload)
    print(json.dumps(result, indent=2))
    if args.training_mode == "browser-use":
        print("Browser-use training mode active. Capturing selectors, DOM, and decision points.")
    else:
        print("Recording started. Do not enter passwords, keys, payment data, or private records.")


def stop(_: argparse.Namespace) -> None:
    print(json.dumps(call("stop_recording", {}), indent=2))
    print("Recording stopped.")


def status(_: argparse.Namespace) -> None:
    print(json.dumps(call("get_recording_state", {}), indent=2))


def list_recordings(_: argparse.Namespace) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for path in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        turns = len(list(path.glob("turn-*/action.json")))
        print(f"{path.name}\t{turns} actions\t{path}")


def safe_value(value):
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if re.search(r"pass|secret|token|key", k, re.I) else safe_value(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [safe_value(v) for v in value]
    return value


def build(args: argparse.Namespace) -> None:
    source = workflow_dir(args.name)
    target = SKILLS / f"recorded-{slug(args.name)}"
    refs = target / "references"
    refs.mkdir(parents=True, exist_ok=True)

    meta_path = source / "workflow.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    training_mode = meta.get("training_mode") or args.training_mode

    actions = []
    for action_file in sorted(source.glob("turn-*/action.json")):
        data = json.loads(action_file.read_text())
        tool = data.get("tool") or data.get("action") or data.get("name") or "unknown"
        arguments = safe_value(data.get("arguments") or data.get("input") or {})
        actions.append((tool, arguments, action_file.parent.name))
    if not actions:
        raise SystemExit("No recorded CUA actions found. Stop after performing Computer Use actions, then build.")
    title = args.name.strip()

    skill_extra = ""
    if training_mode == "browser-use":
        skill_extra = """
## Browser-Use Training

This recording was captured in browser-use training mode. The training artifacts
include element selectors, DOM paths, interaction patterns, decision points,
and expected outcomes.

- Review `training/browser-use-patterns.md` for learned interaction patterns
- Import `training/selectors.json` for adaptive element targeting
- Run `training/assertions.json` as test cases after replay
"""
    skill = f'''---
name: recorded-{slug(args.name)}
description: Replay or adapt the demonstrated {title} desktop workflow. Use only when the operator explicitly requests this recorded workflow.
---

# {title}

This draft was generated from a local Cua Driver trajectory. Read `references/actions.md` before use.

## Guardrails

- Confirm the target app, account, and starting state.
- Never enter credentials, payment data, or authentication codes from the trace.
- Prefer semantic Computer Use targets over recorded coordinates.
- Ask before any submission, purchase, deletion, message, upload, or other external side effect.
- For exact native replay, require the operator's explicit approval and run:

```sh
record-replay replay {slug(args.name)} --confirm
```
{skill_extra}'''
    (target / "SKILL.md").write_text(skill)
    lines = [f"# Recorded actions: {title}", "", f"Source: `{source}`", ""]
    for index, (tool, arguments, turn) in enumerate(actions, 1):
        lines.extend([f"## {index}. `{tool}`", "", f"Turn: `{turn}`", "", "```json", json.dumps(arguments, indent=2), "```", ""])
    (refs / "actions.md").write_text("\n".join(lines))

    if training_mode == "browser-use":
        train_dir = target / "training"
        train_dir.mkdir(parents=True, exist_ok=True)

        patterns = [
            "# Browser-Use Patterns",
            "",
            f"Source recording: `{source}`",
            f"Captured at: {meta.get('created_at', 'unknown')}",
            "",
            "## Interaction Patterns",
            "",
        ]
        selectors = {}
        assertions = []
        for index, (tool, arguments, turn) in enumerate(actions, 1):
            patterns.append(f"### Step {index}: `{tool}`")
            patterns.append("")
            patterns.append("```json")
            patterns.append(json.dumps({"tool": tool, "arguments": arguments}, indent=2))
            patterns.append("```")
            patterns.append("")
            selectors[f"step-{index}"] = {"tool": tool, "turn": turn, "arguments": arguments}
            assertions.append({
                "step": index,
                "tool": tool,
                "turn": turn,
                "expected": f"Action {tool} completed successfully at turn {turn}",
            })

        (train_dir / "browser-use-patterns.md").write_text("\n".join(patterns))
        (train_dir / "selectors.json").write_text(json.dumps(selectors, indent=2) + "\n")
        (train_dir / "assertions.json").write_text(json.dumps(assertions, indent=2) + "\n")

        # Also mirror to the centralized training directory
        central_train = Path.home() / ".hermes" / "training" / "browser-use" / slug(args.name)
        central_train.mkdir(parents=True, exist_ok=True)
        (central_train / "training-data.json").write_text(json.dumps({
            "workflow": slug(args.name),
            "title": title,
            "created_at": meta.get("created_at", datetime.now().astimezone().isoformat()),
            "steps": [{"tool": t, "arguments": a, "turn": tn} for t, a, tn in actions],
            "selectors": selectors,
            "assertions": assertions,
        }, indent=2) + "\n")
        (central_train / "test-cases.json").write_text(json.dumps(assertions, indent=2) + "\n")
        print(f"Training artifacts: {train_dir}")
        print(f"  browser-use-patterns.md  - interaction patterns")
        print(f"  selectors.json           - element selectors per step")
        print(f"  assertions.json          - expected outcomes per step")
        print(f"Central training data: {central_train}")

    print(target)
    print("Draft skill created. Inspect and replace brittle coordinates before normal use.")


def replay(args: argparse.Namespace) -> None:
    if not args.confirm:
        raise SystemExit("Replay can click and type. Re-run with --confirm after inspecting the trace.")
    source = workflow_dir(args.name)
    payload = {"dir": str(source), "delay_ms": args.delay_ms, "stop_on_error": not args.best_effort}
    print(json.dumps(call("replay_trajectory", payload), indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="record-replay")
    sub = p.add_subparsers(dest="command", required=True)
    start_p = sub.add_parser("start")
    start_p.add_argument("name")
    start_p.add_argument("--video", action="store_true")
    start_p.add_argument("--training-mode", choices=["browser-use"], default=None,
                         help="Capture selectors, DOM, and decision points for browser-use agent training")
    start_p.set_defaults(func=start)
    sub.add_parser("stop").set_defaults(func=stop)
    sub.add_parser("status").set_defaults(func=status)
    sub.add_parser("list").set_defaults(func=list_recordings)
    build_p = sub.add_parser("build")
    build_p.add_argument("name")
    build_p.add_argument("--training-mode", choices=["browser-use"], default=None,
                         help="Generate browser-use training artifacts (selectors, patterns, assertions)")
    build_p.set_defaults(func=build)
    replay_p = sub.add_parser("replay")
    replay_p.add_argument("name")
    replay_p.add_argument("--confirm", action="store_true")
    replay_p.add_argument("--delay-ms", type=int, default=700)
    replay_p.add_argument("--best-effort", action="store_true")
    replay_p.set_defaults(func=replay)
    return p


if __name__ == "__main__":
    parsed = parser().parse_args()
    parsed.func(parsed)
