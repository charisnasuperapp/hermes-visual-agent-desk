# 🪄 Hermes Visual Agent Desk & Pixel Office Pro (v4.2)

> **Cockpit Visual Profesional untuk Agen AI Hermes: Dual-View (3D Cyberpunk Studio & 2D Pixel Virtual Office) dengan integrasi VS Code Extension, Autonomous Agent Life (Jalan-jalan, Istirahat Sofa, Ngopi Pantry, Rapat Konferensi), serta Micro & Macro Interactivity.**

![HTML5](https://img.shields.io/badge/HTML5-Dual--View-E34F26?logo=html5&logoColor=white)
![VS Code Extension](https://img.shields.io/badge/VS_Code-Ready-007ACC?logo=visual-studio-code)
![Three.js](https://img.shields.io/badge/Three.js-r128-black?logo=three.js)
![Canvas 2D](https://img.shields.io/badge/Canvas_2D-Pixel_Office-9b6fd8)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)

---

## 🌟 Fitur Baru & Pembaruan v4.2

### 1. 🌑 Tema Gelap Profesional (VS Code Dark Modern / JetBrains IDE)
- Seluruh antarmuka dirancang ulang menjadi palet gelap presisi tinggi: Obsidian `#090d16`, matte glass `#0f172a`, garis batas hairline `border-slate-800`, tipografi developer modern (`Inter` + `JetBrains Mono`).
- Menghapus tampilan warna pastel terang dan elemen kartun anak-anak.
- Mode malam studio 3D dengan pencahayaan moody, lentera hangat, dan obelisk kristal emas.

### 2. 🛋️ Autonomous Agent Life & Zona Kantor 2D
Agen tidak lagi hanya diam terpaku di satu kursi:
- **Zona Meja Pods**: Agen coding intensif dengan dual monitor ultra-wide yang berpendar sesuai jenis tool (`typing` hijau, `browsing` biru, `terminal` amber, `waiting` merah).
- **Zona Pantry & Bar Kopi**: Bar counter lengkap dengan mesin espresso beruap, lampu LED indikator, dispenser galon air, dan cangkir kopi. Agen berjalan ke sini saat ingin minum kopi (`☕`).
- **Zona Lounge Sofa**: Sofa santai beludru sectional dengan bantal empuk, meja kopi, dan tanaman ficus. Agen berjalan dan duduk santai di sini saat istirahat (`💤`).
- **Zona Meja Bundar Rapat (All-Hands Conference Table)**: Meja konferensi kayu mahoni solid dengan layar tengah hologram. Seluruh agen berkumpul di sini saat sesi koordinasi tim (`💬`).
- **Jalan-jalan (Wandering)**: Agen bergerak otonom antar koridor dengan animasi langkah kaki halus.

### 3. 🎯 Micro-Interactivity (Interaksi Perorangan Agen)
Klik agen mana saja (baik di tampilan 3D, kanvas 2D, maupun daftar squad di sidebar):
- Membuka **Agent Command Modal**:
  - ☕ **Traktir Kopi**: Agen beranjak ke barista pantry untuk menikmati matcha/kopi.
  - 🛋️ **Istirahat Lounge**: Agen berjalan ke sofa lounge untuk santai sejenak.
  - 💻 **Fokus Coding**: Agen kembali ke workstation dan memacu kecepatan coding.
  - 🎥 **Kunci Kamera**: Mengarahkan fokus kamera ke posisi agen tersebut.
  - 💬 **Kirim Instruksi Langsung**: Kotak input untuk mengirim prompt atau tugas spesifik ke agen terpilih.

### 4. 📢 Macro-Interactivity (Perintah Seluruh Tim)
Tombol di Top Header Bar:
- 📢 **Rapat Tim (Meeting)**: Semua agen serentak berdiri dan berjalan berkumpul ke Meja Konferensi untuk rapat All-Hands.
- ☕ **Rehat Massal (Break)**: Semua agen beristirahat bersama di lounge dan pantry kopi.
- ⚡ **Sprint Mode (Turbo Coding)**: Semua agen serempak kembali ke meja kerja dengan overclock kecepatan tinggi.

### 5. 🔌 Dual-Stack IPv4/IPv6 Anti-Crash Bridge (`bridge.py`)
- Server HTTP multi-threaded dengan dukungan otomatis dual-stack `AF_INET6` + `AF_INET` (`::` dan `0.0.0.0`).
- Mencegah error `ERR_CONNECTION_REFUSED` pada browser modern Windows yang memprioritaskan IPv6 `[::1]` untuk `localhost`.
- Menangani pemutusan socket mendadak tanpa crash (anti-`WinError 10053`).

### 6. 💻 Integrasi Native VS Code Extension
Dapat dijalankan langsung di dalam VS Code sebagai editor tab atau sidebar panel:
- Command: `Hermes: Open Visual Agent Desk` (Tampilan Utama)
- Command: `Hermes: Open 2D Pixel Office` (Membuka langsung di samping editor dengan `?view=2d`)
- Panel Webview terintegrasi di sidebar panel VS Code.

---

## 🚀 Cara Menjalankan

### Opsi A: Jalankan via Bridge Server (Rekomendasi)
Jalankan file batch:
```cmd
run_desk.bat
```
Atau via terminal:
```powershell
python bridge.py
```
Akses langsung di browser:
- **`http://localhost:8765`** atau **`http://127.0.0.1:8765`**
- Mode 2D langsung: **`http://localhost:8765/?view=2d`**

### Opsi B: Jalankan di dalam VS Code
1. Buka folder ini di VS Code: `code .`
2. Tekan `F5` untuk menjalankan Extension Development Host, atau jalankan perintah:
   - `Ctrl+Shift+P` -> Ketik `Hermes: Open Visual Agent Desk`
   - Tab visual desk akan terbuka berdampingan dengan kode Anda!

---

## 📁 Struktur Berkas

```
visual_agent_desk/
│
├── index.html          # Dual-View Web App (Dark IDE Theme, 3D Voxel + 2D Pixel Office)
├── bridge.py           # Dual-Stack HTTP Server, /state folding, micro/macro API
├── package.json        # Manifest VS Code Extension
├── extension.js        # Provider Webview Panel & Tab VS Code
├── run_desk.bat        # Windows Batch One-Click Launcher
├── run_desk.ps1        # PowerShell One-Click Launcher
├── README.md           # Dokumentasi teknis
│
└── data/               # Penyimpanan lokal
    ├── events.jsonl              # Stream event lifecycle Hermes
    ├── telemetry_history.jsonl   # Riwayat log aktivitas
    └── artifacts/                # Berkas output markdown yang dihasilkan agen
        └── manifest.json         # Indeks artefak tersimpan
```

---

*Dibuat untuk ekosistem CHARISNA SuperApp & Hermes Autonomous Workspace.*
