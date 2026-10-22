



# 🛡️ MYTHIC — Advanced Adversarial OffSec AI Framework
### `OpenMythos × PentestGPT` | Automated Penetration Testing Engine

> *"Security is not a static state, but a continuous evolution. To defend against the algorithms of tomorrow, we must think like the adversaries of today."*
> — Neo Tanju Allabib

> For CTF training + authorized professional pentesting.
> Local inference via Ollama (free, offline). Autonomous pipeline via Claude Code (free CLI).

---

https://github.com/user-attachments/assets/ced37cf2-0ee8-4c79-ade4-1ffa7536fc81

## 📌 Background & The Problem

In the modern cybersecurity landscape, enterprise networks and LLM applications face critical vulnerabilities stemming from a fundamental asymmetry between attackers and defenders:

1. **Slow, Manual Pentesting Lifecycles:** Traditional vulnerability assessments and red-teaming operations take weeks to plan and execute, leaving critical infrastructure exposed to rapidly evolving threats.
2. **Predictable & Static Exploit Payloads:** Conventional defensive firewalls and Intrusion Detection Systems (IDS) rely on signature-based detection. They easily block static scripts but fail against Advanced Persistent Threats (APTs) that utilize adaptive, polymorphic techniques.
3. **Fragile LLM Guardrails:** Current AI alignment mechanisms are rigidly programmed and lack exposure to fluid, adversarial thinking. They fail to anticipate semantic edge-cases, allowing malicious actors to bypass security prompts with relative ease.
4. **The "Adaptability Gap":** There is a distinct lack of tools that can autonomously scan, learn, and mutate their approach in real-time based on the defensive countermeasures they encounter.

These problems share one root cause: **security testing is too static for a dynamic threat landscape.** Mythic bridges this gap by introducing an autonomous, adversarial AI engine that acts as a spar partner for enterprise networks and AI models alike.

---

## 🎯 Project Focus: Proactive Adversarial Defense

**Mythic** operates on the core principle of *Automated Proactive Defense*. Just as immune systems require exposure to pathogens to build resilience, networks and AI models require exposure to highly sophisticated, adaptive attacks to forge unbreakable security postures. 

By unifying offensive security (OffSec) with advanced machine learning, Mythic addresses critical security challenges across multiple domains:

| Domain | Mythic's Role |
|---|---|
| **Enterprise Network Security** | Automates the discovery and exploitation of critical network vulnerabilities using dynamic payload generation, ensuring infrastructure is tested against APT-level sophistication. |
| **AI Alignment & Safety** | Systematically stress-tests LLM guardrails through algorithmic prompt-injection, discovering semantic edge-cases before malicious actors can exploit them. |
| **Incident Response Readiness** | Generates real-time, mutated attack telemetry, allowing Security Operations Centers (SOC) to train against unpredictable, AI-driven intrusion attempts. |
| **Vulnerability Lifecycle Management** | Drastically reduces the time between vulnerability discovery and remediation by autonomously validating the exploitability of active CVEs in target environments. |

---

## 💡 The Mythic Solution & The Five Pillars

Mythic solves modern security bottlenecks through a sophisticated three-pillar approach, combined with five core design philosophies:

1. **Adversarial Prompt Engineering (Mythos AI):** Utilizes heavily fine-tuned linguistic models designed to autonomously discover semantic edge-cases. It systematically generates next-gen "jailbreaks" to evaluate LLM alignment robustly, treating language itself as an attack vector.
2. **Automated Exploit Orchestration (GPTPentest):** A specialized security model integrated directly with terminal-native APIs. It serves as the brain behind the operation, seamlessly interfacing with established network security frameworks like Metasploit to launch coordinated attacks without human bottlenecking.
3. **Intelligent Payload Mutation (Adaptive Engine):** An automated feedback loop that scans target infrastructure, references active CVE databases, and dynamically alters its exploit code at runtime. If an IDS blocks a payload, Mythic instantly re-engineers the code structure to outmaneuver the active defense.

### The Five Pillars

| Pillar | How MYTHIC achieves it |
|--------|----------------------|
| **Comfortable** | Single `mythic.py` entry point. Natural language goals. Session persistence. |
| **Overpowered** | DeepSeek-R1 + PentestGPT multi-stage pipeline + Claude Code autonomous tools. |
| **Creative** | R1 extended thinking + RDT variable-depth reasoning + hypothesis-driven agent. |
| **Adaptive** | Claude Code (online) + Ollama (offline) — swappable, works anywhere. |
| **Aware** | Live progress, session logs, post-run debrief in `debrief.py`. |

---

## 🛠 Development Methodology

Mythic was engineered using an **Agile Red-Teaming** methodology. This approach ensures the framework remains relevant against zero-day threats:

- **Continuous Feedback Loops:** The engine is built to learn from failure. Every blocked payload or rejected prompt is fed back into the model to improve the next iteration.
- **Modular Integration:** The prompt-injection engine (Mythos AI) and the network exploitation engine (GPTPentest) operate as independent microservices.
- **Automated Sandbox Testing:** Exploit pipelines are continuously tested against isolated, simulated environments.

---

## 💻 Technology Stack & Architecture

Mythic is built on a cutting-edge, high-performance stack designed for interoperability between machine learning models and low-level system execution:

- **Core Logic:** Python 3.12 / 3.14 (Asynchronous execution for rapid scanning).
- **Linguistic Engine (OpenMythos):** Recurrent-Depth Transformer (RDT) architecture via PyTorch (torch 2.6.0+cu124) on NVIDIA RTX hardware.
- **OffSec Integration:** Claude Code CLI (Autonomous pipeline) and Ollama local models (Interactive REPL).
- **Session Management:** SQLite session stores and custom C2 telemetry logging.

### System Architecture Layout

```text
                    +---------------------------------------+
                    |         MYTHIC LAUNCHER               |
                    |         mythic.py                     |
                    +----------+---------------+------------+
                               |               |
              +----------------+               +------------------+
              v                                                   v
+---------------------------+                   +--------------------------------+
|   pentestgpt-AGENT        |                   |  pentestgpt-LEGACY             |
|   (Interactive REPL)      |                   |  (Autonomous pipeline)         |
|                           |                   |                                |
|  Claude Code CLI (free)   |                   |  Ollama local models:          |
|  Supervisor -> Executor   |                   |    deepseek-r1-tool-calling:7b |
|  SQLite session store     |                   |    qwen3.5:2b (parser)         |
+---------------------------+                   +--------------------------------+
                               |
                               v
               +-------------------------------+
               |     OpenMythos RDT            |
               |  (Research + reasoning layer) |
               |                               |
               |  Prelude -> [Loop x T] -> Coda|
               |  torch 2.6.0+cu124            |
               |  NVIDIA RTX 3050 Ti           |
               +-------------------------------+
```

---

## 📁 Workspace Layout

```text
C:\UNLISTED\
├── mythic.py             <- YOU ARE HERE — unified launcher
├── debrief.py            <- Post-run lesson tracker
├── CHEATSHEET.md         <- Quick reference (keep open during sessions)
├── PentestGPT\
│   ├── pentestgpt_agent\ <- Autonomous pipeline (Claude Code backend)
│   ├── pentestgpt_legacy\<- Interactive mode (Ollama backend)
│   └── .venv\            <- Python 3.14 venv (fully installed)
├── OpenMythos\           <- Recurrent-Depth Transformer (RDT) architecture
│   └── .venv\            <- Python 3.12 venv (torch 2.6.0+cu124, CUDA)
├── sessions\             <- Auto-created. Your run history.
└── logs\                 <- Auto-created. Session transcripts.
```

---

## 🚀 Quick Start

### Option A — Autonomous Mode (Claude Code, FREE after one-time login)

```powershell
# One-time setup: run from C:\UNLISTED
cd C:\UNLISTED
claude /login

# CTF: capture a flag
py -3.12 mythic.py agent --target 10.10.11.234 --goal "Capture the flag"

# Pentest: full discovery + report
py -3.12 mythic.py agent --target 10.10.11.234 --goal "Full pentest, document all findings"

# Resume a previous session
py -3.12 mythic.py agent --target 10.10.11.234 --goal "Capture the flag" --resume
```

### Option B — Interactive Mode (Ollama, 100% LOCAL, FREE, works offline)

```powershell
# Default: MFDoom/deepseek-r1-tool-calling:7b (fits in 4GB VRAM)
py -3.12 mythic.py legacy

# Use deepseek-r1:14b as main brain (CPU offload, slower but more powerful)
py -3.12 mythic.py legacy --reasoning-model ollama:deepseek-r1:14b

# Use qwen3.5:9b
py -3.12 mythic.py legacy --reasoning-model ollama:qwen3.5:9b
```

**Interactive REPL commands:**
| Command | Action |
|---------|--------|
| `next` | Feed tool output → AI updates task tree |
| `more` | Get step-by-step commands for current task |
| `todo` | Show full Penetration Testing Tree (PTT) |
| `discuss` | Free-form chat |
| `brainstorm` | AI lists all possible approaches |
| `quit` | Save and exit |

### Option C — OpenMythos RDT Architecture Test

```powershell
py -3.12 mythic.py mythos
```

---

## 📊 System Check & Available Local Models (Ollama)

### System Check

```powershell
# Full status: GPU, models, sessions
py -3.12 mythic.py status

# Smoke test all backends (should be 5/5)
py -3.12 mythic.py smoke
```

### Available Local Models (Ollama)

| Model | Size | VRAM | Best for |
|-------|------|------|----------|
| `MFDoom/deepseek-r1-tool-calling:7b` | 4.7GB | ✅ Fits 4GB | **Default reasoning + tool calls** |
| `qwen3.5:2b` | 2.7GB | ✅ Fits | **Default parser** |
| `deepseek-r1:14b` | 9GB | ⚠️ CPU offload | Deep reasoning (slower) |
| `qwen3.5:9b` | 6.6GB | ⚠️ CPU offload | Balanced |
| `qwen3:0.6b` | 522MB | ✅ Fits | Ultra-fast auxiliary |

> **Note:** The RTX 3050 Ti has 4GB VRAM. Models >4GB use Ollama's CPU offload — they work but are slower.

---

## 🧠 After Every Session — Debrief

Mythic learns from its engagements. Use the debrief tool to process session logs and track lessons learned:

```powershell
py -3.12 debrief.py                    # Full wizard
py -3.12 debrief.py --lessons          # Review all lessons
py -3.12 debrief.py --search "XSS"    # Search by keyword
```

---

## 🔬 Results & Quantifiable Milestones

Project Mythic has successfully demonstrated the viability of automated, AI-driven red-teaming operations. During extensive simulated environments and authorized stress-tests, the framework achieved:

- **Unprecedented Efficiency:** Reduced the reconnaissance-to-exploitation lifecycle from days to minutes, autonomously identifying critical network and model vulnerabilities.
- **High Exploit Success Rate:** Orchestrated smooth and intelligent deployments with significantly higher success rates than traditional static testing scripts, successfully bypassing industry-standard IDS through its Intelligent Payload Mutation loop.
- **Robust LLM Alignment Testing:** Systematically generated novel prompt-injections that successfully mapped the alignment boundaries of state-of-the-art LLMs, proving the necessity for fluid, adversarial training in AI development.

This project currently stands as a cutting-edge standard for proactive adversarial defense.

---

## ⚖️ Ethics — Non-Negotiable

1. **Authorized targets only** — HTB, THM, your own lab, or written permission.
2. **No production systems** without a signed scope document.
3. **Human review** before any destructive or irreversible action.
4. **Responsible disclosure** for any real bugs found in bug bounty scope.

---

## 🌱 Vision

The integration of AI into cybersecurity is no longer an option; it is an imperative. As networks become more complex and Artificial Intelligence becomes deeply woven into global infrastructure, the threats against them will become fully automated. 

**Project Mythic** was born from the belief that we cannot defend against machine-speed attacks with human-speed responses. By building an OffSec AI framework that continuously adapts, learns, and mutates, we are not just creating a weapon—we are forging the ultimate whetstone upon which the next generation of cybersecurity defenses will be sharpened. 

---

## Credits

Architected, developed, and engineered to push the boundaries of proactive cybersecurity.

**Principal Security Researcher & Lead Engineer:**  
Neo Tanju Allabib 

*MYTHIC v1.0 | Advanced Adversarial OffSec AI Framework | OpenMythos × PentestGPT*  
*torch 2.6.0+cu124 | RTX 3050 Ti | Claude Code v2.1.212*
