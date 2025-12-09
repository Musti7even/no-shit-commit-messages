# 🧠 No-Shit-Commit-Messages

Stop writing shitty commit messages.  
Just run `git commit -m ""` — we’ll handle generating a nice commit message.

Uses GPT-5-mini currently.
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

### Generate and Commit

```bash
git add .
git commit -m ""        # → AI generates commit message and commits
git commit -m "manual"  # → still behaves normally, to give you max freedom
git commit               # → opens editor as usual
```

### Preview Message (New!)

Generate a commit message without committing:

```bash
git add .
git commit -p           # → Generates message and shows a preview
```

Preview output example:

```
🧠 Generating commit message…
┌─────────────────────────────────────────────────────────┐
│                    📝 Commit Preview                     │
└─────────────────────────────────────────────────────────┘

Message:
  feat(ui): improve layout responsiveness on profile page

Stats:
  📄 Files changed: 2
  ➕ Insertions: 10
  ➖ Deletions: 3
  📊 Diff lines: 45

┌─────────────────────────────────────────────────────────┐
```

You can also use the long form: `git commit --preview`

---

## ⚙️ Configuration

Optional `~/.nscmrc`:

```yaml
provider: openai
model: gpt-5-mini-2025-08-07
style: conventional
```

Environment variables override the config file:

- `NSCM_PROVIDER` — provider to use (default: `openai`)
- `NSCM_MODEL` — model identifier (default: `gpt-5-mini-2025-08-07`)
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

- Ollama or even faster model providers
- additional context for better commit messages
- Optional interactive confirmation (accept/regenerate/edit)
- Submit to Homebrew core once stable

---

MIT © 2025 / Mustafa Yenler


