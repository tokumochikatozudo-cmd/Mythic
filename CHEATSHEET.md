# MYTHIC Quick-Start Cheat Sheet
*OpenMythos x PentestGPT — Advanced AI Pentesting System*

---

## Launch Commands

```powershell
# Interactive mode (Ollama — local, free, offline-capable)
py -3.12 C:\UNLISTED\mythic.py legacy

# Autonomous mode (Claude Code — free, needs login once)
py -3.12 C:\UNLISTED\mythic.py agent --target 10.10.11.234 --goal "Capture the flag"

# System health check
py -3.12 C:\UNLISTED\mythic.py status

# Full backend smoke test
py -3.12 C:\UNLISTED\mythic.py smoke

# OpenMythos RDT architecture demo
py -3.12 C:\UNLISTED\mythic.py mythos

# Post-session lesson recording
py -3.12 C:\UNLISTED\debrief.py
py -3.12 C:\UNLISTED\debrief.py --search "SSRF"
```

Or just double-click: `START_INTERACTIVE.bat` / `STATUS.bat` / `DEBRIEF.bat`

---

## First-Time Claude Setup (one-time only)

```powershell
# Open PowerShell and run:
claude /login
# Follow the browser login flow — then you're set forever
```

---

## Interactive Mode Commands (inside `mythic.py legacy`)

| Command | What it does |
|---------|-------------|
| `next` | Feed tool output → AI updates task tree + picks next step |
| `more` | Expand current task into exact step-by-step commands |
| `todo` | Show full Penetration Testing Tree (PTT) |
| `discuss` | Free chat — ask anything, share observations |
| `brainstorm` | AI lists ALL possible approaches (good when stuck) |
| `quit` | Save session and exit |

**Typical CTF workflow:**
```
1. Start: py -3.12 mythic.py legacy
2. Describe: "HTB machine at 10.129.x.x, Linux, unknown services"
3. Run nmap → paste output → type: next → select: tool
4. AI builds PTT + suggests next task
5. Type: more → get exact commands
6. Run commands → paste results → type: next
7. Repeat until flag captured
8. Exit: quit
9. Debrief: py -3.12 debrief.py
```

---

## VRAM Guide — RTX 3050 Ti (4GB)

| Model | VRAM | Status | Use for |
|-------|------|--------|---------|
| `MFDoom/deepseek-r1-tool-calling:7b` | ~3.8GB | ✅ Fits | **Default reasoning** |
| `qwen3.5:2b` | ~1.6GB | ✅ Fits | **Default parser** |
| `qwen3:0.6b` | ~0.4GB | ✅ Fits | Ultra-fast parser |
| `deepseek-r1:14b` | ~9GB | ⚠️ CPU offload | Deep reasoning (slow) |
| `qwen3.5:9b` | ~6.6GB | ⚠️ CPU offload | Balanced (slow) |
| `gemma2:9b` | ~5.4GB | ⚠️ CPU offload | Alternative |

```powershell
# Default (safe, fits in VRAM):
py -3.12 mythic.py legacy

# Deep reasoning (CPU offload, slower but more powerful):
py -3.12 mythic.py legacy --reasoning-model ollama:deepseek-r1:14b
```

---

## First HTB Session

```powershell
# 1. Connect HTB OpenVPN
# 2. Spawn your target on HTB website
# 3. Run:
py -3.12 C:\UNLISTED\mythic.py agent `
  --target 10.129.x.x `
  --goal "HackTheBox authorized machine. Capture user and root flags."

# OR interactive for more control:
py -3.12 C:\UNLISTED\mythic.py legacy
# Describe: "HTB machine at 10.129.x.x, need to capture flags"
```

---

## CTF Web Challenge

```powershell
py -3.12 C:\UNLISTED\mythic.py agent `
  --target "http://challenge.ctf.io:5000" `
  --goal "CTF web challenge. Find the flag in format FLAG{...}"
```

---

## After Every Session

```powershell
py -3.12 C:\UNLISTED\debrief.py
```
Records: what worked, what failed, key lessons → builds your **personal knowledge base**.

Search lessons anytime:
```powershell
py -3.12 C:\UNLISTED\debrief.py --search "privilege escalation"
py -3.12 C:\UNLISTED\debrief.py --search "SQL injection"
```

---

## File Map

| File | Purpose |
|------|---------|
| `C:\UNLISTED\mythic.py` | **Main launcher** |
| `C:\UNLISTED\debrief.py` | Lesson recorder |
| `C:\UNLISTED\README.md` | Full documentation |
| `C:\UNLISTED\START_INTERACTIVE.bat` | Double-click for interactive mode |
| `C:\UNLISTED\sessions\` | Past session JSON files |
| `C:\UNLISTED\lessons.jsonl` | Searchable lesson database |
| `C:\UNLISTED\PentestGPT\logs\` | Session transcripts |

---

*MYTHIC v1.0 | OpenMythos x PentestGPT | RTX 3050 Ti | torch 2.6.0+cu124*
