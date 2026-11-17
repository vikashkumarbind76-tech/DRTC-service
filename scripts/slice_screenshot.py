from PIL import Image
import os

img = Image.open(r'C:\Users\Vikash\.gemini\antigravity\brain\30ea19b8-8ecd-4f4c-855e-094b7954d7c0\full_page_screenshot.png')
w, h = img.size
out_dir = r'C:\Users\Vikash\.gemini\antigravity\brain\30ea19b8-8ecd-4f4c-855e-094b7954d7c0\live_slices'
os.makedirs(out_dir, exist_ok=True)

# Let's crop into chunks of 1500px to see everything
for i in range(0, min(h, 12000), 1200):
    box = (0, i, w, min(i + 1200, h))
    slice_img = img.crop(box)
    slice_img.save(f"{out_dir}/slice_{i//1200}.jpg", quality=85)

print(f"Saved slices up to height {min(h, 12000)} in {out_dir}")

