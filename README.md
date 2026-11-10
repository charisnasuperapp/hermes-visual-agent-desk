# Hermes Pixel Office

Kantor pixel 2D untuk melihat aktivitas Hermes dan tim agen dalam satu layar. Peta dapat digeser dengan drag kiri dan diperbesar dengan roda mouse. Hermes tampil sebagai kucing yang bergerak otomatis mengikuti status dari backend; klik lantai tidak mengendalikannya.

## Menjalankan

1. Pasang Python 3.10 atau lebih baru.
2. Jalankan `pip install -r backend/requirements.txt`.
3. Jalankan `python backend/app.py`.
4. Buka `http://127.0.0.1:19000/`.

Backend memakai Flask dan Pillow. Frontend memakai Phaser lokal di `frontend/vendor`; tidak perlu layanan CDN untuk kantor utama. Port bawaan 19000. Periksa pengaturan firewall sebelum membuka layanan ke jaringan.

## Kontrol kantor

| Aksi | Hasil |
| --- | --- |
| Drag kiri pada peta | Geser kamera saat peta diperbesar |
| Roda mouse | Zoom peta |
| Tab ruangan | Sorot bagian kantor |
| Klik agen | Tampilkan dialog status yang dapat dibaca |
| Klik furnitur aktif | Lihat fungsi meja, pantry, server, dan ruang rapat |
| Istirahat Santai | Tim menuju pantry atau pod tidur |
| Kembali ke Pos | Tim kembali ke stasiun kerja |

Hermes utama mengikuti status watcher `agent.log` jika log tersedia. Bila tidak ada aktivitas log, backend memakai status tersimpan. Agen pendamping mempunyai animasi kantor dan data registri; tampilan mereka bukan bukti sambungan langsung ke Bumi Makmur POS, Homestay, atau MoniFlow. Kartu sumber data menampilkan status menunggu sampai integrasi sumber disediakan.

Rute agen dikalibrasi untuk peta bawaan. Saat gambar latar diganti, gerak otomatis dibatasi sampai jalur peta baru dikalibrasi. Hal ini mencegah karakter menembus dinding pada gambar yang belum dikenali.

## Integrasi dan API

| Endpoint | Fungsi |
| --- | --- |
| `GET /health` | Pemeriksaan layanan |
| `GET /status` | Status Hermes dan kantor |
| `GET /agents` | Registri agen |
| `POST /set_state` | Kirim status Hermes dari proses tepercaya |
| `GET /yesterday-memo` | Memo harian tersedia |

Contoh: `python set_state.py writing "Meninjau kode"`. Endpoint status disediakan untuk integrasi lokal. Antarmuka kantor tidak menampilkan tombol untuk mengendalikan Hermes secara manual.

## Struktur utama

- `backend/app.py`: server, status, watcher log, dan API.
- `frontend/index.html`: kantor dan dashboard.
- `frontend/office_navigation.js`: jalur agen, pintu, dan penghalang furnitur.
- `frontend/office_bg_small.webp`: peta bawaan.
- `agents-state.json`, `state.json`, `memo.json`: data lokal; jangan masukkan data pribadi ke commit.

## Lisensi

Kode berlisensi MIT. Aset gambar dalam repositori hanya untuk penggunaan nonkomersial. Karakter tamu menggunakan aset LimeZu; lihat [LICENSE](LICENSE) untuk syarat lengkap dan atribusi.
