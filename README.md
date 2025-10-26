# 🧠 No-Shit-Commit-Messages

Stop writing shitty commit messages.  
Just run `git commit -m ""` — we’ll handle the rest.

---

## 🚀 Install

```bash
brew tap Musti7even/no-shit-commit-messages
brew install no-shit-commit-messages
export OPENAI_API_KEY=sk-...
alias git='nscm'
```

---

## 💡 Usage

```bash
git add .
git commit -m ""        # → AI generates commit message
git commit -m "         # → AI generates commit message (unclosed quote)
git commit -m "manual"  # → behaves normally
git commit               # → opens editor as usual
```

Example output:

```
🧠 Generating commit message…
💬 feat(ui): improve layout responsiveness on profile page
[main 9b3c2d1] feat(ui): improve layout responsiveness on profile page
 2 files changed, 10 insertions(+), 3 deletions(-)
```

---

## ⚙️ Configuration

Optional `~/.nscmrc`:

```yaml
provider: openai
model: gpt-4o-mini
style: conventional
```

Environment variables override the config file:

- `NSCM_PROVIDER` — provider to use (default: `openai`)
- `NSCM_MODEL` — model identifier (default: `gpt-4o-mini`)
- `NSCM_STYLE` — style hint (default: `conventional`)
- `OPENAI_API_KEY` — required when provider is `openai`

---

## 🛠️ Development

Project layout:

```
no-shit-commit-messages/
├─ nscm.py
├─ brew/
│  └─ no-shit-commit-messages.rb
├─ README.md
├─ LICENSE
└─ .github/workflows/release.yml
```

Run locally without Homebrew:

```bash
export OPENAI_API_KEY=sk-...
python3 ./nscm.py commit -m ""
```

---

## 🧭 Roadmap

- Ollama / Anthropic providers
- Multiline commit bodies
- Optional interactive confirmation
- `--dry-run` previews
- Submit to Homebrew core once stable

---

MIT © 2025 Arrow / Mustafa Yenler


