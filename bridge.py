#!/usr/bin/env python3
"""
Hermes Visual Agent Desk — Micro Bridge Server
------------------------------------------------
Provides a lightweight local HTTP server and file-persistence API
for the 3D Pixel Garden Desk.

Zero dependencies: Runs purely on Python standard library.
Default URL: http://localhost:8765
Data Directory: ./data
"""

import os
import sys
import json
import time
import re
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARTIFACTS_DIR = os.path.join(DATA_DIR, "artifacts")

# Ensure required storage folders exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

class DeskBridgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local cross-origin access (e.g., file:/// or localhost)
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

        if parsed.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            status_data = {
                "status": "online",
                "app": "Hermes Visual Agent Desk — 3D Pixel Garden",
                "version": "3.8",
                "port": PORT,
                "data_dir": DATA_DIR,
                "artifacts_dir": ARTIFACTS_DIR,
                "server_time": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(status_data, indent=2).encode("utf-8"))
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
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"count": len(logs), "logs": logs[-50:]}).encode("utf-8"))
            return

        # Default: Serve static files
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

            # Update manifest
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
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, DeskBridgeHandler)
    print("=" * 65)
    print(f"✨ Hermes Visual Agent Desk — Micro Bridge Aktif")
    print(f"🌐 Akses Web : http://localhost:{PORT}")
    print(f"📁 Data Path : {DATA_DIR}")
    print(f"📄 Artefak   : {ARTIFACTS_DIR}")
    print("=" * 65)
    print("Tekan Ctrl+C untuk menghentikan server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan dengan aman.")
        httpd.server_close()

if __name__ == '__main__':
    run()
