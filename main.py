import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from PIL import Image, ImageTk
import threading
import cv2
import requests
import os
import time
from pattern_to_shirt import apply_pattern_to_shirt  # pastikan file ini ada

# ---------------- CONFIG ----------------
RAPIDAPI_KEY = "7da4cb208dmsh4464812e85a195bp1a37c6jsn67de9767a8a2"
API_URL = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
USER_IMG = "input.jpg"
RESULT_IMG = "result.jpg"

TEMPLATE_DIR = "assets/templates"
PATTERN_DIR = "assets/patterns"
TEMP_OUTPUT = "pattern_result.jpg"

# ---------------- VARIABLES ----------------
cap = None
frame = None
running = True
user_image_captured = False
final_clothing_image = None

# ---------------- FUNCTIONS ----------------
def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    update_camera_feed()

def update_camera_feed():
    global frame
    if cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            display_img = img.resize((320, 180))
            imgtk = ImageTk.PhotoImage(image=display_img)
            left_panel.imgtk = imgtk
            left_panel.configure(image=imgtk)
    if running:
        left_panel.after(20, update_camera_feed)

def capture_image():
    """Countdown 10 detik sebelum capture gambar"""
    global frame, user_image_captured

    if cap is None or not cap.isOpened():
        print("❌ Kamera tidak aktif.")
        messagebox.showerror("Kamera Error", "Kamera tidak aktif atau tidak terdeteksi.")
        return

    countdown_window = Toplevel(root)
    countdown_window.title("Countdown")
    countdown_label = tk.Label(countdown_window, text="10", font=("Arial", 48))
    countdown_label.pack(padx=20, pady=20)

    def do_countdown():
        for i in range(10, 0, -1):
            countdown_label.config(text=str(i))
            countdown_window.update()
            time.sleep(1)
        countdown_window.destroy()

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(USER_IMG, frame)
            print("📸 User image captured")

            # Update flag di thread utama
            root.after(0, lambda: after_capture_success())
        else:
            print("❌ Gagal mengambil gambar.")
            root.after(0, lambda: messagebox.showerror("Error", "Gagal mengambil gambar."))

    threading.Thread(target=do_countdown).start()

def after_capture_success():
    global user_image_captured
    user_image_captured = True
    load_preview(USER_IMG, left_panel, preview_only=True)
    messagebox.showinfo("Sukses", "Foto berhasil diambil! Silakan lanjut pilih pola dan klik Generate Result.")

def load_preview(path, panel, preview_only=False):
    img = Image.open(path)
    w, h = img.size

    # Skala menyesuaikan lebar maksimum panel, tanpa mengubah rasio
    max_w, max_h = (320, 240) if not preview_only else (240, 240)
    scale = min(max_w / w, max_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h))

    tk_img = ImageTk.PhotoImage(img)
    panel.config(image=tk_img, width=max_w, height=max_h)
    panel.image = tk_img


def show_popup(img_path, title="Preview"):
    popup = Toplevel(root)
    popup.title(title)

    img = Image.open(img_path)
    w, h = img.size

    # Batasi ukuran popup tanpa merusak rasio
    max_w, max_h = 480, 480
    scale = min(max_w / w, max_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h))

    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(popup, image=tk_img)
    label.image = tk_img
    label.pack(padx=10, pady=10)


def combine_pattern_and_template():
    gender = gender_var.get()
    pattern_choice = pattern_var.get()

    if not gender or not pattern_choice:
        messagebox.showwarning("Peringatan", "Pilih gender dan pola terlebih dahulu!")
        return None

    template_name = "kemeja_putih_1.png" if gender == "Pria" else "kemeja_putih_2.png"
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    pattern_path = os.path.join(PATTERN_DIR, f"{pattern_choice}.jpg")

    if not os.path.exists(template_path) or not os.path.exists(pattern_path):
        messagebox.showerror("Error", "Template atau pola tidak ditemukan.")
        return None

    apply_pattern_to_shirt(template_path, pattern_path, TEMP_OUTPUT)
    load_preview(TEMP_OUTPUT, center_panel)
    show_popup(TEMP_OUTPUT, "Hasil Pola ke Kemeja")
    return TEMP_OUTPUT

def generate_result():
    global final_clothing_image

    if not user_image_captured:
        messagebox.showwarning("Peringatan", "Ambil gambar terlebih dahulu sebelum generate!")
        print("⚠️ Ambil gambar terlebih dahulu!")
        return

    final_clothing_image = combine_pattern_and_template()
    if final_clothing_image is None:
        print("⚠️ Ambil gambar dan pilih pola terlebih dahulu!")
        return

    threading.Thread(target=call_api).start()

def call_api():
    print("🔄 Sending request to API...")
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com"
    }
    try:
        with open(USER_IMG, "rb") as user_file, open(final_clothing_image, "rb") as cloth_file:
            files = {
                "avatar_image": ("input.jpg", user_file, "image/jpeg"),
                "clothing_image": ("clothing.jpg", cloth_file, "image/jpeg")
            }
            response = requests.post(API_URL, headers=headers, files=files)

        if response.status_code == 200 and response.content[:4] == b'\xff\xd8\xff\xe0':
            with open(RESULT_IMG, "wb") as f:
                f.write(response.content)
            print("✅ Success! Result saved as", RESULT_IMG)
            root.after(0, lambda: [
                load_preview(RESULT_IMG, right_panel),
                show_popup(RESULT_IMG, "Hasil Virtual Try-On")
            ])
        else:
            print(f"❌ Error {response.status_code}: {response.text[:300]}")
            messagebox.showerror("API Error", f"Gagal generate hasil: {response.status_code}")
    except Exception as e:
        print("⚠️ Exception:", e)
        messagebox.showerror("Exception", str(e))

def on_close():
    global running
    running = False
    if cap and cap.isOpened():
        cap.release()
    root.destroy()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Virtual Try-On App")
root.protocol("WM_DELETE_WINDOW", on_close)

# Panels
left_panel = tk.Label(root)
left_panel.grid(row=0, column=0, padx=10, pady=10)

center_panel = tk.Label(root)
center_panel.grid(row=0, column=1, padx=10, pady=10)

right_panel = tk.Label(root)
right_panel.grid(row=0, column=2, padx=10, pady=10)

# Dropdown untuk gender dan pola
gender_var = tk.StringVar()
pattern_var = tk.StringVar()

gender_label = tk.Label(root, text="Pilih Gender:")
gender_label.grid(row=1, column=0)
gender_dropdown = ttk.Combobox(root, textvariable=gender_var, values=["Pria", "Wanita"], state="readonly")
gender_dropdown.grid(row=2, column=0)

pattern_label = tk.Label(root, text="Pilih Pola (1–20):")
pattern_label.grid(row=1, column=1)
pattern_dropdown = ttk.Combobox(root, textvariable=pattern_var, values=[str(i) for i in range(1, 21)], state="readonly")
pattern_dropdown.grid(row=2, column=1)

# Buttons
btn_capture = tk.Button(root, text="📸 Capture (Countdown 10s)", command=capture_image)
btn_capture.grid(row=3, column=0, pady=5)

btn_preview = tk.Button(root, text="👕 Tampilkan Pola ke Kemeja", command=combine_pattern_and_template)
btn_preview.grid(row=3, column=1, pady=5)

btn_generate = tk.Button(root, text="✨ Generate Result", command=generate_result)
btn_generate.grid(row=3, column=2, pady=5)

# Start camera loop
start_camera()
root.mainloop()
