# OSINT Search by Name — Panduan

Ini adalah panduan singkat (Bahasa Indonesia) untuk menggunakan `osintupdate.py`. Script ini membuka pencarian Google untuk nama target dan (opsional) membuka beberapa pencarian site-specific untuk jejaring sosial. Script juga menyediakan opsi "auto-click" yang, jika diaktifkan, akan mencoba mengklik hasil pencarian teratas menggunakan Selenium.

---

## Persyaratan

- Python 3.8+ terpasang di sistem (direkomendasikan 3.10+).
- Google Chrome terpasang (untuk metode Selenium Chrome).
- Koneksi internet (untuk membuka Google dan mengunduh driver jika perlu).

## File penting

- `osintupdate.py` — script utama (terletak di folder ini).
- `requirements.txt` — daftar paket Python yang disarankan.

## Instalasi dependensi (direkomendasikan menggunakan virtual environment)

Buka terminal (Linux / macOS / WSL) dan jalankan (gunakan python3):

```bash
cd ~/Downloads
python3 -m venv .venv
source .venv/bin/activate    # Linux / macOS / WSL
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Catatan Windows: jika Anda menggunakan Git Bash atau PowerShell, gunakan langkah aktivasi venv sesuai platform (lihat bagian "Mengunggah ke GitHub dan menggunakan di perangkat lain"). Alternatif singkat (tanpa virtualenv):

```bash
python3 -m pip install --user -r requirements.txt
```

## Cara menjalankan

Jalankan script dengan Python 3 di terminal (Linux / macOS / WSL):

```bash
cd ~/Downloads
python3 osintupdate.py
```

Di Windows gunakan `python` atau environment yang sesuai jika Python 3 sudah menjadi default.

Script akan menampilkan beberapa prompt interaktif:

- Masukkan nama target.
- Tanyakan apakah ingin membuka pencarian akun sosial media juga (Y/n).
- Tanyakan apakah mengaktifkan auto-click hasil pencarian teratas (y/N). Jika memilih ya, pilih metode (saat ini hanya `selenium`).

Jika memilih auto-click dan Selenium tersedia, script akan membuka Chrome (melalui selenium + webdriver-manager) dan mencoba mengklik hasil pencarian teratas.

## Opsi dan perilaku

- open_social_tabs: membuka tab Google untuk situs-situs sosial (Facebook, Instagram, Twitter, LinkedIn, dll.).
- auto-click: jika aktif, script akan membuka ulang (via Selenium) halaman hasil pencarian Google dan mencoba klik elemen hasil (berdasarkan tag `h3` -> parent `<a>`).
- headless: tidak tersedia via prompt interaktif saat ini, tapi fungsi Selenium menerima argumen `headless` (default False) jika Anda ingin memanggil fungsi langsung dari kode.

## Troubleshooting

- Jika Anda melihat pesan `Selenium atau webdriver_manager tidak ditemukan`, jalankan:

```bash
python -m pip install selenium webdriver-manager
```

- Jika WebDriver gagal dijalankan, pastikan:

  - Chrome terpasang dan versi Chrome kompatibel dengan driver yang diunduh (webdriver-manager biasanya mengunduh yang cocok).
  - Anda memiliki izin untuk mengunduh dan menjalankan driver.

- Jika auto-click gagal menemukan elemen yang dapat diklik:
  - Struktur HTML hasil Google dapat berubah (ads, featured snippets). Saat ini script mencari tag `h3` dan klik parent `<a>` pertama yang clickable.
  - Anda bisa memperbesar `timeout` di fungsi `auto_click_top_result_with_selenium` atau menambahkan log debugging.

## Keamanan & etika

- Jangan melakukan scraping/akses berlebihan ke Google atau situs lain. Gunakan script ini secara bertanggung jawab.
- Otomasi klik pada halaman hasil mesin pencari dapat dianggap aktivitas agresif jika dilakukan dalam skala besar.

## Langkah lanjut (opsional)

- Menambah mode non-interaktif (CLI) menggunakan `argparse`.
- Menambah fallback GUI automation (mis. pyautogui) jika Anda membuka browser manual.
- Menambah logging, sleep jitter, dan pembatasan frekuensi untuk mengurangi kemungkinan terdeteksi oleh proteksi bot.

---

Jika Anda mau, saya bisa: menambahkan opsi CLI sekarang, menambahkan pyautogui fallback, atau membuat skrip uji cepat untuk memverifikasi auto-click di mesin Anda. Mana yang ingin Anda saya lanjutkan?

## Mengunggah ke GitHub dan menggunakan di perangkat lain

Panduan singkat ini menjelaskan langkah yang umum dipakai untuk mengunggah project ke GitHub dari mesin Anda sekarang dan cara meng-clone serta men-setup di perangkat lain.

1. Buat repository di GitHub

- Masuk ke https://github.com dan buat repository baru (pilih Public atau Private sesuai kebutuhan). Catat URL repository (mis. `https://github.com/username/osint-search.git`).

2. Inisialisasi git di folder lokal dan push
   Buka terminal di folder `~/Downloads` (Linux/macOS/WSL) atau folder Downloads pengguna di Windows, lalu jalankan:

```bash
cd ~/Downloads
git init
git add osintupdate.py README.md requirements.txt
echo ".venv/" > .gitignore
git add .gitignore
git commit -m "Initial commit: osint search script + README"
git branch -M main
git remote add origin <URL_REPO_GITHUB>
git push -u origin main
```

Ganti `<URL_REPO_GITHUB>` dengan URL repo yang Anda buat.

3. Clone dan setup di perangkat lain

- Di perangkat lain, clone repository:

```bash
git clone https://github.com/username/osint-search.git
cd osint-search
```

-- Buat virtual environment dan install dependensi (Linux/macOS/WSL menggunakan python3):

```bash
python3 -m venv .venv
source .venv/bin/activate    # Linux / macOS / WSL
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Windows CMD: .venv\Scripts\activate.bat
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

4. Menjalankan script di perangkat lain

- Jalankan dengan (Linux/macOS/WSL):

```bash
python3 osintupdate.py
```

Jika di Windows, jalankan `python osintupdate.py` sesuai environment.

- Pastikan Google Chrome sudah terpasang di perangkat tersebut jika Anda berniat menggunakan metode `selenium`.

5. Catatan tentang credential & keamanan

- Jangan commit file yang berisi kredensial atau file environment lokal (mis. `.env` atau file konfigurasi pribadi). Tambahkan mereka ke `.gitignore`.
- Jika Anda menggunakan repository public, pertimbangkan untuk tidak menyertakan data sensitif di dalam commit.

6. Tips untuk menjaga kompatibilitas lintas perangkat

- Sertakan `requirements.txt` yang diperbarui bila Anda menambah dependensi baru.
- Pertimbangkan menambahkan `pyproject.toml` atau `Pipfile` jika ingin mengelola dependency lebih ketat.
- Jika memakai Windows di beberapa mesin, gunakan instruksi aktivasi venv khusus Windows di README.

Jika Anda mau, saya bisa otomatis membuat file `.gitignore` yang lebih lengkap (mengabaikan venv, **pycache**, .vscode, dsb.) dan menambahkan instruksi CI sederhana (GitHub Actions) untuk menjalankan tests atau lint pada push.
