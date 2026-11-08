#!/usr/bin/env python3
"""
Hermes Visual Agent Desk & Modern Campus — Dual-Stack Bridge Server
-------------------------------------------------------------------
Provides state folding, worksheets sync, agent life-cycle simulation,
and Hermes event-sourcing API.

Features:
- Dual-Stack IPv6 / IPv4 listener (localhost & 127.0.0.1 without connection refused)
- Hermes Worksheets Sync & Switcher (Pembahasan A, B, C...)
- Dynamic Agent Life: Walking, Sitting on Park Benches, Working at Desks, Group Meetings
- Micro & Macro Interactivity API
- Zero external dependencies: Python 3 standard library only
"""

import os
import sys
import json
import time
import re
import random
import socket
import sqlite3
import threading
from datetime import datetime
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTIFACTS_DIR = os.path.join(DATA_DIR, "artifacts")
EVENTS_FILE = os.path.join(DATA_DIR, "events.jsonl")
WORKSHEETS_FILE = os.path.join(DATA_DIR, "worksheets.json")
_MAX_LOG_BYTES = 512 * 1024
_STALE_SECONDS = 30 * 60

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

_lock = threading.Lock()
_demo_running = True
_demo_thread = None
_agent_overrides = {}
_active_worksheet_id = "ws-topic-a"
_in_memory_agents = {}
_hermes_memory_chat = {}

HERMES_STATE_DB = os.path.expanduser('~\\AppData\\Local\\hermes\\state.db')

def get_hermes_sessions():
    """Retrieve real Hermes sessions from AppData/Local/hermes/state.db."""
    if os.path.exists(HERMES_STATE_DB):
        try:
            conn = sqlite3.connect(f"file:{HERMES_STATE_DB}?mode=ro", uri=True)
            cur = conn.cursor()
            rows = cur.execute("""
                SELECT id, title, started_at, last_activity_at, pinned 
                FROM sessions 
                ORDER BY pinned DESC, last_activity_at DESC 
                LIMIT 20
            """).fetchall()
            conn.close()
            sessions = []
            for r in rows:
                sid, title, started, last_act, pinned = r
                sessions.append({
                    "id": sid,
                    "title": title or f"Session {sid[:12]}",
                    "started_at": started,
                    "last_activity_at": last_act,
                    "pinned": bool(pinned)
                })
            if sessions:
                return sessions
        except Exception as e:
            print(f"[!] Error reading hermes state.db: {e}")

    return [
        {"id": "local-27e0a60c312fe97402f76d3316ad6ee047a451d83a24e4b02df4919458f611e8", "title": "Buat ONAL Universal Memory Bridge", "pinned": True, "last_activity_at": time.time() - 3600*19},
        {"id": "local-d88d47d76f7775a808ef671244ea73631e9554801dd17fa85dd86c688d172234", "title": "CHARISNA SuperApp", "pinned": False, "last_activity_at": time.time() - 3600*24},
        {"id": "sess-zennai-lab", "title": "zennAI Intelligence Architecture", "pinned": False, "last_activity_at": time.time() - 3600*48},
        {"id": "sess-star-office", "title": "Star Office World Cockpit", "pinned": False, "last_activity_at": time.time() - 3600*72}
    ]

def get_hermes_messages(session_id):
    """Retrieve real messages for a session from hermes state.db and in-memory chat."""
    msgs = []
    if os.path.exists(HERMES_STATE_DB) and session_id:
        try:
            conn = sqlite3.connect(f"file:{HERMES_STATE_DB}?mode=ro", uri=True)
            cur = conn.cursor()
            rows = cur.execute("""
                SELECT id, role, content, tool_name, reasoning, timestamp 
                FROM messages 
                WHERE session_id = ? 
                ORDER BY id ASC 
                LIMIT 40
            """, (session_id,)).fetchall()
            conn.close()
            for r in rows:
                mid, role, content, tool, reasoning, ts = r
                if content or tool or reasoning:
                    msgs.append({
                        "id": mid,
                        "role": role,
                        "content": content or "",
                        "tool_name": tool,
                        "reasoning": reasoning,
                        "timestamp": ts
                    })
        except Exception as e:
            print(f"[!] Error reading hermes messages: {e}")

    # Append any dynamic messages sent in current session
    if session_id in _hermes_memory_chat:
        msgs.extend(_hermes_memory_chat[session_id])

    if not msgs:
        msgs = [
            {
                "id": 1,
                "role": "user",
                "content": "Halo Hermes, tolong laporkan status arsitektur CHARISNA SuperApp dan integrasi Star Office.",
                "timestamp": time.time() - 120
            },
            {
                "id": 2,
                "role": "assistant",
                "reasoning": "Mengecek status dual-stack bridge dan multi-business databases...",
                "tool_name": "inspect_system_health",
                "content": "Siap! Seluruh sistem beroperasi optimal:\n- **Star Office World**: Aktif di `http://localhost:8765`.\n- **Bumi Makmur POS**: Source of truth transaksi dan stok barang.\n- **CHARISNA Homestay**: Source of truth unit kamar & penyewa.\n- **Money Management**: Laporan pembukuan keluarga terdata dengan provenance penuh.",
                "timestamp": time.time() - 60
            }
        ]
    return msgs

AGENT_ID_MAP = {
    "hermes": "sess-hermes-prime",
    "athena": "sess-athena-core",
    "hephaestus": "sess-hephaestus",
    "iris": "sess-iris-ui",
    "zephyr": "sess-zephyr",
}

AGENT_PROFILES = {
    "sess-hermes-prime": {
        "id": "sess-hermes-prime",
        "label": "Hermes Prime",
        "codename": "HERMES-01",
        "role": "Lead Architect & Orchestrator",
        "model": "Hermes-3-70B / Claude-3.5-Sonnet",
        "level": 5,
        "xp": 840,
        "max_xp": 1000,
        "avatar_idx": 0,
        "desk_idx": 0,
        "bench_idx": 0,
        "platform": "hermes",
        "status": "working",
        "behavior": "desk",
        "activity": "typing",
        "detail": "Mengorkestrasi sistem hybrid storage & visual workspace"
    },
    "sess-athena-core": {
        "id": "sess-athena-core",
        "label": "Athena Owl",
        "codename": "ATHENA-02",
        "role": "Knowledge & Intelligence Specialist",
        "model": "Gemini-1.5-Pro / GPT-4o",
        "level": 4,
        "xp": 620,
        "max_xp": 800,
        "avatar_idx": 1,
        "desk_idx": 1,
        "bench_idx": 1,
        "platform": "athena",
        "status": "working",
        "behavior": "desk",
        "activity": "reading",
        "detail": "Menelusuri indeks semantik FTS5 & review queue"
    },
    "sess-hephaestus": {
        "id": "sess-hephaestus",
        "label": "Hephaestus Forge",
        "codename": "FORGE-03",
        "role": "DevOps & Infrastructure Engineer",
        "model": "DeepSeek-Coder-V2 / Claude-3.5-Sonnet",
        "level": 4,
        "xp": 530,
        "max_xp": 800,
        "avatar_idx": 2,
        "desk_idx": 2,
        "bench_idx": 0,
        "platform": "forge",
        "status": "idle",
        "behavior": "bench",
        "activity": "resting",
        "detail": "Santai di bangku taman menikmati sakura 🌸"
    },
    "sess-iris-ui": {
        "id": "sess-iris-ui",
        "label": "Iris Prism",
        "codename": "PRISM-04",
        "role": "UI/UX & Creative Synthesizer",
        "model": "Claude-3.5-Sonnet / Gemini-Flash",
        "level": 3,
        "xp": 410,
        "max_xp": 600,
        "avatar_idx": 3,
        "desk_idx": 3,
        "bench_idx": 1,
        "platform": "prism",
        "status": "working",
        "behavior": "desk",
        "activity": "typing",
        "detail": "Mendesain tilemap Pixel Office & 2D canvas controls"
    },
    "sess-zephyr": {
        "id": "sess-zephyr",
        "label": "Zephyr Runner",
        "codename": "ZEPHYR-05",
        "role": "Telemetry & Performance Profiler",
        "model": "Mistral-Large-2 / Qwen-2.5",
        "level": 3,
        "xp": 310,
        "max_xp": 600,
        "avatar_idx": 4,
        "desk_idx": 4,
        "bench_idx": 1,
        "platform": "zephyr",
        "status": "idle",
        "behavior": "drinking",
        "activity": "resting",
        "detail": "Menyeduh matcha hangat di break room 🍵"
    }
}

DEFAULT_WORKSHEETS = [
    {
        "id": "ws-topic-a",
        "code": "A",
        "title": "CHARISNA Intelligence System & Holographic Memory",
        "category": "Architecture & Long-Term Memory",
        "status": "active",
        "assigned": ["hermes", "athena"],
        "goal": "Implementasi hybrid storage: aktif = lokal (AppData/Local/hermes), arsip = Drive I:/My Drive/Charisna SuperApp. Holographic memory SQLite FTS5.",
        "deliverable": """# Lembar Kerja A: CHARISNA Intelligence System & Long-Term Memory
**Status**: Sedang Berlangsung (Hermes Prime & Athena Owl)
**Arsip**: `Reports/2026-11-08-intelligence-system-implementation.md`

## 1. Komponen Utama
- **Hybrid Storage**: Aktif lokal di `AppData/Local/hermes`, sinkronisasi keputusan ke Google Drive.
- **Holographic Provider**: SQLite FTS5 incremental indexing (`charisna_indexer.py`).
- **Seed Pengetahuan**: DEC-0001 (decoupled multi-business: Bumi Makmur POS, Homestay, MoniFlow).

## 2. Status Agen
- `hermes`: Mengorkestrasi event stream & verifikasi postconditions.
- `athena`: Menelusuri indeks semantik FTS5 & review queue.""",
        "created_at": "2026-11-08T06:00:00",
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "ws-topic-b",
        "code": "B",
        "title": "CHARISNA AI Office Installation & Multi-Business Hub",
        "category": "Infrastructure & Deployment",
        "status": "ready",
        "assigned": ["hephaestus"],
        "goal": "Integrasi CLI Hermes lokal (hermes.exe), kanban sync, dual-stack HTTP bridge (anti-crash), dan desktop UI.",
        "deliverable": """# Lembar Kerja B: AI Office Installation & Local Bridge
**Status**: Siap Ditinjau (Hephaestus Forge)
**Catatan**: `Reports/2026-11-08-charisna-ai-office-installation.md`

## 1. Spesifikasi Teknis
- Port: `http://localhost:8765` & `http://127.0.0.1:8765` (Dual-Stack IPv6/IPv4).
- CLI Hermes: `AppData/Local/hermes/bin/hermes.exe` (`hermes kanban list --json`).
- Zero-crash threading model dengan daemon threads.

## 2. Status Agen
- `hephaestus`: Sandboxing & build tool verification.""",
        "created_at": "2026-11-08T07:15:00",
        "updated_at": datetime.now().isoformat()
    },
    {
        "id": "ws-topic-c",
        "code": "C",
        "title": "Modern Smooth 3D Campus & Interactive Visualizer",
        "category": "UI / UX Redesign",
        "status": "active",
        "assigned": ["iris", "hermes"],
        "goal": "Rombak total desain kuno/kotak-kotak menjadi smooth 3D campus, bangku taman interaktif, zoom in/out 2D, dan worksheet switcher.",
        "deliverable": """# Lembar Kerja C: Modern Smooth Visual Campus & Dynamic Life
**Status**: Sprint Aktif (Iris Prism & Hermes Core)

## 1. Poin Transformasi Desain
- **Buang Voxel Kotak-kotak**: Ganti dengan smooth 3D geometry (rounded terrain, stylized trees, curved benches, floating glass OLED displays).
- **Bangku Taman Interaktif**: Agen santai dan duduk di bangku taman saat idle/break, dan hanya kembali ke meja kerja saat ada tugas aktif.
- **Kontrol 2D Pan & Zoom**: Kanvas 2D kini mendukung zoom in/out halus (mouse wheel) dan drag geser bebas.
- **Sinkronisasi Lembar Kerja**: Pindah fokus kerja antar pembahasan A, B, dan C dengan 1 klik.""",
        "created_at": "2026-11-08T08:00:00",
        "updated_at": datetime.now().isoformat()
    }
]

def load_worksheets():
    if not os.path.exists(WORKSHEETS_FILE):
        save_worksheets(DEFAULT_WORKSHEETS)
        return DEFAULT_WORKSHEETS
    try:
        with open(WORKSHEETS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data
            return DEFAULT_WORKSHEETS
    except Exception:
        return DEFAULT_WORKSHEETS

def save_worksheets(data):
    try:
        with open(WORKSHEETS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[!] Error saving worksheets: {e}")

class DualStackThreadingHTTPServer(ThreadingHTTPServer):
    """Multi-threaded HTTP Server supporting both IPv4 (127.0.0.1) and IPv6 (::1/localhost)."""
    address_family = socket.AF_INET6
    daemon_threads = True
    allow_reuse_address = True

    def server_bind(self):
        try:
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except Exception:
            pass
        return super().server_bind()

def _short(text, n=60):
    s = str(text or "").strip().replace("\n", " ")
    return s[: n - 1] + "…" if len(s) > n else s

def _process_event_into_state(ev: dict):
    now = time.time()
    kind = ev.get("event")
    key = ev.get("session_id") or ev.get("child_session_id") or f"pid-{ev.get('pid', 'core')}"

    a = _in_memory_agents.get(key)
    if a is None:
        if key in AGENT_PROFILES:
            a = dict(AGENT_PROFILES[key])
        else:
            a = {
                "id": key,
                "label": f"agent {key[-6:]}",
                "codename": f"AGT-{key[-4:]}",
                "role": "Autonomous Worker",
                "model": "Hermes-3-70B",
                "level": 1,
                "xp": 50,
                "max_xp": 200,
                "avatar_idx": len(_in_memory_agents) % 5,
                "kind": "main",
                "status": "idle",
                "tool": "",
                "activity": "resting",
                "detail": "",
                "behavior": "bench",  # desk, bench, walking, drinking, meeting
                "platform": ev.get("platform") or "hermes",
                "first_seen": ev.get("ts", now),
                "updated_at": ev.get("ts", now),
            }
        _in_memory_agents[key] = a
    a["updated_at"] = ev.get("ts", now)

    if kind == "session_start":
        a["status"] = "idle"
        a["behavior"] = "bench"
        plat = ev.get("platform") or ""
        if key not in AGENT_PROFILES:
            a["label"] = f"{plat or 'hermes'} {key[-6:]}"
        a["detail"] = "Online di Pixel Office"
    elif kind == "session_end":
        a["status"] = "gone"
        a["behavior"] = "walking"
    elif kind == "subagent_start":
        child = ev.get("child_session_id")
        if child:
            ck = str(child)
            sub = _in_memory_agents.get(ck)
            if not sub:
                sub = {
                    "id": ck,
                    "kind": "subagent",
                    "role": "Specialized Subagent Task",
                    "model": "Hermes-Subagent",
                    "level": 1,
                    "xp": 20,
                    "max_xp": 100,
                    "avatar_idx": (len(_in_memory_agents) + 1) % 5,
                    "first_seen": ev.get("ts", now),
                }
                _in_memory_agents[ck] = sub
            sub["label"] = _short(ev.get("child_goal"), 26) or f"sub {ck[-6:]}"
            sub["status"] = "working"
            sub["behavior"] = "desk"
            sub["detail"] = _short(ev.get("child_goal"))
            sub["parent"] = str(ev.get("parent_session_id") or "")
            sub["updated_at"] = ev.get("ts", now)
    elif kind == "subagent_stop":
        child = ev.get("child_session_id")
        if child and str(child) in _in_memory_agents:
            _in_memory_agents[str(child)]["status"] = "done"
            _in_memory_agents[str(child)]["behavior"] = "bench"
            _in_memory_agents[str(child)]["updated_at"] = ev.get("ts", now)
    elif kind == "tool_start":
        a["status"] = "working"
        a["behavior"] = "desk"
        tool = str(ev.get("tool_name") or "")
        a["tool"] = tool
        act = ev.get("activity")
        if not act:
            if tool in ("write_file", "patch", "edit_file"):
                act = "typing"
            elif tool in ("read_file", "search_files", "grep"):
                act = "reading"
            elif tool in ("web_search", "browser", "fetch"):
                act = "browsing"
            elif tool in ("terminal", "run_command", "bash"):
                act = "running"
            elif tool in ("delegate_task", "invoke_subagent"):
                act = "delegating"
            else:
                act = "working"
        a["activity"] = act
        a["detail"] = _short(ev.get("preview") or ev.get("args") or tool)
    elif kind == "tool_end":
        a["status"] = "thinking"
        a["tool"] = ""
        if ev.get("status") != "error":
            gained = random.randint(25, 45)
            a["xp"] = a.get("xp", 0) + gained
            max_xp = a.get("max_xp", 200)
            if a["xp"] >= max_xp:
                a["level"] = a.get("level", 1) + 1
                a["xp"] -= max_xp
                a["max_xp"] = a["level"] * 200
                a["detail"] = f"🌟 LEVEL UP! Rank {a['level']}"
            else:
                a["detail"] = f"+{gained} XP selesai eksekusi"
        else:
            a["detail"] = f"⚠ {_short(ev.get('error_message'), 40)}"
    elif kind == "approval_request":
        a["status"] = "waiting"
        a["behavior"] = "desk"
        a["tool"] = ""
        a["detail"] = _short(ev.get("command"), 40) or "needs approval"
    elif kind == "approval_response":
        choice = str(ev.get("choice") or "")
        if choice in ("deny", "timeout"):
            a["status"] = "thinking"
            a["detail"] = f"approval: {choice}"
        else:
            a["status"] = "working"
            a["detail"] = ""
    elif kind == "agent_behavior":
        a["behavior"] = ev.get("behavior", "bench")
        a["activity"] = ev.get("activity", a.get("activity", "resting"))
        if ev.get("detail"):
            a["detail"] = ev.get("detail")

def publish_event(event: dict) -> None:
    try:
        event.setdefault("ts", time.time())
        event.setdefault("pid", os.getpid())
        with _lock:
            _process_event_into_state(event)
        try:
            line = json.dumps(event, ensure_ascii=False, default=str)
            with open(EVENTS_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    except Exception as e:
        print(f"[!] Error publishing event: {e}")

def maybe_trim_events() -> None:
    try:
        if not os.path.exists(EVENTS_FILE) or os.path.getsize(EVENTS_FILE) <= _MAX_LOG_BYTES:
            return
        with open(EVENTS_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
        keep = lines[len(lines) // 2:]
        tmp = EVENTS_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(keep) + "\n")
        os.replace(tmp, EVENTS_FILE)
    except Exception as e:
        print(f"[!] Error trimming events: {e}")

def init_in_memory_state():
    """Seed agents from AGENT_PROFILES and warm up with recent events."""
    now = time.time()
    for sid, prof in AGENT_PROFILES.items():
        _in_memory_agents[sid] = dict(prof)
        _in_memory_agents[sid]["first_seen"] = now
        _in_memory_agents[sid]["updated_at"] = now
    
    if not os.path.exists(EVENTS_FILE):
        return
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        for line in lines[-200:]:
            line = line.strip()
            if line:
                try:
                    ev = json.loads(line)
                    _process_event_into_state(ev)
                except Exception:
                    continue
    except Exception as e:
        print(f"[!] Error warming state cache: {e}")

def build_office_state() -> dict:
    """Return live in-memory agent snapshots with zero disk read overhead."""
    now = time.time()
    with _lock:
        agents = {k: dict(v) for k, v in _in_memory_agents.items()}

    # Apply manual micro-overrides
    for aid, override in _agent_overrides.items():
        if aid in agents:
            agents[aid].update(override)

    visible = []
    for a in agents.values():
        if a.get("id") == "sess-iris":
            continue
        age = now - float(a.get("updated_at") or 0)
        if a["status"] == "gone" and age > 25:
            continue
        if a["status"] == "done" and age > 90:
            continue
        if age > _STALE_SECONDS:
            continue
        visible.append(a)

    visible.sort(key=lambda a: (a.get("kind") != "main", a.get("first_seen", 0)))
    return {"agents": visible, "ts": now, "active_worksheet": _active_worksheet_id}


# ---------------------------------------------------------------------------
# Autonomous Life & Demo Simulation Worker
# ---------------------------------------------------------------------------
DEMO_TOOLS = [
    ("terminal", "running", {"command": "npm test"}),
    ("read_file", "reading", {"path": "src/core/hermes.ts"}),
    ("web_search", "browsing", {"query": "deep learning agent optimization"}),
    ("write_file", "typing", {"path": "src/agents/orchestrator.py"}),
    ("search_files", "reading", {"pattern": "def execute_task"}),
    ("delegate_task", "delegating", {"task": "Audit security & memory"}),
]

def demo_worker():
    global _demo_running
    sids = ["sess-hermes-prime", "sess-athena-core", "sess-hephaestus", "sess-iris-ui", "sess-zephyr"]
    for sid in sids:
        publish_event({"event": "session_start", "session_id": sid, "platform": AGENT_PROFILES.get(sid, {}).get("platform", "hermes")})

    while _demo_running:
        for sid in sids:
            if not _demo_running:
                break
            
            rnd = random.random()
            if rnd < 0.40:
                # Rest on Park Bench or Coffee Lounge
                behavior = random.choice(["bench", "drinking", "walking"])
                if behavior == "bench":
                    detail = "Duduk santai di bangku taman dekat bunga sakura 🌸"
                elif behavior == "drinking":
                    detail = "Menikmati seduhan kopi di break room ☕"
                else:
                    detail = "Jalan-jalan santai melihat panorama kota 🚶"
                publish_event({"event": "agent_behavior", "session_id": sid, "behavior": behavior, "activity": "resting", "detail": detail})
                time.sleep(random.uniform(5.0, 9.0))
            else:
                # Work at desk
                tool, act, args = random.choice(DEMO_TOOLS)
                publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "desk", "activity": act, "detail": f"Workstation: {tool}"})
                publish_event({"event": "tool_start", "session_id": sid, "tool_name": tool, "activity": act, "preview": str(args)})
                time.sleep(random.uniform(5.0, 9.0))
                publish_event({"event": "tool_end", "session_id": sid, "tool_name": tool, "status": "ok"})

        time.sleep(3.0)

def toggle_demo_mode():
    global _demo_running, _demo_thread
    _demo_running = not _demo_running
    if _demo_running:
        _demo_thread = threading.Thread(target=demo_worker, daemon=True)
        _demo_thread.start()
    return _demo_running

# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------
class DeskBridgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def address_string(self):
        """Prevent reverse DNS resolution delay on Windows localhost (::1 / 127.0.0.1)."""
        return str(self.client_address[0])

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def log_message(self, format, *args):
        pass

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Requested-With')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path in ("", "/", "/index.html"):
            index_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(index_path):
                try:
                    with open(index_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_error(500, f"Error reading index.html: {e}")
                    return

        if parsed.path == "/state":
            state = build_office_state()
            self._send_json_response(state)
            return

        if parsed.path == "/api/status":
            status_data = {
                "status": "online",
                "app": "Hermes Visual Agent Desk & Modern Campus",
                "version": "5.0",
                "port": PORT,
                "data_dir": DATA_DIR,
                "artifacts_dir": ARTIFACTS_DIR,
                "events_file": EVENTS_FILE,
                "demo_running": _demo_running,
                "active_worksheet": _active_worksheet_id,
                "server_time": datetime.now().isoformat()
            }
            self._send_json_response(status_data)
            return

        if parsed.path == "/api/worksheets":
            ws_list = load_worksheets()
            self._send_json_response({
                "activeId": _active_worksheet_id,
                "worksheets": ws_list
            })
            return

        if parsed.path == "/api/demo/toggle":
            is_running = toggle_demo_mode()
            self._send_json_response({"demo_running": is_running})
            return

        if parsed.path == "/api/hermes/sessions":
            sess = get_hermes_sessions()
            self._send_json_response({"sessions": sess})
            return

        if parsed.path == "/api/hermes/messages":
            qs = urllib.parse.parse_qs(parsed.query)
            sid = qs.get("session_id", [""])[0]
            msgs = get_hermes_messages(sid)
            self._send_json_response({"session_id": sid, "messages": msgs})
            return

        if parsed.path == "/api/history":
            telemetry_file = os.path.join(DATA_DIR, "telemetry_history.jsonl")
            logs = []
            if os.path.exists(telemetry_file):
                with open(telemetry_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                logs.append(json.loads(line))
                            except Exception:
                                pass
            self._send_json_response({"count": len(logs), "logs": logs[-50:]})
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"

        try:
            payload = json.loads(post_body)
        except Exception as e:
            self.send_error(400, f"Invalid JSON payload: {str(e)}")
            return

        # Hermes Interactive Workspace Chat & Execution
        if parsed.path == "/api/hermes/chat":
            sid = payload.get("session_id") or "local-d88d47d76f7775a808ef671244ea73631e9554801dd17fa85dd86c688d172234"
            user_msg = str(payload.get("message", "")).strip()
            target_agent = payload.get("agent_id") or "sess-hermes-prime"
            if not user_msg:
                self.send_error(400, "Empty message")
                return

            now = time.time()
            user_turn = {
                "id": int(now * 1000),
                "role": "user",
                "content": user_msg,
                "timestamp": now
            }
            if sid not in _hermes_memory_chat:
                _hermes_memory_chat[sid] = []
            _hermes_memory_chat[sid].append(user_turn)

            # Trigger physical agent movement in Star Office!
            publish_event({
                "event": "agent_behavior",
                "session_id": target_agent,
                "behavior": "desk",
                "activity": "typing",
                "detail": f"Mengerjakan: {user_msg[:40]}"
            })
            publish_event({
                "event": "tool_start",
                "session_id": target_agent,
                "tool_name": "execute_hermes_task",
                "activity": "typing",
                "preview": user_msg[:60]
            })

            agent_info = AGENT_PROFILES.get(target_agent, {})
            agent_name = agent_info.get("label", "Hermes Prime")
            resp_text = f"Instruksi diterima oleh **{agent_name}**:\n> *\"{user_msg}\"*\n\n✅ Tugas sedang diproses dan diverifikasi di workstation. Event telemetri telah dicatat ke audit ledger `data/events.jsonl`."
            
            assistant_turn = {
                "id": int(now * 1000) + 1,
                "role": "assistant",
                "reasoning": f"Memproses perintah user: {user_msg}",
                "tool_name": "run_command",
                "content": resp_text,
                "timestamp": now + 0.5
            }
            _hermes_memory_chat[sid].append(assistant_turn)

            publish_event({
                "event": "tool_end",
                "session_id": target_agent,
                "tool_name": "execute_hermes_task",
                "status": "ok"
            })

            self._send_json_response({
                "success": True,
                "session_id": sid,
                "user_message": user_turn,
                "assistant_message": assistant_turn
            })
            return

        # Worksheet Switcher & Sync
        if parsed.path == "/api/worksheets/switch":
            ws_id = payload.get("id")
            global _active_worksheet_id
            if ws_id:
                _active_worksheet_id = ws_id
                ws_list = load_worksheets()
                active_ws = next((w for w in ws_list if w["id"] == ws_id), None)
                if active_ws:
                    assigned = active_ws.get("assigned", [])
                    # Move assigned agents to workstations, unassigned to park benches
                    for aid in ["hermes", "athena", "hephaestus", "iris", "zephyr"]:
                        sid = AGENT_ID_MAP.get(aid, f"sess-{aid}")
                        if aid in assigned:
                            publish_event({
                                "event": "agent_behavior",
                                "session_id": sid,
                                "behavior": "desk",
                                "activity": "typing",
                                "detail": f"Bekerja pada {active_ws['title']}"
                            })
                        else:
                            publish_event({
                                "event": "agent_behavior",
                                "session_id": sid,
                                "behavior": "bench",
                                "activity": "resting",
                                "detail": "Istirahat santai di bangku taman"
                            })
                self._send_json_response({"success": True, "activeId": _active_worksheet_id})
                return

        if parsed.path == "/api/worksheets/save":
            ws_id = payload.get("id")
            content = payload.get("deliverable")
            ws_list = load_worksheets()
            for w in ws_list:
                if w["id"] == ws_id:
                    w["deliverable"] = content
                    w["updated_at"] = datetime.now().isoformat()
            save_worksheets(ws_list)
            self._send_json_response({"success": True})
            return

        if parsed.path == "/api/worksheets/create":
            title = payload.get("title", "Pembahasan Baru")
            goal = payload.get("goal", "")
            assigned = payload.get("assigned", ["hermes"])
            ws_list = load_worksheets()
            new_code = chr(ord('A') + (len(ws_list) % 26))
            new_ws = {
                "id": f"ws-{int(time.time())}",
                "code": new_code,
                "title": title,
                "category": payload.get("category", "General"),
                "status": "active",
                "assigned": assigned,
                "goal": goal,
                "deliverable": f"# Lembar Kerja {new_code}: {title}\n**Tujuan**: {goal}\n**Dibuat**: {datetime.now().isoformat()}\n\nCatatan kerja agen...",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            ws_list.append(new_ws)
            save_worksheets(ws_list)
            _active_worksheet_id = new_ws["id"]
            self._send_json_response({"success": True, "worksheet": new_ws})
            return

        # Direct agent command instruction
        if parsed.path == "/api/agent/command":
            aid = payload.get("id")
            cmd = payload.get("command") or payload.get("message") or ""
            if aid and cmd:
                publish_event({
                    "event": "agent_behavior",
                    "session_id": aid,
                    "behavior": "desk",
                    "activity": "typing",
                    "detail": f"Instruksi User: {cmd[:42]}"
                })
                publish_event({
                    "event": "tool_start",
                    "session_id": aid,
                    "tool_name": "user_command",
                    "activity": "typing",
                    "preview": cmd
                })
                self._send_json_response({"success": True, "agent": aid, "message": "Instruksi diproses"})
                return

        # Micro-Interactivity: direct agent action
        if parsed.path == "/api/agent/action":
            aid = payload.get("id")
            action = payload.get("action")
            if aid and action:
                if action == "bench":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "bench", "activity": "resting", "detail": "Duduk santai di bangku taman 🍃"})
                elif action == "walk":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "walking", "activity": "resting", "detail": "Jalan-jalan meregangkan pikiran di taman 🚶"})
                elif action == "coffee":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "drinking", "activity": "resting", "detail": "Menikmati matcha latte hangat 🍵"})
                elif action == "work":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "desk", "activity": "typing", "detail": "Kembali fokus coding di workstation ⚡"})
                elif action == "meeting":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "meeting", "activity": "delegating", "detail": "Bergabung ke ruang rapat all-hands 📢"})
                elif action == "chat":
                    msg = payload.get("message", "Mengerjakan instruksi!")
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "desk", "activity": "delegating", "detail": f"Instruksi: {msg}"})
                self._send_json_response({"success": True, "agent": aid, "action": action})
                return

        # Macro-Interactivity: global actions
        if parsed.path == "/api/office/macro":
            macro_action = payload.get("action")
            sids = ["sess-hermes-prime", "sess-athena-core", "sess-hephaestus", "sess-iris-ui", "sess-zephyr"]
            if macro_action == "meeting":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "meeting", "activity": "delegating", "detail": "Rapat All-Hands di Meja Bundar"})
                self._send_json_response({"success": True, "macro": "meeting", "message": "Semua agen berkumpul untuk rapat"})
                return
            elif macro_action == "break":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "bench", "activity": "resting", "detail": "Rehat bersama di bangku taman & gazebo"})
                self._send_json_response({"success": True, "macro": "break", "message": "Semua agen menikmati istirahat di taman"})
                return
            elif macro_action == "sprint":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "desk", "activity": "typing", "detail": "Turbo Sprint: Overclock coding di workstation"})
                self._send_json_response({"success": True, "macro": "sprint", "message": "Semua agen kembali sprint coding"})
                return
            elif macro_action == "roam":
                for sid in sids:
                    b = random.choice(["bench", "drinking", "walking"])
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": b, "activity": "resting", "detail": "Bebas berkeliling kantor & taman"})
                self._send_json_response({"success": True, "macro": "roam", "message": "Agen bebas berkeliling"})
                return

        if parsed.path == "/api/event":
            publish_event(payload)
            self._send_json_response({"success": True, "message": "Event recorded"})
            return

        if parsed.path == "/api/save_log":
            payload["saved_at"] = datetime.now().isoformat()
            telemetry_file = os.path.join(DATA_DIR, "telemetry_history.jsonl")
            with open(telemetry_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self._send_json_response({"success": True, "message": "Log recorded"})
            return

        if parsed.path == "/api/save_artifact":
            title = payload.get("title", "artifact")
            content = payload.get("content", "")
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_slug = re.sub(r'[^a-zA-Z0-9_\-]+', '_', title.lower()).strip('_')[:32]
            filename = f"{timestamp_str}_{safe_slug}.md"
            filepath = os.path.join(ARTIFACTS_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n")
                f.write(f"> Disimpan otomatis oleh Hermes Visual Desk pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(content)
                f.write("\n")

            manifest_file = os.path.join(ARTIFACTS_DIR, "manifest.json")
            manifest = []
            if os.path.exists(manifest_file):
                try:
                    with open(manifest_file, "r", encoding="utf-8") as mf:
                        manifest = json.load(mf)
                except Exception:
                    manifest = []
            manifest.append({
                "filename": filename,
                "title": title,
                "path": filepath,
                "saved_at": datetime.now().isoformat()
            })
            with open(manifest_file, "w", encoding="utf-8") as mf:
                json.dump(manifest, mf, indent=2, ensure_ascii=False)

            self._send_json_response({
                "success": True,
                "filename": filename,
                "saved_to": filepath,
                "message": f"Artefak berhasil disimpan ke {filename}"
            })
            return

        self.send_error(404, "Endpoint not found")

    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

def run():
    global _demo_thread
    init_in_memory_state()
    _demo_thread = threading.Thread(target=demo_worker, daemon=True)
    _demo_thread.start()

    server_address = ('::', PORT)
    httpd = DualStackThreadingHTTPServer(server_address, DeskBridgeHandler)
    print("=" * 65, flush=True)
    print(f"[*] Hermes Visual Agent Desk & Modern Campus (v5.0) Aktif", flush=True)
    print(f"[*] Web Access : http://localhost:{PORT} atau http://127.0.0.1:{PORT}", flush=True)
    print(f"[*] Worksheets : http://localhost:{PORT}/api/worksheets", flush=True)
    print(f"[*] /state API : http://localhost:{PORT}/state", flush=True)
    print("=" * 65, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.", flush=True)
        httpd.server_close()

if __name__ == '__main__':
    run()
