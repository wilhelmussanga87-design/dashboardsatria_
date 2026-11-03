# SATRIA — HTML siap hosting DomaiNesia

## Berkas yang digunakan

- **SATRIA-DomaiNesia-Siap-Upload.zip**: paket untuk diunggah ke hosting. `index.html` langsung berada di akar ZIP.
- **public_html/index.html**: halaman awal; dapat dibuka langsung untuk pratinjau di laptop.
- **Perbarui-HTML.bat**: ekspor ulang data terbaru dari aplikasi SATRIA lokal.
- **ekspor_html.py** dan **site/**: pembuat paket dan template, cukup disimpan di laptop.

Paket HTML hanya membutuhkan hosting yang dapat menyajikan HTML, CSS, JavaScript, gambar, dan dokumen. Tidak membutuhkan Python, Streamlit, database MySQL, npm, atau proses instalasi di server hosting.

## Mengunggah ke DomaiNesia

1. Masuk ke panel hosting dari akun DomaiNesia. Buka **File Manager** (nama menu dapat berbeda sesuai layanan).
2. Pilih document root domain/subdomain tujuan. Pada cPanel, domain utama biasanya memakai `public_html`; domain/subdomain lain mengikuti lokasi yang ditetapkan pada menu Domains.
3. Untuk alamat `https://domain-bapak/satria/`, buat folder **satria** di dalam document root. Untuk alamat domain langsung, gunakan document root itu sendiri. Gunakan folder tujuan yang tidak menimpa situs lain.
4. Unggah **SATRIA-DomaiNesia-Siap-Upload.zip**, kemudian **Extract** di folder tujuan.
5. Pastikan `index.html`, `styles.css`, `app.js`, `data.js`, `assets/`, dan `dokumen/` berada pada tingkat folder yang sama. Tampilkan hidden files untuk melihat `.htaccess`.
6. Aktifkan SSL domain melalui panel hosting jika belum aktif. Buka alamat situs menggunakan **https://**.
7. Periksa Ringkasan, filter periode, galeri, dan unduhan dokumen. Jika domain baru, tunggu DNS mengarah ke hosting sesuai petunjuk penyedia.
8. Hapus ZIP dari folder publik sesudah berhasil diekstrak; salinan ZIP tetap tersedia di laptop.

Hanya unggah isi ZIP hasil ekspor. Folder aplikasi Streamlit, basis data SQLite, backup, dan konfigurasi akun tidak diperlukan di hosting HTML.

## Pembaruan data

1. Perbarui data di aplikasi SATRIA asli seperti biasa.
2. Klik **Perbarui-HTML.bat** pada folder Hosting-DomaiNesia di laptop. Letak folder ini harus tetap langsung di bawah folder Dashboard Pengendalian agar sumber `data/satria.db` ditemukan otomatis.
3. Tunggu pesan selesai. Ekspor hanya membaca basis data; tidak mengubah data aplikasi.
4. Unggah ZIP baru dan ekstrak untuk mengganti berkas versi HTML sebelumnya. Bila ada dokumen/foto yang dihapus dari sumber, bersihkan folder publik lama terlebih dahulu setelah mencadangkan situs agar salinan lama tidak tertinggal.
5. Muat ulang browser (Ctrl+F5) dan periksa stempel **Ekspor data**.

Semua tabel diekspor dalam satu transaksi baca yang konsisten. Akun pengguna, hash/salt sandi, log audit, dan berkas impor mentah tidak disertakan. Kolom akun pencatat pada catatan arahan dipertahankan sebagai konteks sumber, tanpa data login.

## Fitur versi HTML

- Ringkasan anggaran per periode, grafik IKPA, serta prioritas perhatian.
- Rincian anggaran kategori agregat, jenis, dan bagian, dengan sumber masing-masing.
- Paket, informasi Kartu Kendali, matriks risiko 5×5, monitoring kontrak.
- Milestone, catatan arahan/usulan, unduh dokumen, serta galeri foto.
- Pencarian, filter status/periode, unduh CSV sesuai filter, cetak halaman, tampilan HP.
- Seluruh aset lokal; tidak memerlukan CDN atau layanan grafik eksternal.

Ini merupakan **publikasi salinan data (snapshot), akses baca**. Tidak ada login, input/update bersama, impor Excel/PDF ke database hosting, audit baru, atau pengiriman peringatan otomatis. Fitur operasional tersebut tetap ada pada aplikasi Streamlit asli dan memerlukan layanan server bila hendak dijalankan online.

Periode anggaran dan IKPA dapat berbeda. Paket/kontrak memiliki sumber/periode sendiri. Status milestone dan kontrak tidak diubah menjadi selesai otomatis. Peringatan jadwal dihitung pada tanggal ekspor, bukan klaim kemajuan hari ini. Catatan arahan menampilkan akun pencatat dan dapat berisi usulan yang belum disahkan.

Siapa pun yang dapat membuka URL situs dapat membaca data dan mengunduh dokumen yang dipublikasikan. Jika dashboard hanya untuk internal, gunakan proteksi direktori/password yang disediakan panel hosting (misalnya Directory Privacy pada cPanel), bukan formulir login JavaScript.

## Mengubah tampilan atau menambah dokumen/foto

- Edit HTML/CSS/JavaScript pada folder **site/**, lalu jalankan ekspor ulang.
- Foto diambil dari `assets/kegiatan/` dan `assets/galeri/` aplikasi asli. Nama file menjadi caption. Kelompok visual pendukung dipisahkan dari dokumentasi kegiatan.
- Dokumen diambil dari `assets/pilar/` (DOCX, PDF, MD) dan buku panduan PDF pada folder aplikasi. Dokumen draf tetap disebut sebagai salinan dokumen, tidak dinyatakan telah disahkan.

## Jika ada kendala

- **Halaman kosong/data tidak tampil:** pastikan `data.js` ikut terunggah; aktifkan JavaScript dan periksa tidak ada folder tambahan setelah ekstraksi.
- **Logo/foto hilang:** pastikan folder `assets` terunggah lengkap dan gunakan nama file sesuai paket (hosting Linux membedakan huruf besar/kecil).
- **HTTP 500 setelah unggah:** beberapa layanan membatasi direktif `.htaccess`; coba ubah nama `.htaccess` dan hubungi dukungan hosting. HTML tetap bisa berjalan tanpa berkas ini.
- **Situs lama masih tampil:** periksa document root domain, file index lain, cache hosting/CDN, lalu Ctrl+F5.
- **Data tidak berubah:** klik ekspor ulang setelah memperbarui SQLite dan unggah paket baru. Versi HTML tidak menarik data dari laptop secara otomatis.

Paket ini disiapkan untuk diunggah; penerbitan ke akun DomaiNesia dilakukan melalui panel hosting milik Bapak.
