# Hermes Agent-Pixels for CHARISNA

Kantor agen ini memakai [Agent-Pixels](https://github.com/gcampton/Agent-Pixels) resmi sebagai plugin [Paperclip](https://github.com/paperclipai/paperclip). Repo ini berisi panduan integrasi Hermes dan launcher lokal. Aset serta kode Agent-Pixels tetap berasal dari upstream; repo ini tidak mendistribusikannya ulang.

## Status integrasi

Diuji di Windows pada 11 November 2026 dengan Paperclip `2026.1106.0`, Agent-Pixels `0.1.0` (dibangun ulang terhadap SDK Paperclip saat ini), dan Hermes Agent `v0.22.6`.

- Paperclip lokal: `http://127.0.0.1:3100`
- Kantor: `http://127.0.0.1:3100/CHA/agent-pixels`
- Agen Hermes: adapter `hermes_local`, uji lingkungan **pass**, status **ready**.
- Agent-Pixels membaca status agen dari Paperclip. Tugas tes memicu Hermes CLI dan menampilkan status `running` serta gerak agen di kantor.

**Batas sinkronisasi:** sesi Hermes yang berjalan di luar Paperclip tidak otomatis masuk ke Agent-Pixels. Adapter `hermes_local` menjalankan Hermes CLI pada tugas Paperclip, memakai instalasi dan konfigurasi Hermes lokal. Integrasi ke percakapan Hermes eksternal membutuhkan API/event bridge tambahan.

## Menjalankan

Jalankan `run_agent_pixels.ps1` di PowerShell. Launcher membuka Paperclip pada loopback dan memakai data lokal yang sudah disiapkan. Setelah server siap, buka alamat kantor di atas. Data Paperclip berada di profil pengguna, bukan repo ini.

## Pemasangan baru

1. Pasang Node.js 22+ dan Hermes CLI. Pastikan `hermes --version` berhasil.
2. Jalankan `npx --yes --registry https://registry.npmjs.org paperclipai onboard --yes --bind loopback --no-install-service`.
3. Pasang plugin dari [rilis Agent-Pixels](https://github.com/gcampton/Agent-Pixels/releases) dengan `npx paperclipai plugin install --local <folder-ekstraksi>`. Bila rilis tidak kompatibel dengan SDK Paperclip terbaru, bangun dari [sumber upstream](https://github.com/gcampton/Agent-Pixels) terhadap SDK versi Paperclip terpasang. Jangan menyalin aset upstream ke repo ini tanpa izin lisensi yang jelas.
4. Buat agen Paperclip dengan adapter `hermes_local`. Set `hermesCommand` ke path penuh `hermes.exe`. Jalankan **Test Environment** hingga lulus, lalu selesaikan setup agen.
5. Buka menu **Agent Pixels** dan jalankan tugas Paperclip untuk melihat perubahan aktivitas.

Pada Windows, tes adapter mencari `python3` dalam `PATH` dan kunci model pada `~/.hermes/.env`. Instalasi Hermes tertentu menyimpan `.env` di `%LOCALAPPDATA%\hermes\.env`. Gunakan tautan simbolik atau secret store Paperclip agar tidak menggandakan kunci. Jangan commit `.env`, token, sesi, atau data pribadi.

## Keamanan dan cakupan

Paperclip berjalan pada `127.0.0.1` (loopback). Launcher tidak membuka layanan ke jaringan. Repo lama tersimpan dalam riwayat Git; konfigurasi dan data lokal diabaikan Git. Untuk fitur, bug, dan lisensi Agent-Pixels, lihat upstream.
