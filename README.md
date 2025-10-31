# 🤖 AI Personal Finance Tracker (A-PFT)

## Ketentuan Teknis
* Karya ini orisinal dan buatan sendiri.
* Menggunakan library eksternal (`google-genai`, `python-dotenv`) yang relevan untuk fitur AI dan keamanan API.
* Repositori ini berisi seluruh source code dan file pendukung.

---

## Judul dan Deskripsi Singkat Karya

**AI Personal Finance Tracker (A-PFT)** adalah aplikasi pelacak keuangan pribadi berbasis konsol Python. Aplikasi ini membantu pengguna mencatat, meringkas, dan menganalisis kebiasaan finansial mereka. Fitur utamanya adalah integrasi **Gemini API** (mode simulasi aktif jika kunci tidak tersedia) yang memberikan analisis dan saran mendalam mengenai kesehatan keuangan pengguna. Antarmuka konsol ditingkatkan secara signifikan dengan kode warna ANSI untuk memudahkan pembacaan dan pemahaman data secara cepat.

## Cara Menjalankan/Mengakses Karya Tersebut

### Prasyarat
1.  **Python 3.x** terinstal.
2.  Akses ke Terminal/Command Prompt.

### Langkah-langkah Instalasi
1.  **Clone Repositori** (Asumsi proyek Anda sudah di repositori):
    ```bash
    git clone https://github.com/rapirawr/Finance-Tracker-with-AI-intergration.git
    cd Finance-Tracker-with-AI-intergration
    ```
2.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Konfigurasi API Key (Opsional untuk fitur AI nyata):**
    * Buat file bernama `.env` di direktori utama proyek.
    * Tambahkan kunci API Gemini Anda di dalam file tersebut:
        ```
        GEMINI_API_KEY="AIzaSy...KunciAndaDiSini...U"
        ```
    * *(Jika file `.env` tidak dibuat, fitur AI akan berjalan dalam mode simulasi)*.
4.  **Jalankan Aplikasi:**
    ```bash
    python main.py
    ```

### Cara Mengakses
Aplikasi akan menampilkan menu berbasis angka (1-8). Pilih angka yang sesuai, misalnya `7` untuk mendapatkan Analisis Keuangan dari AI.

## Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python
* **Pustaka Utama:**
    * `google-genai` (Untuk fitur AI dan analisis data)
    * `python-dotenv` (Untuk mengamankan dan menyembunyikan kunci API)
    * `datetime`, `json`, `os`, `statistics` (Pustaka standar Python)
* **Antarmuka:** Konsol/Terminal dengan kode warna ANSI.
