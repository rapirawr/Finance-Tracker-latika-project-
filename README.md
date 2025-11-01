# 🤖 AI Personal Finance Tracker (A-PFT)

Aplikasi pelacak keuangan pribadi berbasis konsol Python yang terintegrasi dengan Gemini AI untuk analisis keuangan mendalam.

## 🌟 Fitur Utama

* **Pencatatan Transaksi:** Mencatat pemasukan dan pengeluaran harian.
* **Ringkasan Cepat:** Menyajikan total saldo dan pengeluaran per kategori.
* **Analisis AI:** Integrasi Gemini API untuk mendapatkan ringkasan keuangan dan saran spesifik yang **Gen Z *Vibe*** (menggunakan kode warna ANSI untuk tampilan terminal yang lebih baik).
* **Keamanan:** Menggunakan `python-dotenv` untuk mengelola Kunci API.
* **Mode Simulasi:** Jika Kunci API Gemini tidak tersedia, analisis akan otomatis berjalan dalam mode simulasi.

---

## 🛠️ Ketentuan Teknis dan Teknologi

| Teknologi | Keterangan |
| :--- | :--- |
| **Bahasa** | Python 3.x |
| **AI/API** | `google-genai` (Gemini 2.5 Flash Model) |
| **Keamanan** | `python-dotenv` |
| **Antarmuka** | Konsol/Terminal dengan Kode Warna ANSI |
| **Cacing (*Caching*)** | Menggunakan `__pycache__` untuk mempercepat waktu *loading* modul. |

---

## 🚀 Cara Menjalankan Aplikasi

### Prasyarat

Pastikan Anda telah menginstal:
1.  **Python 3.x**
2.  Akses ke Terminal/Command Prompt.

### Langkah-langkah Instalasi

1.  **Clone Repositori:**
    ```bash
    git clone [https://github.com/rapirawr/Finance-Tracker-with-AI-intergration.git](https://github.com/rapirawr/Finance-Tracker-with-AI-intergration.git)
    cd Finance-Tracker-with-AI-intergration
    ```

2.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    *Jika Anda tidak memiliki Kunci API, aplikasi akan tetap berjalan dalam mode simulasi.*

3.  **Jalankan Aplikasi:**
    ```bash
    python main.py
    ```

### Cara Mengakses
Setelah dijalankan, aplikasi akan menampilkan menu utama berbasis angka (1-8). Pilih angka yang sesuai, misalnya:
* `1` untuk Menambah Transaksi.
* `7` untuk mendapatkan **Analisis Keuangan AI**.

---

## 💾 Kegunaan Caching (`__pycache__`)

Ketika modul aplikasi diimpor (seperti `.utils` atau `.summary`), Python secara otomatis menghasilkan *folder* `__pycache__` yang berisi *bytecode* terkompilasi (`.pyc` files).

* **Manfaat:** Ini mempercepat *waktu loading* aplikasi pada eksekusi berikutnya, karena Python dapat melewati langkah kompilasi dari kode sumber dan langsung menjalankan *bytecode* yang sudah siap.
