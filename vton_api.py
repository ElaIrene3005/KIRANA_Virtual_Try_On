import requests
import os

def call_vton_api(user_img, clothing_img, result_path, api_key):
    url = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com"
    }

    print("🔄 Sending request to API...")
    try:
        with open(user_img, "rb") as user_file, open(clothing_img, "rb") as cloth_file:
            files = {
                "avatar_image": ("input.jpg", user_file, "image/jpeg"),
                "clothing_image": ("clothing.jpg", cloth_file, "image/jpeg")
            }
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200 and response.content[:4] == b'\xff\xd8\xff\xe0':
            with open(result_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Success! Result saved as {result_path}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text[:300]}")
            return False
    except Exception as e:
        print("⚠️ Exception:", e)
        return False
