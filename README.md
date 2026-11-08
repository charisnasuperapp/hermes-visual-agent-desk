# 🎮 Hermes Pixel Office (v6.0) — Virtual Agent Workspace

> **Cockpit Virtual Retro 2D Pixel-Art untuk Agen AI Hermes: Mengusung arsitektur visual `app.pixeloffice.org`, kanvas HTML5 2D performa tinggi (<1% CPU), kontrol Smooth Pan & Zoom, 5 zona ruangan kantor interaktif, maskot kucing peliharaan (Mochi), mode pencahayaan atmosfer, sinkronisasi lembar kerja Hermes, serta efek audio 8-bit synthesizer murni.**

![Canvas 2D](https://img.shields.io/badge/Engine-HTML5_2D_Canvas-9b59b6?logo=html5&logoColor=white)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)
![Dual-Stack](https://img.shields.io/badge/Bridge-Dual--Stack_IPv6%2FIPv4-blue)
![VS Code Extension](https://img.shields.io/badge/VS_Code-Ready-007ACC?logo=visual-studio-code)
![Low CPU](https://img.shields.io/badge/CPU_Load-<1%25-success)

---

## 🌟 Fitur Unggulan v6.0

### 1. 🚀 Ringan & Bebas Beban CPU (< 1% CPU Load)
- Menggantikan sepenuhnya Three.js 3D WebGL dengan **HTML5 2D Canvas murni** berteknologi pixelated (`image-rendering: pixelated; crisp-edges`).
- Bebas dari lag, panas laptop, maupun pembekuan sistem.

### 2. 🔍 Kontrol Mulus Pan & Zoom (Smooth Camera Engine)
- **Mouse Wheel Zoom**: Zoom in dan zoom out fleksibel (**90% hingga 450%**) berpusat tepat di posisi kursor mouse.
- **Klik & Drag Pan**: Geser pandangan kantor ke segala arah secara instan.
- **Pintasan Cepat**: Tombol `[+]`, `[-]`, `[⊙ Reset 200%]`, dan `[Kantor]` di pojok kiri bawah.

### 3. 🏢 Denah Kantor Multi-Ruangan (Pixel Floorplan)
- 💻 **Workstation Dev Pods**: 5 meja kayu dengan kursi ergonomis, dual monitor menyala dinamis (terminal hijau berkedip, browsing biru, flicker cepat saat mengetik kode, dan redup saat rehat).
- ☕ **Break Room & Coffee Lounge**: Mesin espresso dengan animasi uap mengepul (`~♨~`), dispenser galon air bergelembung, mesin arcade retro "HERMES-88" berkedip, dan sofa santai beludru ungu.
- 📢 **Conference Boardroom**: Meja rapat besar dengan 6 kursi eksekutif dan papan tulis digital arsitektur sistem CHARISNA.
- 🗄️ **Server Vault**: Rak server data center berteknologi tinggi dengan lampu LED berkedip hijau, biru, dan amber.
- 🌸 **Teras Luar & Taman Sakura**: Jalur bebatuan taman, **pohon Sakura mekar dengan kelopak bunga merah muda melayang ditiup angin**, kolam ikan koi dengan riak air halus, lentera batu, serta **bangku taman kayu** tempat agen duduk menikmati udara segar.

### 4. 🐱 Maskot Kantor: Kucing Calico "Mochi"
- Kucing pixel interaktif yang berjalan-jalan di sekitar taman dan lounge atau tidur melingkar di bawah pohon sakura (`zzz`).
- **Bisa Dielus (Click to Pet)**: Memunculkan balon hati cinta `❤️`, mengeluarkan suara mengeong 8-bit, dan memberikan dorongan semangat tim (+15 Team Morale)!

### 5. 🌗 Pengubah Suasana & Pencahayaan Atmosfer
Tombol `[Suasana]` di header atas untuk berganti mode pencahayaan secara instan:
- 🌙 **Cyberpunk Night**: Langit bertabur bintang, pendaran lampu LED server, dan monitor menyala kontras.
- 🌅 **Golden Twilight (Senja)**: Pencahayaan keemasan hangat merayap di lantai kayu dan kelopak sakura.
- ☀️ **Studio Day (Siang)**: Nuansa retro studio terang dan jernih.

### 6. 🛋️ Interaktivitas Perabot (Interactive Furniture)
- **Klik Mesin Espresso**: Menyeduh kopi panas dengan suara brewing `☕`.
- **Klik Mesin Arcade**: Memainkan jingle retro 8-bit dan mencatat high score `🕹️`.
- **Klik Papan Tulis Rapat**: Membuka modal diagram arsitektur decoupled CHARISNA (Bumi Makmur POS, Homestay, Money Management, Core FTS5).
- **Klik Rak Server**: Memeriksa status kesehatan server dan latensi jaringan.

### 7. 🎯 Interaktivitas Mikro & Makro
- **Perintah Makro Seluruh Tim**:
  - 📢 **Rapat**: Memanggil seluruh agen berkumpul ke meja rapat.
  - ☕ **Rehat**: Mengarahkan seluruh agen santai ke lounge dan bangku taman.
  - ⚡ **Sprint**: Menugaskan semua agen kembali ke meja kerja untuk fokus coding intensif.
  - 🌳 **Bebas**: Membebaskan agen berjalan-jalan santai di area kantor dan taman.
- **Inspeksi Mikro Perorangan**:
  - Klik agen mana saja untuk membuka **Agent Dossier Modal**: menampilkan potret pixel animasi 4x, Level & XP progress bar (sistem rank RPG), status aktivitas, lokasi agen, serta kotak instruksi langsung.

### 8. 📑 Sinkronisasi Lembar Kerja (Hermes Worksheets Switcher)
- Bilah tab di header atas: `[A] Intelligence Memory`, `[B] AI Office Bridge`, `[C] Pixel Campus`, dan `[+] Baru`.
- Berpindah tab menyinkronkan tugas agen dan membuka editor markdown catatan kerja di laci geser samping.

### 9. 🎶 Efek Suara 8-Bit Synthesizer Murni
- Efek suara retro dihasilkan secara matematis menggunakan Web Audio API (square/triangle wave): suara blip tombol, langkah kaki, seduhan kopi, jingle arcade, meongan kucing, lonceng rapat, dan jingle kenaikan level. Tersedia tombol toggle **Mute/Unmute**.

---

## 🚀 Cara Menjalankan

### Opsi A: Jalankan via Skrip Otomatis
Cukup klik ganda file:
```cmd
run_desk.bat
```
atau via PowerShell:
```powershell
.\run_desk.ps1
```

Akses browser akan terbuka otomatis ke:
👉 **http://localhost:8765** (atau **http://127.0.0.1:8765**)

### Opsi B: Jalankan di dalam VS Code (Extension)
1. Buka folder ini di VS Code.
2. Tekan `F5` atau buka Command Palette (`Ctrl+Shift+P`).
3. Pilih:
   - `Hermes: Open 2D Pixel Office` (Membuka di panel editor samping).
   - Atau buka panel **Hermes Desk** di bilah sisi.

---

## 🏗️ Struktur Proyek

```
visual_agent_desk/
├── bridge.py           # Dual-Stack IPv6/IPv4 HTTP Bridge & Life-Cycle Simulator
├── index.html          # HTML5 2D Canvas Engine, Pixel Art Tilemap & UI Overlays
├── extension.js        # Integrasi VS Code Extension Webview Provider
├── package.json        # Manifest VS Code Extension
├── run_desk.bat        # Windows Batch Launcher
├── run_desk.ps1        # PowerShell Runner
├── README.md           # Dokumentasi Resmi Proyek
└── data/
    ├── events.jsonl    # Event log stream agen
    ├── worksheets.json # Database sinkronisasi lembar kerja
    └── artifacts/      # Dokumen markdown artefak yang diexport
```
