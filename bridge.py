#!/usr/bin/env python3
"""
Hermes Visual Agent Desk & Pixel Office — Core Bridge Server
--------------------------------------------------------------
Provides a high-performance local HTTP server, state-folding engine,
file persistence, and Hermes event-sourcing API.

Features:
- Dual-View Support: 3D Voxel Studio & 2D Pixel Virtual Office
- Autonomous Agent Behaviors: Working, Walking, Resting, Drinking, Meeting
- Micro-Interactivity: Direct commands to individual agents (Coffee, Rest, Code, Chat)
- Macro-Interactivity: All-hands Team Meeting, Group Break, Turbo Sprint
- Native VS Code Extension Bridge (/state & CORS)
- Zero external dependencies: Python 3 standard library only

Default URL: http://127.0.0.1:8765 or http://localhost:8765
"""

import os
import sys
import json
import time
import re
import random
import socket
import threading
from datetime import datetime
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import urllib.parse
from pathlib import Path

class DualStackThreadingHTTPServer(ThreadingHTTPServer):
    """Multi-threaded HTTP Server supporting both IPv4 (127.0.0.1) and IPv6 (::1/localhost)."""
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        try:
            self.address_family = socket.AF_INET6
            super().__init__(('::', server_address[1]), RequestHandlerClass, bind_and_activate=False)
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            if bind_and_activate:
                self.server_bind()
                self.server_activate()
        except Exception as e:
            self.address_family = socket.AF_INET
            super().__init__(('0.0.0.0', server_address[1]), RequestHandlerClass, bind_and_activate)

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
_MAX_LOG_BYTES = 512 * 1024
_STALE_SECONDS = 30 * 60

# Ensure storage directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

_lock = threading.Lock()
_demo_running = True  # Active by default for immediate lively experience
_demo_thread = None

# Custom agent overrides (from micro-interactivity)
_agent_overrides = {}

def publish_event(event: dict) -> None:
    try:
        event.setdefault("ts", time.time())
        event.setdefault("pid", os.getpid())
        line = json.dumps(event, ensure_ascii=False, default=str)
        with _lock:
            with open(EVENTS_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            maybe_trim_events()
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

def read_events() -> list:
    if not os.path.exists(EVENTS_FILE):
        return []
    out = []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
    except Exception as e:
        print(f"[!] Error reading events: {e}")
    return out

def _short(text, n=60):
    s = str(text or "").strip().replace("\n", " ")
    return s[: n - 1] + "…" if len(s) > n else s

def build_office_state() -> dict:
    """Fold events.jsonl into current live agent snapshots (Hermes Pixel Office spec)."""
    agents = {}
    now = time.time()

    def ensure(key: str, ev: dict) -> dict:
        a = agents.get(key)
        if a is None:
            a = {
                "id": key,
                "label": f"agent {key[-6:]}",
                "kind": "main",
                "status": "idle",
                "tool": "",
                "activity": "working",
                "detail": "",
                "behavior": "desk",  # desk, walking, resting, drinking, meeting
                "platform": ev.get("platform") or "hermes",
                "first_seen": ev.get("ts", now),
                "updated_at": ev.get("ts", now),
            }
            agents[key] = a
        a["updated_at"] = ev.get("ts", a["updated_at"])
        return a

    for ev in read_events():
        kind = ev.get("event")
        key = ev.get("session_id") or ev.get("child_session_id") or f"pid-{ev.get('pid', 'core')}"

        if kind == "session_start":
            a = ensure(key, ev)
            a["status"] = "idle"
            a["behavior"] = "desk"
            plat = ev.get("platform") or ""
            a["label"] = f"{plat or 'hermes'} {key[-6:]}"
            a["detail"] = "session started"
        elif kind == "session_end":
            if key in agents:
                agents[key]["status"] = "gone"
                agents[key]["behavior"] = "walking_out"
                agents[key]["updated_at"] = ev.get("ts", now)
        elif kind == "subagent_start":
            child = ev.get("child_session_id")
            if child:
                ck = str(child)
                ev2 = dict(ev)
                ev2["session_id"] = ck
                a = ensure(ck, ev2)
                a["kind"] = "subagent"
                a["label"] = _short(ev.get("child_goal"), 26) or f"sub {ck[-6:]}"
                a["status"] = "working"
                a["behavior"] = "desk"
                a["detail"] = _short(ev.get("child_goal"))
                a["parent"] = str(ev.get("parent_session_id") or "")
        elif kind == "subagent_stop":
            child = ev.get("child_session_id")
            if child and str(child) in agents:
                agents[str(child)]["status"] = "done"
                agents[str(child)]["behavior"] = "resting"
                agents[str(child)]["updated_at"] = ev.get("ts", now)
        elif kind == "tool_start":
            a = ensure(key, ev)
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
            a = ensure(key, ev)
            a["status"] = "thinking"
            a["tool"] = ""
            if ev.get("status") == "error":
                a["detail"] = f"⚠ {_short(ev.get('error_message'), 40)}"
            else:
                a["detail"] = ""
        elif kind == "approval_request":
            a = ensure(key, ev)
            a["status"] = "waiting"
            a["behavior"] = "desk"
            a["tool"] = ""
            a["detail"] = _short(ev.get("command"), 40) or "needs approval"
        elif kind == "approval_response":
            a = ensure(key, ev)
            choice = str(ev.get("choice") or "")
            if choice in ("deny", "timeout"):
                a["status"] = "thinking"
                a["detail"] = f"approval: {choice}"
            else:
                a["status"] = "working"
                a["detail"] = ""
        elif kind == "agent_behavior":
            a = ensure(key, ev)
            a["behavior"] = ev.get("behavior", "desk")
            a["activity"] = ev.get("activity", a.get("activity", "working"))
            if ev.get("detail"):
                a["detail"] = ev.get("detail")

    # Apply manual micro-overrides
    for aid, override in _agent_overrides.items():
        if aid in agents:
            agents[aid].update(override)

    visible = []
    for a in agents.values():
        age = now - float(a.get("updated_at") or 0)
        if a["status"] == "gone" and age > 25:
            continue
        if a["status"] == "done" and age > 90:
            continue
        if age > _STALE_SECONDS:
            continue
        if a["status"] in ("working", "thinking") and age > 240:
            a["status"] = "idle"
            a["behavior"] = "resting"
        visible.append(a)

    visible.sort(key=lambda a: (a["kind"] != "main", a.get("first_seen", 0)))
    return {"agents": visible, "ts": now}

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
DEMO_GOALS = [
    "Refactor neural pipeline",
    "Benchmark 60 FPS Three.js loop",
    "Synthesize 8-bit sound chimes",
    "Security audit & sandboxing",
    "Deploy Charisna office cluster"
]

def demo_worker():
    global _demo_running
    publish_event({"event": "session_start", "session_id": "sess-hermes-prime", "platform": "hermes"})
    publish_event({"event": "session_start", "session_id": "sess-athena-core", "platform": "athena"})
    publish_event({"event": "session_start", "session_id": "sess-hephaestus", "platform": "forge"})
    publish_event({"event": "session_start", "session_id": "sess-iris-ui", "platform": "prism"})
    
    live_subs = []
    counter = 0

    while _demo_running:
        counter += 1
        sids = ["sess-hermes-prime", "sess-athena-core", "sess-hephaestus", "sess-iris-ui"]

        # Cycle tasks and autonomous wandering/resting
        for sid in sids:
            if not _demo_running:
                break
            
            # 20% chance to take a walk or rest
            rnd = random.random()
            if rnd < 0.20:
                behavior = random.choice(["resting", "drinking", "walking"])
                detail = "Menikmati matcha hangat di lounge" if behavior == "resting" else "Mengambil air minum di cooler" if behavior == "drinking" else "Jalan-jalan meregangkan pikiran"
                publish_event({"event": "agent_behavior", "session_id": sid, "behavior": behavior, "activity": "resting", "detail": detail})
                time.sleep(random.uniform(2.5, 4.0))
                publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "desk", "activity": "working", "detail": "Kembali ke meja kerja"})
            else:
                tool, act, args = random.choice(DEMO_TOOLS)
                publish_event({"event": "tool_start", "session_id": sid, "tool_name": tool, "activity": act, "preview": str(args)})
                time.sleep(random.uniform(2.0, 3.5))
                publish_event({"event": "tool_end", "session_id": sid, "tool_name": tool, "status": "ok"})

        if not _demo_running:
            break

        # Spawn subagents
        if len(live_subs) < 3 and random.random() < 0.55:
            sub_id = f"sub-{counter}"
            goal = random.choice(DEMO_GOALS)
            publish_event({"event": "subagent_start", "parent_session_id": "sess-hermes-prime", "child_session_id": sub_id, "child_goal": goal})
            tool, act, args = random.choice(DEMO_TOOLS)
            publish_event({"event": "tool_start", "session_id": sub_id, "tool_name": tool, "activity": act, "preview": goal})
            live_subs.append(sub_id)

        if live_subs and random.random() < 0.40:
            done_sub = live_subs.pop(0)
            publish_event({"event": "tool_end", "session_id": done_sub, "tool_name": "terminal", "status": "ok"})
            publish_event({"event": "subagent_stop", "child_session_id": done_sub})

        # All-hands meeting occasion
        if counter % 7 == 4:
            for s in sids:
                publish_event({"event": "agent_behavior", "session_id": s, "behavior": "meeting", "activity": "delegating", "detail": "Rapat koordinasi tim di pusat kantor"})
            time.sleep(4.5)
            for s in sids:
                publish_event({"event": "agent_behavior", "session_id": s, "behavior": "desk", "activity": "working", "detail": "Rapat selesai, kembali fokus"})

        # Approval request
        elif counter % 6 == 3:
            publish_event({"event": "approval_request", "session_id": "sess-hermes-prime", "command": "deploy production update"})
            time.sleep(3.5)
            publish_event({"event": "approval_response", "session_id": "sess-hermes-prime", "choice": "approve"})

        time.sleep(random.uniform(2.0, 3.5))

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

    def handle(self):
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            pass

    def log_message(self, format, *args):
        # Clean silent logging to prevent console encoding clutter
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

        if parsed.path == "/state":
            state = build_office_state()
            self._send_json_response(state)
            return

        if parsed.path == "/api/status":
            status_data = {
                "status": "online",
                "app": "Hermes Visual Agent Desk & Pixel Office Pro",
                "version": "4.2",
                "port": PORT,
                "data_dir": DATA_DIR,
                "artifacts_dir": ARTIFACTS_DIR,
                "events_file": EVENTS_FILE,
                "demo_running": _demo_running,
                "server_time": datetime.now().isoformat()
            }
            self._send_json_response(status_data)
            return

        if parsed.path == "/api/demo/toggle":
            is_running = toggle_demo_mode()
            self._send_json_response({"demo_running": is_running})
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

        # Micro-Interactivity: direct agent action
        if parsed.path == "/api/agent/action":
            aid = payload.get("id")
            action = payload.get("action")
            if aid and action:
                if action == "coffee":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "drinking", "activity": "resting", "detail": "Menikmati seduhan matcha latte hangat"})
                elif action == "rest":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "resting", "activity": "resting", "detail": "Sedang istirahat santai di sofa lounge"})
                elif action == "work":
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "desk", "activity": "typing", "detail": "Fokus coding di terminal"})
                elif action == "chat":
                    msg = payload.get("message", "Siap menjalankan instruksi!")
                    publish_event({"event": "agent_behavior", "session_id": aid, "behavior": "desk", "activity": "delegating", "detail": f"Pesan: {msg}"})
                self._send_json_response({"success": True, "agent": aid, "action": action})
                return

        # Macro-Interactivity: global actions
        if parsed.path == "/api/office/macro":
            macro_action = payload.get("action")
            sids = ["sess-hermes-prime", "sess-athena-core", "sess-hephaestus", "sess-iris-ui"]
            if macro_action == "meeting":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "meeting", "activity": "delegating", "detail": "Rapat All-Hands Tim di meja bundar"})
                self._send_json_response({"success": True, "macro": "meeting", "message": "Semua agen berkumpul untuk rapat"})
                return
            elif macro_action == "break":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "resting", "activity": "resting", "detail": "Sesi istirahat bersama di lounge"})
                self._send_json_response({"success": True, "macro": "break", "message": "Semua agen menikmati istirahat"})
                return
            elif macro_action == "sprint":
                for sid in sids:
                    publish_event({"event": "agent_behavior", "session_id": sid, "behavior": "desk", "activity": "typing", "detail": "Overclock Sprint: Coding intensif"})
                self._send_json_response({"success": True, "macro": "sprint", "message": "Semua agen kembali sprint coding"})
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

        if parsed.path == "/api/save_mission":
            payload["saved_at"] = datetime.now().isoformat()
            mission_file = os.path.join(DATA_DIR, "missions_history.jsonl")
            with open(mission_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self._send_json_response({"success": True, "message": "Misi disimpan ke riwayat"})
            return

        self.send_error(404, "Endpoint not found")

    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

def run():
    # Start autonomous life simulator thread by default
    global _demo_thread
    _demo_thread = threading.Thread(target=demo_worker, daemon=True)
    _demo_thread.start()

    server_address = ('::', PORT)
    httpd = DualStackThreadingHTTPServer(server_address, DeskBridgeHandler)
    print("=" * 65)
    print(f"[*] Hermes Visual Agent Desk & Pixel Office (PRO) Aktif")
    print(f"[*] Web Access : http://127.0.0.1:{PORT} atau http://localhost:{PORT}")
    print(f"[*] /state API : http://127.0.0.1:{PORT}/state")
    print(f"[*] Data Path  : {DATA_DIR}")
    print(f"[*] Artifacts  : {ARTIFACTS_DIR}")
    print("=" * 65)
    print("Server siap melayani request secara multi-threaded (anti-crash).")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        httpd.server_close()

if __name__ == '__main__':
    run()
