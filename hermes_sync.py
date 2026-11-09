#!/usr/bin/env python3
"""Hermes to Star Office UI Realtime State Synchronizer.
Reads local Hermes SQLite state.db (AppData/Local/hermes/state.db) in read-only mode,
and keeps Star Office UI state.json updated with Hermes' active tasks.
"""

import os
import sys
import time
import json
import sqlite3
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HERMES_STATE_DB = os.path.expanduser(r"~\AppData\Local\hermes\state.db")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.json")

def get_latest_hermes_activity():
    if not os.path.exists(HERMES_STATE_DB):
        return None
    try:
        conn = sqlite3.connect(f"file:{HERMES_STATE_DB}?mode=ro", uri=True)
        cur = conn.cursor()
        row = cur.execute("""
            SELECT role, content, tool_name, timestamp 
            FROM messages 
            ORDER BY id DESC 
            LIMIT 1
        """).fetchone()
        conn.close()
        if row:
            role, content, tool_name, ts = row
            return {"role": role, "content": content or "", "tool_name": tool_name, "ts": ts}
    except Exception:
        pass
    return None

def update_star_office_state(state, detail):
    try:
        data = {
            "state": state,
            "detail": detail,
            "progress": 0,
            "updated_at": datetime.now().isoformat()
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Star Office State -> {state}: {detail}")
    except Exception as e:
        print(f"[!] Gagal menulis state.json: {e}")

def run_sync_loop():
    print("=" * 55)
    print("Hermes -> Star Office UI Synchronizer Aktif")
    print(f"Database Hermes: {HERMES_STATE_DB}")
    print(f"Target State   : {STATE_FILE}")
    print("=" * 55)

    last_ts = None
    while True:
        act = get_latest_hermes_activity()
        if act:
            ts = act.get("ts")
            if ts != last_ts:
                last_ts = ts
                role = act.get("role")
                tool = act.get("tool_name")
                content = (act.get("content") or "").strip().replace("\n", " ")[:60]

                if tool:
                    if tool in ("write_file", "patch", "edit_file"):
                        state = "writing"
                        detail = f"Coding ({tool}): {content}"
                    elif tool in ("read_file", "search_files", "grep", "web_search"):
                        state = "researching"
                        detail = f"Riset ({tool}): {content}"
                    else:
                        state = "executing"
                        detail = f"Menjalankan {tool}: {content}"
                elif role == "user":
                    state = "receiving"
                    detail = f"Instruksi User: {content}"
                elif role == "assistant":
                    state = "writing"
                    detail = f"Hermes: {content}"
                else:
                    state = "idle"
                    detail = "Standby & siap bertugas"

                update_star_office_state(state, detail)
        time.sleep(2.0)

if __name__ == "__main__":
    run_sync_loop()
