# Virtual Try-On Application

Virtual Try-On adalah aplikasi interaktif berbasis Python yang memungkinkan pengguna untuk mencoba kemeja secara virtual. Pengguna dapat mengambil gambar diri mereka melalui kamera, memilih template kemeja, menambahkan pola batik atau desain, dan melihat hasil try-on menggunakan API berbasis Diffusion Model.

## Fitur Utama

- Capture gambar pengguna dengan countdown 10 detik.
- Pilih template kemeja berdasarkan gender.
- Terapkan pola (batik atau desain) ke template kemeja.
- Generate virtual try-on menggunakan API Try-On Diffusion.
- Preview hasil pola dan hasil try-on dalam GUI interaktif.
- Mendukung penyimpanan hasil try-on.

## Struktur Folder Repository

Virtual-Try-On/
│
├── assets/                 # Folder berisi aset aplikasi
│   ├── templates/          # Template kemeja
│   │   ├── kemeja_putih_1.png
│   │   └── kemeja_putih_2.png
│   └── patterns/           # Pola batik atau desain kemeja
│       ├── 1.jpg
│       ├── 2.jpg
│       └── ... (1–20)
│
├── results/                # Folder hasil output
│   ├── pattern_result.jpg
│   └── result.jpg
│
├── main.py                 # Program utama GUI dan workflow virtual try-on
├── vton_api.py             # File untuk memanggil API Try-On Diffusion
├── pattern_to_shirt.py     # File untuk menggabungkan pola ke template kemeja
├── README.md               # Dokumentasi proyek
└── .gitignore              # File Git ignore


## Branch Struktur (Git)

- `main` → Branch utama untuk versi stabil aplikasi GUI.  
- `dev` → Branch pengembangan untuk fitur baru atau eksperimen.  
- `assets-update` → Branch khusus untuk update template kemeja atau pola batik.  
- `api-integration` → Branch khusus untuk pengembangan integrasi dengan Try-On Diffusion API.

## Requirement / Library

- Python 3.x  
- Tkinter  
- OpenCV (`cv2`)  
- Pillow (`PIL`)  
- Requests  
- Threading (bawaan Python)  
- RapidAPI key untuk Try-On Diffusion API  

