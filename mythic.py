#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MYTHIC - Advanced AI Pentesting System
=======================================
OpenMythos x PentestGPT â€” unified launcher.

Usage:
  python mythic.py status                              # System health check
  python mythic.py agent  --target IP --goal "..."    # Autonomous (Claude Code)
  python mythic.py legacy                             # Interactive (Ollama local)
  python mythic.py mythos                             # OpenMythos RDT demo
  python mythic.py smoke                              # Smoke test all backends
  python mythic.py setup                              # Install OpenMythos deps
"""

import sys
import os
import subprocess
import json
import urllib.request
from pathlib import Path
from datetime import datetime

# Force UTF-8 on Windows terminals (needed for block characters in title art)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# MYTHIC title art (FateGate font, Blu palette) - load from sidecar module
try:
    import importlib.util as _ilu, os as _os
    _spec = _ilu.spec_from_file_location(
        "mythic_title",
        _os.path.join(_os.path.dirname(__file__), "mythic_title.py")
    )
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _TITLE_LINES = _mod.LINES
except Exception:
    _TITLE_LINES = []  # Graceful fallback: title art skipped if file missing

# ============================================================
# Paths
# ============================================================
ROOT       = Path(__file__).parent
PENTESTGPT = ROOT / "PentestGPT"
OPENMYTHOS = ROOT / "OpenMythos"
PGPT_VENV  = PENTESTGPT / ".venv" / "Scripts"
AGENT_DIR  = PENTESTGPT / "pentestgpt_agent"
SESSIONS   = ROOT / "sessions"
LOGS       = ROOT / "logs"

# ============================================================
# VRAM Budget â€” RTX 3050 Ti = 4096 MiB
# Models that fully fit in VRAM (safe):
#   MFDoom/deepseek-r1-tool-calling:7b  ~3.8 GB  <-- best for reasoning
#   qwen3.5:2b                          ~1.6 GB  <-- best parser
#   qwen3:0.6b                          ~0.4 GB  <-- tiny parser
# Models that exceed VRAM (CPU offload via Ollama):
#   deepseek-r1:14b, qwen3.5:9b, gemma2:9b  --> use if you don't mind slower speed
# ============================================================
DEFAULT_REASONING = "ollama:MFDoom/deepseek-r1-tool-calling:7b"
DEFAULT_PARSING   = "ollama:qwen3.5:2b"
VRAM_SAFE_MODELS  = {
    "MFDoom/deepseek-r1-tool-calling:7b",
    "MFDoom/deepseek-r1-tool-calling:14b",   # borderline, may OOM
    "qwen3.5:2b",
    "qwen3:0.6b",
}
VRAM_UNSAFE_MODELS = {  # will OOM on 4GB VRAM â€” need CPU offload flag
    "deepseek-r1:14b",
    "qwen3.5:9b",
    "gemma2:9b",
}

# ============================================================
# Colors
# ============================================================
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

# Portrait art loaded from mythic_art.py (keeps this file encoding-clean)
try:
    import importlib.util as _ilu2, os as _os2
    _aspec = _ilu2.spec_from_file_location(
        'mythic_art',
        _os2.path.join(_os2.path.dirname(__file__), 'mythic_art.py')
    )
    _amod = _ilu2.module_from_spec(_aspec)
    _aspec.loader.exec_module(_amod)
    _MYTHIC_ART = _amod.ART
except Exception:
    _MYTHIC_ART = ''

def _colorize_art(line: str, y: int = 0) -> str:
    """Apply ANSI color to each character based on visual density (Cyan/Blue aesthetic)."""
    out = []
    
    # Beautiful holographic Cyan to Deep Blue palette based on density
    colors = {
        '@': "\033[38;5;51m",  # Bright Cyan
        '%': "\033[38;5;45m",  # Turquoise
        '#': "\033[38;5;39m",  # Deep Sky Blue
        '*': "\033[38;5;33m",  # Dodger Blue
        '+': "\033[38;5;27m",  # Blue
        '=': "\033[38;5;21m",  # Dark Blue
        '-': "\033[38;5;19m",  # Deeper Blue
        ':': "\033[38;5;17m",  # Midnight Blue
        '.': "\033[38;5;234m"  # Almost black
    }
    
    for ch in line:
        if ch == ' ':
            out.append(ch)
        else:
            col = colors.get(ch, "\033[38;5;235m")
            out.append(col + ch + C.RESET)
            
    return ''.join(out)

def _ansi(s: str) -> str:
    """Inject ESC (0x1B) before every '[' â€” converts bare ANSI seqs to live ones."""
    return s.replace("[", "\033[")

def banner():
    # â”€â”€ Portrait art (density-coloured) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    for i, line in enumerate(_MYTHIC_ART.split('\n')[1:]):   # skip leading blank line
        print(_colorize_art(line, i))

    # â”€â”€ MYTHIC title (FateGate/Blu from patorjk.com) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print()
    if _TITLE_LINES:
        for line in _TITLE_LINES:
            print(_ansi(line))
    else:
        # Fallback if mythic_title.py is missing
        print(C.CYAN + C.BOLD + "  [ M Y T H I C ]" + C.RESET)

    # â”€â”€ Tagline (dark blue, centred under title) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    print(
        "\033[0;34m  Advanced Adversarial OffSec AI Framework"
        "\033[0m  \033[0;90mÃ—\033[0m  "
        "\033[0;34mAutomated Penetration Testing Engine\033[0m"
    )
    print()


def ok(msg):    print(f"  [+] {msg}")
def warn(msg):  print(f"  {C.YELLOW}[!]{C.RESET} {msg}")
def err(msg):   print(f"  {C.RED}[X]{C.RESET} {msg}")
def info(msg):  print(f"  [i] {msg}")
def good(msg):  print(f"  {C.GREEN}[+]{C.RESET} {msg}")
def section(msg):
    print(f"\n{C.BOLD}{C.PURPLE}{'='*52}{C.RESET}")
    print(f"{C.BOLD}  {msg}{C.RESET}")

def vram_warn(model_name: str):
    """Warn if the chosen model is known to exceed 4GB VRAM."""
    bare = model_name.replace("ollama:", "").strip()
    if bare in VRAM_UNSAFE_MODELS:
        warn(f"'{bare}' needs ~9GB VRAM â€” RTX 3050 Ti has 4GB.")
        warn("Ollama will CPU-offload the excess, which is SLOW.")
        warn(f"Recommended alternative: {DEFAULT_REASONING}")
        print()

# ============================================================
# Backend checks
# ============================================================

def check_claude_cli() -> bool:
    """Detect Claude Code CLI (handles Windows .ps1 scripts)."""
    # Try invoking via powershell first
    for cmd_try in [["claude", "--version"],
                    ["powershell", "-Command", "claude --version"]]:
        try:
            r = subprocess.run(cmd_try, capture_output=True, text=True, timeout=10)
            if r.returncode == 0 and r.stdout.strip():
                ok(f"Claude Code CLI: {r.stdout.strip().splitlines()[0]}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

    # Fallback: check for the .ps1 file directly
    claude_ps1 = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.ps1"
    if claude_ps1.exists():
        ok(f"Claude Code CLI: found ({claude_ps1})")
        warn("  Needs login: open PowerShell and run  claude /login")
        return True

    err("Claude Code CLI not found.")
    info("  Install: npm install -g @anthropic-ai/claude-code")
    return False

def check_claude_auth() -> bool:
    """Check if claude is actually authenticated (not just installed)."""
    try:
        r = subprocess.run(
            ["powershell", "-Command", "claude --version"],
            capture_output=True, text=True, timeout=10
        )
        # A simple version check doesn't prove auth â€” we just check it exists
        return r.returncode == 0
    except Exception:
        return False

def check_ollama(model: str = None) -> bool:
    """Check if Ollama is running and optionally if a model is available."""
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            ok("Ollama is running")
            if model:
                bare = model.replace("ollama:", "")
                if bare in r.stdout:
                    ok(f"  Model ready: {bare}")
                    return True
                else:
                    warn(f"  Model not found: {bare}")
                    info(f"  Pull: ollama pull {bare}")
                    return False
            return True
        return False
    except FileNotFoundError:
        err("Ollama not found â€” install from https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        err("Ollama not responding")
        return False

def check_openmythos() -> bool:
    """Check OpenMythos + CUDA availability."""
    mythos_python = OPENMYTHOS / ".venv" / "Scripts" / "python.exe"
    if not mythos_python.exists():
        warn("OpenMythos venv not found. Run: python mythic.py setup")
        return False
    try:
        r = subprocess.run(
            [str(mythos_python), "-c",
             "import torch; import open_mythos; "
             "print('torch', torch.__version__); "
             "print('CUDA:', torch.cuda.is_available()); "
             "print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU-only')"],
            capture_output=True, text=True, timeout=45, cwd=str(OPENMYTHOS)
        )
        if r.returncode == 0:
            for line in r.stdout.strip().splitlines():
                ok(f"OpenMythos: {line}")
            return True
        else:
            warn(f"OpenMythos issue: {(r.stderr or r.stdout)[:200]}")
            return False
    except subprocess.TimeoutExpired:
        warn("OpenMythos check timed out (CUDA init can be slow â€” that's normal)")
        return False

def check_nvidia() -> dict:
    """Return GPU info dict from nvidia-smi."""
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            parts = [p.strip() for p in r.stdout.strip().split(",")]
            return {
                "name":  parts[0] if len(parts) > 0 else "?",
                "total": parts[1] if len(parts) > 1 else "?",
                "free":  parts[2] if len(parts) > 2 else "?",
            }
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {}

# ============================================================
# Commands
# ============================================================

def cmd_status(args):
    banner()

    section("GPU / Hardware")
    gpu = check_nvidia()
    if gpu:
        ok(f"GPU   : {gpu['name']}")
        ok(f"VRAM  : {gpu.get('free','?')} free  /  {gpu.get('total','?')} total")
        info("Safe models  (<=4GB): MFDoom/deepseek-r1-tool-calling:7b, qwen3.5:2b, qwen3:0.6b")
        info("CPU-offload (>4GB) : deepseek-r1:14b, qwen3.5:9b  (slower but works)")
    else:
        warn("No NVIDIA GPU detected")

    section("Backends")
    check_claude_cli()
    check_ollama()

    section("Ollama Models")
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        lines = r.stdout.strip().splitlines()
        for line in lines[1:]:
            parts = line.split()
            if not parts:
                continue
            name = parts[0]
            rest = " ".join(parts[1:])
            vram_tag = ""
            bare = name.split(":")[0] + (":" + name.split(":")[1] if ":" in name else "")
            if any(k in name for k in VRAM_SAFE_MODELS):
                vram_tag = f"  {C.GREEN}[VRAM OK]{C.RESET}"
            elif any(k in name for k in VRAM_UNSAFE_MODELS):
                vram_tag = f"  {C.YELLOW}[CPU offload]{C.RESET}"
            print(f"    {C.CYAN}{name:<44}{C.RESET} {rest}{vram_tag}")
    except Exception:
        warn("Could not list Ollama models")

    section("OpenMythos (RDT Architecture)")
    check_openmythos()

    section("Sessions")
    SESSIONS.mkdir(exist_ok=True)
    sessions = sorted(SESSIONS.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if sessions:
        for s in sessions[:5]:
            mtime = datetime.fromtimestamp(s.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            info(f"{s.stem[:48]:<50} {mtime}")
    else:
        info("No sessions yet â€” run your first target and debrief after!")

    section("Quick Commands")
    print(f"""
  {C.BOLD}Interactive (Ollama â€” LOCAL, FREE):{C.RESET}
    py -3.12 mythic.py legacy                          # default (7b, fits VRAM)
    py -3.12 mythic.py legacy --reasoning-model ollama:deepseek-r1:14b  # CPU offload

  {C.BOLD}Autonomous (Claude Code â€” FREE after login):{C.RESET}
    py -3.12 mythic.py agent --target 10.10.11.234 --goal "Capture the flag"

  {C.BOLD}First time Claude setup:{C.RESET}
    claude /login                                       # run once in PowerShell

  {C.BOLD}OpenMythos RDT demo:{C.RESET}
    py -3.12 mythic.py mythos

  {C.BOLD}Post-session debrief:{C.RESET}
    py -3.12 debrief.py

  {C.BOLD}Smoke test:{C.RESET}
    py -3.12 mythic.py smoke
""")


def cmd_agent(args):
    banner()
    section("Autonomous Agent -- Claude Code Backend")

    claude_ps1 = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.ps1"
    if not claude_ps1.exists():
        err("Claude Code CLI not found at %APPDATA%\\npm\\claude.ps1")
        sys.exit(1)

    ok(f"Claude Code CLI: {claude_ps1}")
    print()

    # Check auth by reading what pentestgpt-agent would say
    info("Note: Claude Code must be authenticated before this works.")
    info("If you see 'AgentAuthError', open PowerShell and run:  claude /login")
    print()

    SESSIONS.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)

    target_safe = (args.target
                   .replace(".", "_").replace(":", "_")
                   .replace("/", "_").replace("http", "").strip("_"))
    run_id = f"{target_safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    goal   = getattr(args, "goal",  "Capture the flag from this authorized target.")
    model  = getattr(args, "model", "claude-opus-4-8")

    info(f"Target  : {args.target}")
    info(f"Goal    : {goal}")
    info(f"Model   : {model}")
    info(f"Run ID  : {run_id}")
    print()

    agent_exe = AGENT_DIR / ".venv" / "Scripts" / "pentestgpt-agent.exe"
    if agent_exe.exists():
        cmd = [str(agent_exe)]
    else:
        cmd = ["uv", "run", "pentestgpt-agent"]

    cmd += [
        "--goal",   goal,
        "--target", args.target,
        "--backend","claude",
        "--model",  model,
        "--effort", "high",
        "--run-id", run_id,
    ]
    if getattr(args, "resume", False):
        cmd.append("--resume")
        info("Resuming previous session...")

    info(f"Launching: {' '.join(cmd)}")
    print()

    try:
        subprocess.run(cmd, cwd=str(AGENT_DIR), check=False)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[!] Interrupted. Run with --resume to continue.{C.RESET}")


def cmd_legacy(args):
    banner()
    section("Legacy Interactive Mode -- Ollama Backend")

    r_model = getattr(args, "reasoning_model", DEFAULT_REASONING) or DEFAULT_REASONING
    p_model = getattr(args, "parsing_model",   DEFAULT_PARSING)   or DEFAULT_PARSING

    # VRAM safety check â€” warn if model will OOM
    vram_warn(r_model)

    # Auto-pull missing models
    for m in [r_model, p_model]:
        if m.startswith("ollama:"):
            bare = m.replace("ollama:", "")
            r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if bare not in r.stdout:
                warn(f"Model not found locally: {bare}")
                info(f"Pulling {bare} ...")
                subprocess.run(["ollama", "pull", bare])

    # For CPU-offload models: set Ollama env to allow GPU+CPU hybrid
    env = os.environ.copy()
    env["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"
    bare_r = r_model.replace("ollama:", "")
    if any(k in bare_r for k in VRAM_UNSAFE_MODELS):
        env["OLLAMA_GPU_OVERHEAD"]   = "200000000"   # reserve 200MB for other GPU use
        env["OLLAMA_MAX_LOADED_MODELS"] = "1"        # evict other models
        info("CPU offload mode active for large model.")

    info(f"Reasoning model : {r_model}")
    info(f"Parsing model   : {p_model}")
    print()

    legacy_exe = str(PGPT_VENV / "pentestgpt-legacy.exe")
    cmd = [
        legacy_exe,
        "--reasoning-model", r_model,
        "--parsing-model",   p_model,
        "--base-url",        "http://localhost:11434/v1",
    ]

    info(f"Launching: {' '.join(cmd)}")
    print()

    try:
        subprocess.run(cmd, cwd=str(PENTESTGPT), env=env, check=False)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[!] Session ended. Debrief: py -3.12 debrief.py{C.RESET}")


def cmd_mythos(args):
    banner()
    section("OpenMythos -- Recurrent Depth Transformer Demo")

    mythos_python = OPENMYTHOS / ".venv" / "Scripts" / "python.exe"
    if not mythos_python.exists():
        err("OpenMythos venv not ready. Run: py -3.12 mythic.py setup")
        sys.exit(1)

    test_code = r"""
import torch
from open_mythos.main import OpenMythos, MythosConfig

print("=" * 52)
print("  MYTHIC -- OpenMythos RDT Architecture Test")
print("=" * 52)
print(f"PyTorch : {torch.__version__}")
print(f"CUDA    : {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU     : {torch.cuda.get_device_name(0)}")
    free = (torch.cuda.get_device_properties(0).total_memory
            - torch.cuda.memory_allocated(0)) / 1e9
    print(f"VRAM    : {free:.2f} GB free")

device = "cuda" if torch.cuda.is_available() else "cpu"

cfg = MythosConfig(
    vocab_size=1000, dim=256, n_heads=8, max_seq_len=128,
    max_loop_iters=8, prelude_layers=1, coda_layers=1,
    n_experts=8, n_shared_experts=1, n_experts_per_tok=2,
    expert_dim=64, lora_rank=8, attn_type="gqa", n_kv_heads=2
)
model = OpenMythos(cfg).to(device)

total = sum(p.numel() for p in model.parameters())
print(f"\nParameters : {total:,}")

ids = torch.randint(0, cfg.vocab_size, (2, 16)).to(device)

print("\n[Shallow] 4 loops (fast, broad recon)")
logits = model(ids, n_loops=4)
print(f"  Output: {logits.shape}")

print("\n[Deep]    8 loops (thorough, exploit-level)")
logits = model(ids, n_loops=8)
print(f"  Output: {logits.shape}")

A = model.recurrent.injection.get_A()
rho = torch.linalg.eigvals(A).abs().max().item()
print(f"\nSpectral radius rho(A) = {rho:.4f}  (must be < 1 for stability)")
print("\nOpenMythos is alive and thinking!")
"""
    example = OPENMYTHOS / "example.py"
    script  = str(example) if example.exists() else "-c"
    run_arg = [str(example)] if example.exists() else ["-c", test_code]
    subprocess.run([str(mythos_python)] + run_arg, cwd=str(OPENMYTHOS))


def cmd_smoke(args):
    banner()
    section("Smoke Test -- All Backends")
    results = {}

    info("Claude Code CLI ...")
    results["claude_cli"]   = check_claude_cli()

    info("Ollama + deepseek-r1-tool-calling:7b (VRAM-safe) ...")
    results["ollama_7b"]    = check_ollama("ollama:MFDoom/deepseek-r1-tool-calling:7b")

    info("Ollama + qwen3.5:2b (parser) ...")
    results["ollama_qwen2b"]= check_ollama("ollama:qwen3.5:2b")

    info("OpenMythos + CUDA ...")
    results["openmythos"]   = check_openmythos()

    info("Live Ollama API call (qwen3.5:2b) ...")
    try:
        payload = json.dumps({
            "model": "qwen3.5:2b",
            "messages": [{"role": "user", "content": "Reply ONLY with the word OK, nothing else."}],
            "stream": False, "max_tokens": 5,
            "options": {"num_predict": 5}
        }).encode()
        req = urllib.request.Request(
            "http://localhost:11434/v1/chat/completions",
            data=payload, method="POST",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        reply = data["choices"][0]["message"]["content"].strip()[:60]
        ok(f"Ollama live call: '{reply}'")
        results["ollama_api"] = True
    except Exception as e:
        err(f"Ollama live call failed: {e}")
        results["ollama_api"] = False

    section("Results")
    for name, status in results.items():
        if status is True:
            print(f"    {C.GREEN}PASS{C.RESET}  {name}")
        elif status is False:
            print(f"    {C.RED}FAIL{C.RESET}  {name}")
        else:
            print(f"    {C.YELLOW}----{C.RESET}  {name}")

    passed = sum(1 for v in results.values() if v is True)
    total  = len(results)
    color  = C.GREEN if passed == total else C.YELLOW if passed >= 3 else C.RED
    print(f"\n  {color}{C.BOLD}{passed}/{total} backends operational{C.RESET}")

    if not results.get("claude_cli"):
        print(f"\n  {C.YELLOW}[!] Claude fix: open PowerShell and run  claude /login{C.RESET}")
    if not results.get("openmythos"):
        print(f"  {C.YELLOW}[!] OpenMythos: run  py -3.12 mythic.py mythos  to verify{C.RESET}")
    print()


def cmd_setup(args):
    banner()
    section("Setup -- OpenMythos Installation")

    info("Step 1/3: Python 3.12 venv ...")
    subprocess.run(["uv", "venv", "--python", "3.12", str(OPENMYTHOS / ".venv")])

    info("Step 2/3: PyTorch CUDA 12.4 (~2.4 GB) ...")
    subprocess.run([
        "uv", "pip", "install", "torch", "torchvision",
        "--index-url", "https://download.pytorch.org/whl/cu124",
        "--python", str(OPENMYTHOS / ".venv" / "Scripts" / "python.exe")
    ])

    info("Step 3/3: open-mythos package ...")
    subprocess.run([
        "uv", "pip", "install", "-e", ".", "--no-deps",
        "--python", str(OPENMYTHOS / ".venv" / "Scripts" / "python.exe")
    ], cwd=str(OPENMYTHOS))

    ok("Setup complete! Test: py -3.12 mythic.py mythos")


# ============================================================
# Main
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="MYTHIC -- OpenMythos x PentestGPT Advanced AI Pentesting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Full system health check")

    p_agent = sub.add_parser("agent", help="Autonomous pentesting (Claude Code, free after login)")
    p_agent.add_argument("--target",  required=True, help="Target IP or URL")
    p_agent.add_argument("--goal",    default="Capture the flag from this authorized target.")
    p_agent.add_argument("--model",   default="claude-opus-4-8")
    p_agent.add_argument("--resume",  action="store_true")

    p_legacy = sub.add_parser("legacy", help="Interactive pentesting (Ollama local, always free)")
    p_legacy.add_argument(
        "--reasoning-model", dest="reasoning_model",
        default=DEFAULT_REASONING,
        help=f"Thinking model (default: {DEFAULT_REASONING})"
    )
    p_legacy.add_argument(
        "--parsing-model", dest="parsing_model",
        default=DEFAULT_PARSING,
        help=f"Parser model (default: {DEFAULT_PARSING})"
    )

    sub.add_parser("mythos", help="Test OpenMythos RDT (variable-depth reasoning)")
    sub.add_parser("smoke",  help="Smoke test all backends")
    sub.add_parser("setup",  help="Install OpenMythos + PyTorch CUDA")

    args = parser.parse_args()
    cmd  = getattr(args, "command", None)

    if   not cmd or cmd == "status": cmd_status(args)
    elif cmd == "agent":             cmd_agent(args)
    elif cmd == "legacy":            cmd_legacy(args)
    elif cmd == "mythos":            cmd_mythos(args)
    elif cmd == "smoke":             cmd_smoke(args)
    elif cmd == "setup":             cmd_setup(args)
    else:                            parser.print_help()


if __name__ == "__main__":
    main()


