# 🪄 Hermes Visual Agent Desk — 3D Pixel Garden (HD)

> **Antarmuka visual interaktif berbasis 3D Voxel / Pixel Art untuk memantau, berinteraksi, dan mengeksekusi misi agen cerdas Hermes secara menyenangkan dan bebas bosan.**

![HTML5](https://img.shields.io/badge/HTML5-Single--File-E34F26?logo=html5&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-r128-black?logo=three.js)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v3-38B2AC?logo=tailwind-css&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)

---

## ✨ Fitur Utama

- **🏝️ 3D Voxel Cheerful Garden (Three.js)**:
  - Pulau taman voxel terapung lengkap dengan air mancur kristal berputar, kolam ikan koi animasi, pohon sakura voxel, lentera malam bercahaya, dan partikel kelopak bunga yang melayang.
  - Kamera interaktif 360° (orbit drag, zoom scroll, klik stasiun kerja agen untuk autofokus kamera).
- **🤖 4 Stasiun Kerja Multi-Agent**:
  - **Hermes Prime** (`#F59E0B`): Koordinator strategi & eksekusi misi.
  - **Athena Owl** (`#10B981`): Analisis referensi, pengetahuan & Vector DB.
  - **Hephaestus Forge** (`#F43F5E`): Kompilasi kode, refaktor & pengujian sandbox.
  - **Iris Prism** (`#A855F7`): Desain UI/UX, tema visual, dan pemolesan artefak.
- **⚡ Visual Packet Messenger**: Paket data berpendar terbang melintasi busur parabola 3D antar-stasiun saat agen berkolaborasi.
- **🎵 Synthesizer Chiptune Prosedural**: Efek suara 8-bit retro disintesis langsung menggunakan browser **Web Audio API** (tanpa butuh file MP3/WAV eksternal).
- **🌓 Siklus Waktu & Filter Retro**:
  - Pilihan pencahayaan atmosfer: **Pagi Cerah**, **Senja Keemasan**, dan **Malam Lentera**.
  - Switcher resolusi: **Crisp HD-2D Voxel** atau **Crunchy Retro 16-Bit**.
- **☕ Interaksi Menyenangkan**:
  - Tombol **Traktir Matcha** (Matcha Latte cheer break untuk semua agen).
  - Tombol **Turbo Mode** (Overclock kecepatan agen & paket visual 2x).
  - Tombol **Rayakan di Taman** (Pesta kembang api partikel cahaya).
- **💾 Micro Bridge Server (Python Standar)**:
  - Menyediakan endpoint lokal untuk auto-save log telemetri ke `data/telemetry_history.jsonl`.
  - Menyimpan artefak hasil kerja agen langsung ke berkas Markdown di `data/artifacts/`.
  - Fallback otomatis: Jika bridge offline, berkas tetap dapat diunduh langsung lewat browser atau disalin ke clipboard!

---

## 🚀 Cara Menjalankan

### Cara 1: Sangat Ringan (Zero-Dependency)
Cukup buka file `index.html` langsung di browser Chrome, Edge, atau Firefox (klik ganda dari File Explorer atau via terminal):
```powershell
Start-Process "index.html"
```
*Seluruh fitur visual, audio 8-bit, animasi 3D, dan pengujian misi langsung aktif 100%.*

---

### Cara 2: Lengkap dengan Auto-Save ke Drive (Rekomendasi)
Jalankan file batch launcher:
```powershell
.\run_desk.bat
```
Atau via Python langsung:
```powershell
python bridge.py
```
Lalu buka browser ke **`http://localhost:8765`**.
Indikator **Bridge Aktif** di HUD atas akan menyala hijau, dan setiap misi atau artefak yang kamu hasilkan akan otomatis tersimpan ke folder `data/artifacts/`.

---

## 📁 Struktur Berkas

```
visual_agent_desk/
│
├── index.html          # Standalone Single-File 3D Voxel Desk (HTML + CSS + Three.js)
├── bridge.py           # Zero-dependency Python micro-bridge & static server (Port 8765)
├── run_desk.bat        # Windows Batch One-Click Launcher
├── run_desk.ps1        # PowerShell One-Click Launcher
├── README.md           # Dokumentasi lengkap
│
└── data/               # Folder penyimpanan data lokal
    ├── telemetry_history.jsonl   # Riwayat log aktivitas agen
    ├── missions_history.jsonl    # Riwayat misi
    └── artifacts/                # Berkas output (.md) yang dihasilkan tim Hermes
        └── manifest.json         # Indeks artefak tersimpan
```

---

## 🎨 Keyboard & Mouse Controls

| Aksi | Kontrol |
|---|---|
| **Rotasi Kamera** | Klik kiri mouse + drag |
| **Zoom In / Out** | Scroll roda mouse (wheel) |
| **Fokus ke Agen** | Klik kiri pada model stasiun agen di taman 3D |
| **Reset Kamera** | Tombol **Overview** di HUD atas |
| **Kirim Misi** | Ketik di kolom input bawah lalu tekan `Enter` atau tombol `Dispatch` |

---

*Dibuat untuk ekosistem CHARISNA SuperApp & Hermes Autonomous Workspace.*
