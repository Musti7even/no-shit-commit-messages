#!/usr/bin/env python3
"""
nscm: No-Shit Commit Messages

Lightweight CLI wrapper around git that auto-generates commit messages with an LLM
when the user invokes: `git commit -m ""`.

Installation recommendation:
  - alias git='nscm'

Environment variables:
  - OPENAI_API_KEY: API key for OpenAI (required for provider=openai)
  - NSCM_PROVIDER: provider to use (default: openai)
  - NSCM_MODEL: model identifier (default: gpt-4o-mini)
  - NSCM_STYLE: style hint (e.g., conventional) (default: conventional)

Optional config file at ~/.nscmrc with simple key: value pairs, e.g.:
  provider: openai
  model: gpt-4o-mini
  style: conventional

This file intentionally avoids heavy dependencies. It will try to use `requests`
if available, otherwise falls back to urllib from the standard library.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple


def _print_err(message: str) -> None:
    sys.stderr.write(message + "\n")


def _run_git(args: List[str]) -> int:
    """Execute `git` with given args, stream output to current stdio, return exit code."""
    completed = subprocess.run(["git"] + args)
    return completed.returncode


def _capture_git(args: List[str]) -> Tuple[int, str, str]:
    """Execute `git` and capture stdout/stderr."""
    completed = subprocess.run(["git"] + args, capture_output=True, text=True)
    return completed.returncode, completed.stdout, completed.stderr


def _read_simple_rc(path: str) -> Dict[str, str]:
    """
    Read a very simple rc file where each non-empty, non-comment line is
    `key: value`. Leading/trailing whitespace is trimmed. No nesting.
    """
    config: Dict[str, str] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key and value is not None:
                    config[key] = value
    except FileNotFoundError:
        pass
    except Exception as exc:
        _print_err(f"Warning: failed to read ~/.nscmrc: {exc}")
    return config


def _get_config() -> Dict[str, str]:
    rc = _read_simple_rc(os.path.expanduser("~/.nscmrc"))
    return {
        "provider": os.getenv("NSCM_PROVIDER", rc.get("provider", "openai")),
        "model": os.getenv("NSCM_MODEL", rc.get("model", "gpt-4o-mini")),
        "style": os.getenv("NSCM_STYLE", rc.get("style", "conventional")),
    }


def _get_staged_diff(max_lines: int = 500) -> str:
    """Return the staged diff, truncated to max_lines."""
    code, out, err = _capture_git(["diff", "--cached"])
    if code != 0:
        raise RuntimeError(err.strip() or "failed to get staged diff")
    if not out.strip():
        return ""
    lines = out.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + ["\n... (truncated) ..."]
    return "\n".join(lines)


def _select_http_impl():
    """Return (post_fn, name) where post_fn(url, headers, json_payload, timeout)->(status, text)."""
    try:
        import requests  # type: ignore

        def _post(url: str, headers: Dict[str, str], payload: Dict, timeout: int) -> Tuple[int, str]:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            return resp.status_code, resp.text

        return _post, "requests"
    except Exception:
        import urllib.request

        def _post(url: str, headers: Dict[str, str], payload: Dict, timeout: int) -> Tuple[int, str]:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
                body = resp.read().decode("utf-8")
                return resp.getcode(), body

        return _post, "urllib"


def _openai_chat_complete(model: str, messages: List[Dict[str, str]], timeout_s: int = 20) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 120,
    }

    post_fn, name = _select_http_impl()
    try:
        status, text = post_fn(url, headers, payload, timeout_s)
    except Exception as exc:
        raise RuntimeError(f"OpenAI request failed ({name}): {exc}")

    if status < 200 or status >= 300:
        # Avoid printing sensitive content
        raise RuntimeError(f"OpenAI API error: HTTP {status}")

    try:
        data = json.loads(text)
        content = data["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as exc:
        raise RuntimeError(f"Unexpected OpenAI response format: {exc}")


def _generate_message(diff: str, provider: str, model: str, style: str) -> str:
    if provider != "openai":
        raise RuntimeError(f"Unsupported provider: {provider}")

    system_style = (
        "Write a short, clear, conventional git commit message. "
        "Single-line subject only, <= 72 chars, present tense, no trailing period."
    )
    if style.lower().startswith("conventional"):
        system_style += " Use Conventional Commits format: type(scope?): subject."

    messages = [
        {"role": "system", "content": system_style},
        {
            "role": "user",
            "content": (
                "Summarize the staged diff into a single-line commit subject. "
                "Focus on intent and impact, not code details.\n\nDIFF:\n" + diff
            ),
        },
    ]

    content = _openai_chat_complete(model=model, messages=messages)
    # Keep only first line, trim
    first_line = content.splitlines()[0].strip()
    # Guardrail length
    if len(first_line) > 120:
        first_line = first_line[:120].rstrip()
    return first_line


def _extract_commit_args(argv: List[str]) -> Tuple[bool, List[str]]:
    """
    Inspect argv (after program name) to detect `commit -m ""` or `commit --message ""` or `commit -m "`.
    Returns (should_generate, passthrough_args_without_empty_message).
    If not a commit command or message is non-empty, returns (False, original args-after-git).
    """
    if not argv:
        return False, argv
    if argv[0] != "commit":
        return False, argv

    args = argv[1:]
    should_generate = False
    cleaned: List[str] = ["commit"]

    i = 0
    while i < len(args):
        a = args[i]
        if a == "-m" or a == "--message":
            # If next token exists, check if empty or just a quotation mark
            if i + 1 < len(args):
                val = args[i + 1]
                if val == "" or val == '"' or val == "'":
                    should_generate = True
                    i += 2
                    continue
                else:
                    # Non-empty message → passthrough unchanged
                    return False, ["commit"] + args
            else:
                # `-m` with no value: treat as request to generate
                should_generate = True
                i += 1
                continue
        else:
            cleaned.append(a)
            i += 1

    return should_generate, cleaned


def main() -> int:
    argv = sys.argv[1:]

    # Detect generation flow
    should_generate, passthrough = _extract_commit_args(argv)
    if not should_generate:
        # Simple passthrough to real git
        return _run_git(argv)

    # Generate commit message path
    try:
        diff = _get_staged_diff(max_lines=500)
    except Exception as exc:
        _print_err(f"❌ Failed to read staged diff: {exc}")
        return 1

    if not diff.strip():
        _print_err("❌ No staged changes.")
        return 1

    cfg = _get_config()
    provider = cfg["provider"]
    model = cfg["model"]
    style = cfg["style"]

    print("🧠 Generating commit message…")
    start = time.time()
    try:
        message = _generate_message(diff=diff, provider=provider, model=model, style=style)
    except Exception as exc:
        _print_err(f"❌ Generation failed: {exc}")
        return 1
    dur_ms = int((time.time() - start) * 1000)

    # Safety: ensure message is not empty
    if not message.strip():
        _print_err("❌ Model returned empty message.")
        return 1

    print(f"💬 {message}")

    # Compose commit args: existing flags + -m <message>
    commit_args = passthrough + ["-m", message]

    # Execute git commit
    code = _run_git(commit_args)
    return code


if __name__ == "__main__":
    sys.exit(main())


