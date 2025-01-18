# PENGEMBANGAN SISTEM PENCARIAN RESEP MASAKAN INDONESIA MENGGUNAKAN METODE BM25 DAN FASTTEXT
Proyek ini bertujuan mengembangkan search engine untuk membantu pengguna menemukan resep masakan Indonesia berdasarkan bahan yang mereka miliki.
Aplikasi berbasis Streamlit ini menggunakan algoritma BM25 untuk mencari resep masakan Indonesia yang paling relevan berdasarkan kata kunci yang dimasukkan.
## Fitur
Pencarian Resep: Cari resep masakan Indonesia menggunakan kata kunci seperti "ayam", "kambing", "udang", dan lainnya.
Rekomendasi Teratas: Aplikasi akan menampilkan 10 resep terbaik sesuai dengan kata kunci yang dimasukkan.
Detail Resep: Klik pada nama resep untuk melihat bahan-bahan dan langkah-langkah memasaknya.
## Dataset
Dataset yang digunakan terdiri dari beberapa file CSV yang berisi resep masakan dari berbagai bahan seperti ayam, kambing, telur, dan udang.
Setiap resep memiliki informasi seperti Tittle (judul), Ingredients (bahan-bahan), Steps(langkah-langkah pembuatan), dan Loves (jumlah likes). 
## Cara Menjalankan
1. Pastikan semua dependensi diinstal dengan menjalankan pip install -r requirements.txt
2. Jalankan aplikasi Streamlit: streamlit run app.py
3. Buka aplikasi di browser: Aplikasi akan berjalan di http://localhost:8501
## Cara penggunaan 
1. Ketikkan kata kunci di kolom pencarian (contoh: "udang")
2. Lihat daftar rekomendasi Top 10 yang relevan
3. Klik pada nama resep untuk mengetahui bahan-bahan dan cara memasaknya
