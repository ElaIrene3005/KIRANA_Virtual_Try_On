import cv2
import numpy as np

def apply_pattern_to_shirt(template_path, pattern_path, output_path):
    shirt = cv2.imread(template_path)
    pattern = cv2.imread(pattern_path)

    if shirt is None or pattern is None:
        print("⚠️ Gagal membaca template atau pattern.")
        return

    pattern_resized = cv2.resize(pattern, (shirt.shape[1], shirt.shape[0]))
    blended = cv2.addWeighted(shirt, 0.5, pattern_resized, 0.5, 0)
    cv2.imwrite(output_path, blended)
