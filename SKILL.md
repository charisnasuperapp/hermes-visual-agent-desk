---
name: hermes-visual-agent-desk
description: Panduan dan integrasi resmi Charisna Visual Agent Desk untuk Hermes AI dan autonomous agents ekosistem Charisna SuperApp.
---

# Charisna Visual Agent Desk - Hermes Operations Skill

Skill ini mengatur integrasi visual antara sistem **Hermes AI** dengan **Charisna Visual Agent Desk** (dashboard kantor virtual pixel art).

---

## 1. Menjalankan Dashboard Kantor

Jalankan perintah berikut di PowerShell atau Command Prompt:

```powershell
python backend/app.py
```

Dashboard akan aktif di `http://127.0.0.1:19000`.

---

## 2. Mengubah Status Kantor via Skrip / API

Saat Hermes sedang mengerjakan tugas tertentu, Hermes dapat mempublikasikan statusnya:

```powershell
# Bekerja di meja
python set_state.py writing "Sedang memprogram fitur baru"

# Sinkronisasi ke server
python set_state.py syncing "Menjalankan sinkronisasi database"

# Terjadi error / investigasi
python set_state.py error "Investigasi bug atau kegagalan run"

# Istirahat di sofa
python set_state.py idle "Standby & siap menerima instruksi"
```

Hermes otomatis akan berjalan kaki dengan animasi (*anti-teleport*) ke area yang sesuai di panggung kantor.

---

## 3. Integrasi Tim Multi-Agent

Daftar agent resmi yang aktif di kantor tercatat di `agents-state.json`:
- **Hermes**: Chief AI Architect
- **Onal AI**: Universal Memory
- **Bumi POS**: Bumi Makmur Retail
- **Homestay Bot**: Charisna Homestay
- **MoniFlow**: Financial Ledger
- **Codex Dev**: DevOps Automator
- **Kuro Patrol**: Security Sentinel
