# 🧠 Berbat Commit Mesajlarından Kurtulun

Berbat commit mesajları yazmayı bırak.
Sadece `git commit -m ""` çalıştır — biz güzel bir commit mesajı oluşturmayı hallederiz.

Şu anda GPT-5-mini kullanır.
---

## 🚀 Kurulum

```bash
brew tap Musti7even/no-shit-commit-messages
brew install no-shit-commit-messages
export OPENAI_API_KEY=sk-...
alias git='nscm'
```

---

## 💡 Kullanım

```bash
git add .
git commit -m ""        # → AI commit mesajı oluşturur
git commit -m "manual"  # → normal davranış gösterir, sana max özgürlük sağlar
git commit               # → her zamanki gibi editörü açar
```

Örnek çıktı:

```
🧠 Commit mesajı oluşturuluyor…
💬 "feat(ui): improve layout responsiveness on profile page"

 2 dosya değişti, 10 ekleme(+), 3 silme(-)
```

---

## ⚙️ Yapılandırma

İsteğe bağlı `~/.nscmrc`:

```yaml
provider: openai
model: gpt-5-mini-2025-08-07
style: conventional
```

Ortam değişkenleri config dosyasını geçersiz kılar:

- `NSCM_PROVIDER` — kullanılacak sağlayıcı (varsayılan: `openai`)
- `NSCM_MODEL` — model tanımlayıcısı (varsayılan: `gpt-5-mini-2025-08-07`)
- `NSCM_STYLE` — stil ipucu (varsayılan: `conventional`)
- `OPENAI_API_KEY` — sağlayıcı `openai` olduğunda gereklidir

---

## 🛠️ Geliştirme

Proje düzeni:

```
no-shit-commit-messages/
├─ nscm.py
├─ brew/
│  └─ no-shit-commit-messages.rb
├─ README.md
├─ LICENSE
└─ .github/workflows/release.yml
```

Homebrew olmadan yerel olarak çalıştır:

```bash
export OPENAI_API_KEY=sk-...
python3 ./nscm.py commit -m ""
```

---

## 🧭 Yol Haritası

- Ollama veya daha hızlı model sağlayıcıları
- daha iyi commit mesajları için ek bağlam
- İsteğe bağlı etkileşimli onay
- `--dry-run` ön izlemeleri
- Stabil olduğunda Homebrew core'a gönder

---

MIT © 2025 / Mustafa Yenler


