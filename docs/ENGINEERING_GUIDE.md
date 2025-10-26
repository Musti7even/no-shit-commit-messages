# 🧠 Project Brief: no-shit-commit-messages

### Summary

We’re building a lightweight open-source CLI tool that automatically generates git commit messages using an LLM. It should behave exactly like Git — except when a user types:

```bash
git commit -m ""
```

…the tool generates a high-quality commit message from the staged diff and uses it automatically.

---

## 🎯 Goal

A developer-friendly, installable command-line utility that replaces “shitty commit messages” with smart AI-generated ones.

It should:

- Work via `brew install no-shit-commit-messages`
- Require no extra syntax or commands
- Respect normal git behavior (`git commit -m "manual message"` still works)
- Support OpenAI (and optionally Ollama / Anthropic)
- Be portable across macOS and Linux

---

## 🧱 Architecture Overview

| Component | Description |
| --- | --- |
| `nscm` CLI | Python 3.11+ binary. Wraps native git and intercepts `commit -m ""`. |
| Config file (`~/.nscmrc`) | Optional user config for provider/model defaults. |
| Homebrew Formula | Easy installation via tap + install. |
| GitHub Repository | Source code, release tags, formula file, docs. |
| GitHub Actions CI | Publishes releases + brew formula updates. |

---

## ⚙️ Implementation Details

### 1) Core CLI logic (`nscm.py`)

- Capture all git CLI arguments.
- If `git commit -m` is followed by an empty string or nothing, trigger AI generation.
- Fetch the staged diff via `git diff --cached` (truncate >500 lines).
- Send to LLM API (OpenAI by default).
- Print generated message and run: `git commit -m "<generated>"`.
- Otherwise pass through to real `git` unchanged.

### 2) Homebrew Formula (`brew/no-shit-commit-messages.rb`)

Provide install instructions, python dep, and caveats for alias/env.

### 3) Repository Setup

```
no-shit-commit-messages/
├─ nscm.py
├─ brew/
│  └─ no-shit-commit-messages.rb
├─ README.md
├─ LICENSE (MIT)
└─ .github/workflows/release.yml
```

### 4) README

Include install, usage, config, and example output.

### 5) GitHub Actions CI

Trigger on tags `v*`; compute SHA, prepare for formula updates.

---

## 🧭 Developer Guidelines

- Keep it simple, <300 LOC, readable, and well-commented.
- Gracefully handle missing API keys, empty diffs, timeouts.
- Only use `requests` if available; otherwise stdlib.
- Truncate diff to keep latency fast.
- Never log diff contents.
- Test on macOS + Linux.
- Add demo GIF and example output in README.
- Use SemVer and tag releases.

---

## 🔜 Future roadmap ideas

- Ollama provider (`NSCM_PROVIDER=ollama`)
- Anthropic provider (`NSCM_PROVIDER=anthropic`)
- Multiline commit bodies
- Optional interactive confirmation step
- `--dry-run` preview mode
- Submit to Homebrew core once stable

---

## ✅ Deliverables checklist

| Deliverable | Description |
| --- | --- |
| `nscm.py` | Working CLI tool |
| `brew/no-shit-commit-messages.rb` | Valid formula file |
| `README.md` | With usage + demo |
| `LICENSE` | MIT |
| `.github/workflows/release.yml` | CI pipeline |
| GitHub release | v0.1.0 tagged + tarball |
| SHA updated in formula | Verified brew install works |

---

MIT © 2025 / Mustafa Yenler


