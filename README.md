Virtual-Try-On/
│
├─ assets/
│   ├─ templates/         # Folder berisi template kemeja (kemeja_putih_1.png, kemeja_putih_2.png)
│   └─ patterns/          # Folder berisi pola batik atau desain (1.jpg, 2.jpg, ..., 20.jpg)
│
├─ results/               # Folder hasil output (pattern_result.jpg, result.jpg)
│
├─ main.py                # Program utama GUI dan workflow virtual try-on
├─ vton_api.py            # File untuk memanggil API Try-On Diffusion
├─ pattern_to_shirt.py    # File untuk menggabungkan pola ke template kemeja
├─ README.md              # Dokumentasi proyek
└─ .gitignore             # File Git ignore
