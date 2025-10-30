# 🤖 AI Personal Finance Tracker (A-PFT)

## Deskripsi Proyek

**AI Personal Finance Tracker (A-PFT)** adalah aplikasi berbasis konsol Python yang dirancang untuk membantu pengguna melacak, menganalisis, dan mengelola keuangan pribadi mereka secara cerdas.

Berbeda dari aplikasi pelacak keuangan konvensional, A-PFT menyertakan modul kecerdasan buatan (*AI-powered*) yang ditenagai oleh Gemini API (simulasi) untuk memberikan wawasan dan rekomendasi keuangan yang lebih mendalam dan personal. Selain itu, antarmuka konsol telah ditingkatkan dengan kode warna ANSI untuk pengalaman pengguna (UX) yang lebih menarik dan informatif, memudahkan pembacaan data penting.

## Fitur Unggulan

* **Pencatatan Transaksi Cepat:** Mencatat pemasukan dan pengeluaran dengan kategori, nominal, tanggal, dan catatan.
* **Ringkasan Keuangan Instan:** Melihat saldo saat ini dan *breakdown* visual (menggunakan bar grafik) dari pengeluaran berdasarkan kategori.
* **Analisis Kebiasaan:** Menganalisis kebiasaan pengeluaran, menghitung rata-rata harian, dan mendeteksi tren pengeluaran (Naik, Turun, Stabil).
* **Prediksi Akhir Bulan:** Memprediksi total pengeluaran dan saldo akhir bulan berdasarkan rata-rata pengeluaran harian yang tercatat.
* **Saran Penghematan:** Memberikan saran yang ditargetkan untuk penghematan berdasarkan kategori pengeluaran terbesar atau mingguan yang fluktuatif.
* **⭐ Analisis AI (Gemini Powered):** Fitur utama yang menggunakan data ringkasan keuangan untuk menghasilkan interpretasi kondisi finansial, memberikan diagnosis kesehatan keuangan, dan saran strategis yang lebih holistik.
* **✨ Tampilan Konsol Interaktif:** Menggunakan kode warna ANSI (Hijau, Merah, Kuning) untuk memvisualisasikan status keuangan secara instan (misalnya: Saldo positif/negatif, Pengeluaran tertinggi, Tren risiko).

## Struktur Proyek

Proyek ini terbagi menjadi beberapa modul Python yang terstruktur:

| File | Deskripsi |
| :--- | :--- |
| `main.py` | Modul utama yang menjalankan menu aplikasi dan mengontrol alur program. |
| `modules/utils.py` | Berisi fungsi utilitas dasar, manajemen file JSON, pemformatan mata uang, dan definisi **kode warna ANSI** (untuk UX yang lebih baik). |
| `modules/summary.py` | Menangani fungsi penambahan transaksi, menampilkan ringkasan, dan daftar semua transaksi. |
| `modules/analyze.py` | Berisi fungsi analisis kebiasaan pengeluaran dan prediksi saldo akhir bulan. |
| `modules/suggest.py` | Menghasilkan saran penghematan berdasarkan statistik pengeluaran. |
| `modules/ai_analyze.py` | Modul baru yang mengambil data ringkasan dan memanggil **Gemini API (simulasi)** untuk analisis keuangan mendalam. |

## Persyaratan (Prasyarat)

Untuk menjalankan proyek ini secara penuh (dengan integrasi Gemini API yang sesungguhnya):

1.  **Python 3.x**
2.  **Library (untuk Gemini API):**
    ```bash
    pip install google-genai
    ```
3.  **Kunci API Gemini:** Anda harus memiliki kunci API Gemini yang valid. Kunci ini harus diatur di dalam `modules/ai_analyze.py` untuk mengaktifkan fitur analisis AI secara nyata.
