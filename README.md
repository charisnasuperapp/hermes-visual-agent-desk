# 🪄 Hermes Visual Agent Desk & Pixel Office (HD)

> **Antarmuka visual agen cerdas Hermes: Dual-View (Taman 3D Voxel Garden & Kantor 2D Hermes Pixel Office). Terinspirasi langsung dari `teknium1/hermes-pixel-office` dan `pixel-agents-hq/pixel-agents`.**

![HTML5](https://img.shields.io/badge/HTML5-Dual--View-E34F26?logo=html5&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-r128-black?logo=three.js)
![Canvas 2D](https://img.shields.io/badge/Canvas_2D-Pixel_Office-9b6fd8)
![Hermes Spec](https://img.shields.io/badge/Hermes-Pixel_Office_Compatible-F59E0B)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)

---

## ✨ Fitur Utama

### 1. Dual-View Mode (Beralih Kapan Saja di HUD Atas)
- **🏝️ Taman 3D Voxel (Three.js HD)**:
  - Taman terapung dengan kristal emas berputar, kolam ikan koi bergerak, pohon sakura voxel, partikel kelopak bunga melayang, dan stasiun kerja 3D.
  - Kamera interaktif 360° (orbit drag, zoom scroll, klik stasiun kerja agen untuk autofokus kamera).
- **🏢 Kantor 2D Hermes Pixel Office (Canvas 2D)**:
  - Arsitektur retro pixel office persis `hermes-pixel-office` (Teknium / Nous Research).
  - Agen berjalan masuk lewat pintu, duduk di meja kerja masing-masing, dan berjalan keluar saat sesi berakhir.
  - Monitor berubah warna sesuai aktivitas (`running` terminal hijau, `browsing` biru, `typing` flicker, `waiting` merah).
  - **Subagent Kalung Emas**: Subagent hasil delegasi task otomatis memakai kalung emas (`#e8c170`) dan mendapatkan meja sendiri!
  - **Balon `!` Approval**: Muncul peringatan tanda seru merah dan chime peringatan jika ada command sensitif.
  - Perabot kantor interaktif: Pendingin air, mesin kopi, tanaman sudut, karpet kantor, dan jendela kaca.

### 2. Standard Hermes `/state` & Event Stream (`bridge.py`)
- **Kompatibel 100% dengan `teknium1/hermes-pixel-office`**:
  - Endpoint `GET /state` menyajikan status live seluruh agen (`working`, `thinking`, `waiting`, `done`, `idle`, `gone`).
  - Endpoint `POST /api/event` menerima event hook Hermes (`session_start`, `subagent_start`, `tool_start`, `approval_request`).
  - Auto-trim `data/events.jsonl` jika melebihi 512 KB.

### 3. ▶ Built-in Live Simulation Feed
- Tombol **Simulasi** di top HUD untuk mengaktifkan generator sesi & subagent sintetis di background (seperti `demo_feed.py` Nous Research). Sangat cocok untuk mengamati gerak-gerik agen saat santai.

### 4. 💾 Auto-Save Nyata ke Drive
- Auto-save riwayat telemetri ke `data/telemetry_history.jsonl`.
- Auto-save berkas kode / artefak markdown ke `data/artifacts/`.
- Fallback browser download instan jika bridge sedang offline.

---

## 🚀 Cara Menjalankan

### Cara 1: Sangat Ringan (Zero-Dependency)
Cukup buka file `index.html` langsung di browser Chrome, Edge, atau Firefox:
```powershell
Start-Process "index.html"
```
*Taman 3D dan Kantor 2D langsung aktif secara mandiri.*

---

### Cara 2: Lengkap dengan Micro-Bridge & Auto-Save (Rekomendasi)
Jalankan batch launcher:
```powershell
.\run_desk.bat
```
Atau via Python:
```powershell
python bridge.py
```
Lalu buka browser ke **`http://localhost:8765`**.

---

## 📁 Struktur Berkas

```
visual_agent_desk/
│
├── index.html          # Dual-View Web App (3D Three.js Garden + 2D Pixel Office Canvas)
├── bridge.py           # Micro Bridge, /state folding server, dan Live Simulator
├── run_desk.bat        # Windows Batch One-Click Launcher
├── run_desk.ps1        # PowerShell One-Click Launcher
├── README.md           # Dokumentasi lengkap
│
└── data/               # Penyimpanan lokal
    ├── events.jsonl              # Stream event lifecycle Hermes
    ├── telemetry_history.jsonl   # Riwayat log aktivitas
    └── artifacts/                # Berkas output markdown yang dihasilkan agen
        └── manifest.json         # Indeks artefak tersimpan
```

---

## 🎨 Kontrol

| Aksi | Kontrol |
|---|---|
| **Ganti Tampilan** | Klik tombol `Taman 3D` atau `Kantor 2D` di HUD atas |
| **Simulasi Live** | Klik tombol `Simulasi` di HUD atas untuk memicu agen & subagent |
| **Rotasi 3D** | Klik kiri mouse + drag |
| **Zoom In/Out** | Scroll roda mouse (wheel) |
| **Traktir Matcha** | Tombol di panel kanan bawah untuk menyegarkan agen |
| **Simpan Artefak** | Tombol `Simpan` di tab artefak untuk menulis langsung ke `data/artifacts/` |

---

*Dibuat untuk ekosistem CHARISNA SuperApp & Hermes Autonomous Workspace.*
