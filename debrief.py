#!/usr/bin/env python3
"""
MYTHIC Session Logger — Post-run debrief and lesson tracker.

After every CTF/pentest run, use this to:
  - Record what worked, what failed, key findings
  - Store lessons that get recalled for similar targets next time
  - Build your personal knowledge base over time

Usage:
  python debrief.py                        # Interactive debrief wizard
  python debrief.py --list                 # List all past sessions
  python debrief.py --lessons              # Show all lessons learned
  python debrief.py --search "SSRF"        # Search lessons by keyword
  python debrief.py --show <session-id>    # Show a specific session
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

ROOT     = Path(__file__).parent
SESSIONS = ROOT / "sessions"
LESSONS  = ROOT / "lessons.jsonl"

SESSIONS.mkdir(exist_ok=True)

# ── ANSI colors ───────────────────────────────────────────────────────────────
class C:
    R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"
    P="\033[95m"; CY="\033[96m"; BOLD="\033[1m"; DIM="\033[2m"; X="\033[0m"

def section(t): print(f"\n{C.BOLD}{C.P}{'─'*50}{C.X}\n{C.BOLD}  {t}{C.X}")
def q(prompt): return input(f"\n{C.CY}  ▶ {C.X}{C.BOLD}{prompt}{C.X}\n    > ").strip()
def ok(m): print(f"  {C.G}✓{C.X} {m}")
def info(m): print(f"  {C.B}ℹ{C.X} {m}")

# ── Debrief wizard ─────────────────────────────────────────────────────────────
DIFFICULTY_MAP = {"1":"Easy","2":"Medium","3":"Hard","4":"Insane","5":"Expert"}
OUTCOME_MAP    = {"1":"Solved","2":"Partial","3":"Stuck","4":"Abandoned"}

def run_debrief():
    print(f"""
{C.CY}{C.BOLD}
  +----------------------------------------------+
  |   MYTHIC  --  Post-Run Debrief Wizard        |
  |   Advanced Adversarial OffSec AI Framework   |
  +----------------------------------------------+
{C.X}{C.DIM}  Take 5 minutes. Future-you will thank present-you.{C.X}
""")

    session = {}

    # ── Basic info ────────────────────────────────────────────────────────────
    section("Target Info")
    session["timestamp"]   = datetime.now().isoformat()
    session["target"]      = q("Target name/IP (e.g. 'HTB: BoardLight 10.10.11.1')")
    session["target_type"] = q("Type? [1=HTB, 2=THM, 3=VulnHub, 4=Real pentest, 5=CTF comp]")
    session["category"]    = q("Category? [web / binary / network / crypto / forensics / mixed]")
    session["difficulty"]  = q("Difficulty? [1=Easy, 2=Med, 3=Hard, 4=Insane, 5=Expert]")
    session["model_used"]  = q("Model used? (e.g. 'claude-code / ollama:deepseek-r1:14b')")
    session["outcome"]     = q("Outcome? [1=Solved, 2=Partial, 3=Stuck, 4=Abandoned]")
    session["duration"]    = q("Time spent (e.g. '2h30m')")

    # ── Story ────────────────────────────────────────────────────────────────
    section("What Happened")
    session["summary"] = q(
        "Brief summary — what was the target, what did you find, what was the path?"
    )
    session["what_worked"] = q(
        "What worked? (tools, techniques, approaches that were effective)"
    )
    session["what_failed"] = q(
        "What failed or wasted time? (dead ends, wrong assumptions)"
    )
    session["surprise"] = q(
        "Biggest surprise or 'aha moment'? (can be empty)"
    )

    # ── Lessons ──────────────────────────────────────────────────────────────
    section("Lessons Learned")
    print(f"  {C.DIM}Enter lessons one per line. Empty line to finish.{C.X}")
    print(f"  {C.DIM}Good format: '[technique/tool]: what I learned about it'{C.X}\n")

    lessons = []
    while True:
        lesson = input("    + ").strip()
        if not lesson:
            break
        tags_raw = input(f"      {C.DIM}Tags for this lesson (space-separated, e.g. 'web ssrf nmap):{C.X} ").strip()
        lessons.append({
            "text":    lesson,
            "tags":    tags_raw.lower().split() if tags_raw else [],
            "target":  session["target"],
            "date":    session["timestamp"][:10],
        })

    session["lessons"] = lessons

    # ── AI quality ───────────────────────────────────────────────────────────
    section("AI Performance")
    session["ai_helpful"]  = q("Was the AI helpful? [1-5 stars, or 'n/a']")
    session["ai_feedback"] = q(
        "Any notes on AI behavior? (what it did well / poorly / hallucinated)"
    )

    # ── Next steps ───────────────────────────────────────────────────────────
    section("Next Steps")
    session["next_steps"] = q(
        "If you continue this or a similar target, what would you try next?"
    )
    session["roadmap_update"] = q(
        "Should the MYTHIC roadmap change because of this session? (optional note)"
    )

    # ── Save ─────────────────────────────────────────────────────────────────
    session_id = f"{session['timestamp'][:16].replace(':', '-').replace('T', '_')}_{session['target'][:20].replace(' ', '_').replace('/', '_')}"
    session["id"] = session_id

    # Map user codes to labels
    session["difficulty"] = DIFFICULTY_MAP.get(session["difficulty"], session["difficulty"])
    session["outcome"]    = OUTCOME_MAP.get(session["outcome"],    session["outcome"])

    # Save full session
    out_path = SESSIONS / f"{session_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2, ensure_ascii=False)

    # Append lessons to global lessons log
    if lessons:
        with open(LESSONS, "a", encoding="utf-8") as f:
            for lesson in lessons:
                f.write(json.dumps(lesson, ensure_ascii=False) + "\n")

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"""
{C.G}{C.BOLD}  ✓ Debrief saved!{C.X}
  {C.DIM}Session: {out_path}{C.X}
  {C.DIM}Lessons added to global log: {len(lessons)}{C.X}
""")

    if lessons:
        print(f"  {C.BOLD}Lessons recorded:{C.X}")
        for i, l in enumerate(lessons, 1):
            tags = f" [{' '.join(l['tags'])}]" if l["tags"] else ""
            print(f"  {i}. {l['text']}{C.DIM}{tags}{C.X}")

    if session.get("roadmap_update"):
        print(f"\n  {C.Y}⚠  Roadmap note: {session['roadmap_update']}{C.X}")
        print(f"  {C.DIM}Remember to update the MYTHIC implementation_plan.md with this insight.{C.X}")

    print()


# ── List sessions ─────────────────────────────────────────────────────────────
def list_sessions():
    sessions = sorted(SESSIONS.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not sessions:
        info("No sessions yet. Run a debrief first!")
        return

    section(f"Sessions ({len(sessions)} total)")
    print(f"  {'ID':<45} {'Target':<20} {'Outcome':<10} {'Diff'}")
    print(f"  {'─'*45} {'─'*20} {'─'*10} {'─'*8}")

    for s in sessions:
        try:
            data = json.loads(s.read_text(encoding="utf-8"))
            sid     = data.get("id", s.stem)[:44]
            target  = data.get("target", "?")[:19]
            outcome = data.get("outcome", "?")[:9]
            diff    = data.get("difficulty", "?")[:8]
            col = C.G if outcome=="Solved" else C.Y if outcome=="Partial" else C.R
            print(f"  {sid:<45} {target:<20} {col}{outcome:<10}{C.X} {diff}")
        except Exception:
            print(f"  {s.stem} (unreadable)")


# ── Show one session ──────────────────────────────────────────────────────────
def show_session(session_id: str):
    matches = list(SESSIONS.glob(f"*{session_id}*.json"))
    if not matches:
        print(f"No session matching '{session_id}'")
        return

    data = json.loads(matches[0].read_text(encoding="utf-8"))
    section(f"Session: {data.get('target', '?')}")
    for key, val in data.items():
        if key == "lessons":
            continue
        print(f"  {C.BOLD}{key:<18}{C.X} {val}")

    if data.get("lessons"):
        section("Lessons")
        for i, l in enumerate(data["lessons"], 1):
            tags = f"  {C.DIM}[{' '.join(l['tags'])}]{C.X}" if l.get("tags") else ""
            print(f"  {i}. {l['text']}{tags}")


# ── List all lessons ──────────────────────────────────────────────────────────
def list_lessons(search: str = None):
    if not LESSONS.exists():
        info("No lessons recorded yet.")
        return

    all_lessons = []
    with open(LESSONS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    all_lessons.append(json.loads(line))
                except Exception:
                    pass

    if search:
        search_lower = search.lower()
        all_lessons = [
            l for l in all_lessons
            if search_lower in l.get("text","").lower()
            or search_lower in " ".join(l.get("tags",[])).lower()
        ]
        section(f"Lessons matching '{search}' ({len(all_lessons)} found)")
    else:
        section(f"All Lessons ({len(all_lessons)} total)")

    if not all_lessons:
        info("No matching lessons.")
        return

    for i, l in enumerate(all_lessons, 1):
        tags = f"  {C.DIM}[{' '.join(l['tags'])}]{C.X}" if l.get("tags") else ""
        date = l.get("date","")
        tgt  = l.get("target","")
        src  = f"  {C.DIM}← {tgt} ({date}){C.X}" if (tgt or date) else ""
        print(f"\n  {C.CY}{i}.{C.X} {l['text']}{tags}{src}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="MYTHIC Session Debrief & Lesson Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--list",    action="store_true", help="List all past sessions")
    parser.add_argument("--lessons", action="store_true", help="Show all lessons learned")
    parser.add_argument("--search",  type=str,            help="Search lessons by keyword")
    parser.add_argument("--show",    type=str,            help="Show a specific session by partial ID")

    args = parser.parse_args()

    if args.list:
        list_sessions()
    elif args.lessons:
        list_lessons()
    elif args.search:
        list_lessons(args.search)
    elif args.show:
        show_session(args.show)
    else:
        run_debrief()


if __name__ == "__main__":
    main()
