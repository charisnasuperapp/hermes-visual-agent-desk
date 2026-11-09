# RANGKUMAN KORPUS PENGETAHUAN & INTEGRASI MASTER: CHARISNA ECOSYSTEM & HERMES AGENT

> **Dokumen Pembelajaran Hermes Agent (Machine-Readable & Human-Readable Knowledge Base)**  
> **Target Subjek**: Hermes Agent (`NousResearchInc.HermesAgent` / Hermes CLI / Hermes Core Engine)  
> **Pemilik & Arsitek Utama**: Raja (ZENNITH)  
> **Penyusun**: Antigravity AI Systems Architect  
> **Tanggal Kompilasi**: 9 November 2026  
> **Status**: Terverifikasi & Aktif (Canonical Memory Source)

---

## 1. PROFIL PENGGUNA & LINGKUNGAN KERJA (OPERATING ENVIRONMENT)

- **Identitas Pemilik**: Pengguna dipanggil dengan sapaan hormat **"Raja"** (boss). Seluruh komunikasi, eksekusi perintah, dan konfirmasi harus menghormati arahan strategis beliau.
- **Identitas Mesin**:
  - Windows PC (`zenn-pc-turbo-eclipse`), OS Windows 11 64-bit.
  - Python Environment: Python 3.14.9 & Runtime Hermes (`AppData/Local/hermes`).
  - Node.js Environment: Node v24.22.1.
  - Version Control: Git + GitHub CLI (`gh`) terotentikasi sebagai `charisnasuperapp`.
- **Aturan Batas Wilayah (Isolation Boundary)**:
  - Bekerja secara eksklusif pada PC Windows ini.
  - Instalasi Hermes milik Raja di laptop lain terpisah dan **tidak boleh disentuh**.

---

## 2. ARSITEKTUR UTAMA: CHARISNA SUPERAPP & MULTI-BUSINESS ECOSYSTEM

### Prinsip 1: Satukan Wawasan, Bukan Seluruh Database (*"Unify Insights, Not All Databases"*)
CHARISNA SuperApp bertindak sebagai panel kendali eksekutif dan penyatu keputusan/KPI. Sistem **TIDAK PERNAH** memaksakan seluruh database independen untuk digabung ke dalam satu skema monolitik.

### Prinsip 2: Pemegang Otoritas Data (*Authoritative Source of Truth*)
Setiap unit bisnis independen memegang otoritas mutlak atas datanya sendiri:
1. **Bumi Makmur POS** (Firebase): Otoritas mutlak untuk transaksi penjualan kasir, katalog produk, dan stok fisik toko.
2. **CHARISNA Homestay / Kost**: Otoritas mutlak untuk unit kamar, penyewa, masa sewa, dan status okupansi.
3. **CHARISNA Money Management / MoniFlow**: Otoritas mutlak untuk pembukuan pribadi dan kas keluarga.
4. **Piola / MySalary**: Otoritas mutlak untuk penggajian dan manajemen upah.
5. **CHARISNA Core / SuperApp**: Menyimpan ringkasan harian (*daily rollups*), data agregasi ternormalisasi, dan buku besar audit (*audit ledger*) dengan *data provenance* lengkap (sumber, waktu, hash transaksi).

### Prinsip 3: Disiplin Batas Free-Tier (*No Breaking Free-Tier Limits*)
- Dilarang keras memaksa atau memicu peningkatan kuota berbayar (seperti Firebase Blaze) tanpa persetujuan eksplisit dari Raja.
- Arsitektur berbasis *read-only connector*, *batch sync*, dan pemanfaatan penyimpanan lokal/Cloudflare Free Tier.

### Prinsip 4: Arsitektur Hybrid Storage
- **Hot / Live Cache**: `C:\Users\ZENNITH\AppData\Local\hermes` (database state lokal, FTS5 index, logs).
- **Arsip & Knowledge Base**: `I:\My Drive\Charisna SuperApp\Hermes\` dan `Shared-Knowledge\` (Google Drive ter-mount).

---

## 3. EVOLUSI & IMPLEMENTASI VISUAL AGENT DESK (STAR OFFICE UI)

Perjalanan desain antarmuka visual agen melewati beberapa fase penting yang mencerminkan preferensi dan kebutuhan interaksi Raja:

### Tahap 1: Iterasi 3D Voxel (Ditinggalkan)
- *Awal*: Dibangun menggunakan Three.js bergaya voxel taman 3D.
- *Evaluasi Raja*: "Terkesan kuno, kotak-kotak, kurang bagus, tidak bisa zoom in/out, harus ada orangnya jalan-jalan / duduk di bangku taman, kerja kembali ke tempat kerjanya, lembar kerja di hermes sync kan".
- *Pelajaran*: Raja menginginkan estetika pixel art retro yang hidup, luwes, memiliki interaktivitas mikro & makro, serta tersinkronisasi dua arah dengan aktivitas nyata Hermes.

### Tahap 2: Reverse Engineering Hermes Gateway & Desktop Cockpit
- Berhasil mengidentifikasi infrastruktur lokal Hermes:
  - Gateway FastAPI aktif di `http://127.0.0.1:11188/`.
  - Database state SQLite di `C:\Users\ZENNITH\AppData\Local\hermes\state.db`.
  - Maskot sudut kanan bawah aplikasi desktop Hermes: **Boxcat** (`AppData/Local/hermes/pets/boxcat/` dan `.thumbs/boxcat.png`).
- Direplikasi menjadi dashboard dual cockpit: Star Office 2D Canvas di atas + Hermes Message Console di bawah ("What's next?").

### Tahap 3: Implementasi Bersih Star-Office-UI Resmi (`ringhyacinth/Star-Office-UI`)
Sesuai instruksi terakhir Raja (*"hapus bersih, ganti ini https://github.com/ringhyacinth/Star-Office-UI"*), repositori `visual_agent_desk` dibersihkan total dan digantikan oleh `ringhyacinth/Star-Office-UI`:
- **Teknologi**:
  - Frontend: Phaser 3.80.1 HTML5 Canvas, animasi sprite grid WebP, font ArkPixel, layout responsive.
  - Backend: Flask Service di `backend/app.py`, port default `19000` (`http://127.0.0.1:19000`).
  - Repositori Git: `https://github.com/charisnasuperapp/hermes-visual-agent-desk.git`.
- **Mesin Finite State Machine (FSM) Agen**:
  | Status Agen | Lokasi di Kantor | Deskripsi Visual |
  | :--- | :--- | :--- |
  | `idle` | `breakroom` | Santai di sofa ruang istirahat, menunggu tugas |
  | `writing` | `writing` (meja kerja) | Duduk di meja kerja utama, mengetik kode/dokumen |
  | `researching` | `writing` / ruang dokumen | Menelusuri informasi, membaca berkas, browsing |
  | `executing` | `writing` (workstation) | Menjalankan perintah terminal atau skrip |
  | `syncing` | `writing` | Animasi sinkronisasi data/backup |
  | `error` | `error` (ruang server) | Menginspeksi bug di area server room |
- **Skrip Kontrol & Sinkronisasi**:
  - `set_state.py <state> "<detail>"`: Memperbarui `state.json` secara instan.
  - `hermes_sync.py`: Daemon pengawas `state.db` Hermes yang otomatis memicu perubahan status Star Office saat Hermes sedang bekerja atau istirahat.
  - `run_star_office.bat` & `run_star_office.ps1`: Skrip peluncuran instan di Windows.

---

## 4. PENGETAHUAN TEKNIS MENDALAM: HERMES INTERNALS DI WINDOWS

Hermes harus memahami lingkungan kerjanya sendiri agar tidak mengalami kendala saat eksekusi:

### 1. Higienitas Database SQLite (`state.db`)
- `state.db` di `AppData/Local/hermes/` beroperasi dalam mode WAL (*Write-Ahead Logging*).
- **Aturan Mutlak**: Semua proses pembaca eksternal harus selalu menyambung dengan URI Read-Only:
  ```python
  sqlite3.connect(f"file:{HERMES_STATE_DB}?mode=ro", uri=True)
  ```
  Ini mencegah terjadinya *database is locked* atau konflik transaksi dengan Electron desktop Hermes.

### 2. Standar Output & Enkoding UTF-8 Windows
- Secara default, terminal PowerShell/CMD pada Windows menggunakan codepage `cp1252` atau `cp437`.
- Jika mencetak karakter non-ASCII (emoji, karakter Mandarin, simbol Boxcat), terminal akan *crash* dengan `UnicodeEncodeError`.
- **Solusi Wajib**: Di setiap script Python, selalu sertakan rekonfigurasi UTF-8:
  ```python
  import sys
  if hasattr(sys.stdout, 'reconfigure'):
      try:
          sys.stdout.reconfigure(encoding='utf-8')
      except Exception:
          pass
  ```

### 3. Eksekusi Shell di Windows PowerShell
- Karakter petik ganda (`"`) sering kali di-*strip* atau dipotong oleh parser PowerShell jika disisipkan dalam satu baris perintah `python -c "..."`.
- **Solusi**: Gunakan file script mandiri (*scratch script*), atau gunakan perintah PowerShell native (`Get-Content`, `Set-Content -NoNewline`).
- Perhatikan perbedaan *line endings*: File yang di-checkout di Windows memiliki CRLF (`\r\n`), sehingga operasi patch teks harus memperhitungkan format newline yang konsisten.

### 4. Aturan Dua Kali Gagal (*Two-Failure Rule*)
- Jika suatu pendekatan gagal 2 kali berturut-turut, **STOP mengulang cara yang sama**.
- Lakukan inspeksi akar penyebab (*permissions, path, ports, locks, syntax, encodings*) dan ubah strategi.

---

## 5. REKAPITULASI STATUS LAYANAN & URL AKTIF

| Layanan / Modul | URL / Lokasi | Status & Port | Catatan |
| :--- | :--- | :--- | :--- |
| **Star Office UI** | `http://127.0.0.1:19000` | Aktif (Port 19000) | Dashboard visual agen pixel art resmi |
| **Hermes Gateway** | `http://127.0.0.1:11188` | Aktif (Port 11188) | Backend resmi Hermes Agent Desktop |
| **Hermes Desktop App** | WindowsApps `NousResearchInc.HermesAgent` | Aktif | Antarmuka desktop Electron Raja |
| **CHARISNA SuperApp** | `https://zen.charisna-superapp.workers.dev` | Live | Cloudflare Worker produksi |
| **zennAI** | `https://khusus-jomblo.vercel.app` | Live | Vercel deployment (cocoyiyi88/zennAI) |
| **Git Repositori Visual** | `charisnasuperapp/hermes-visual-agent-desk` | Pushed (Commit `fdfce97`) | Repositori Star-Office-UI |

---

## 6. PROTOKOL OPERASIONAL BAGI HERMES UNTUK BEKERJA SECARA CERDAS

Saat Hermes menerima tugas dari Raja, ikuti alur kerja disiplin berikut:
1. **Perbarui Status Kantor Sebelum Mulai**:
   - Panggil `python set_state.py writing "Mengerjakan: <nama tugas>"` agar karakter visual di Star Office berjalan ke meja kerja dan mengetik.
2. **Jika Melakukan Pencarian / Analisis Data**:
   - Panggil `python set_state.py researching "Menganalisis berkas / referensi"`.
3. **Jika Terjadi Kendala / Error**:
   - Panggil `python set_state.py error "Investigasi: <deskripsi error>"`.
4. **Setelah Tugas Selesai**:
   - Panggil `python set_state.py idle "Standby & siap bertugas"` agar karakter kembali ke sofa ruang istirahat.
5. **Selalu Jaga Integritas Data**:
   - Pertahankan komentar kode dan struktur yang ada.
   - Jangan pernah menghapus file tanpa konfirmasi kecuali diperintahkan secara eksplisit (*"hapus bersih"*).
   - Catat bukti verifikasi sebelum menyatakan tugas selesai.

---
*Dokumen ini dirancang untuk dapat diakses kapan saja oleh Hermes melalui pembacaan berkas atau injeksi memori sistem.*
