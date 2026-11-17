import json
import base64
import os
import re

out_dir = 'stitch_output'
os.makedirs(out_dir, exist_ok=True)

# 1. HTML
with open(r'C:/Users/Vikash/.gemini/antigravity/brain/30ea19b8-8ecd-4f4c-855e-094b7954d7c0/.system_generated/steps/486/output.txt', 'r', encoding='utf-8') as f:
    data_html = json.load(f)

html_content = data_html['html']
html_path = os.path.join(out_dir, 'DRTC_Service_Dark_Industrial_Water_Hygiene_Platform.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f'Saved HTML to {html_path} ({len(html_content)} chars)')

# 2. PNG
with open(r'C:/Users/Vikash/.gemini/antigravity/brain/30ea19b8-8ecd-4f4c-855e-094b7954d7c0/.system_generated/steps/488/output.txt', 'r', encoding='utf-8') as f:
    data_img = json.load(f)

img_bytes = base64.b64decode(data_img['image'])
img_path = os.path.join(out_dir, 'DRTC_Service_Dark_Industrial_Water_Hygiene_Platform.png')
with open(img_path, 'wb') as f:
    f.write(img_bytes)
print(f'Saved PNG screenshot to {img_path} ({len(img_bytes)} bytes)')

# 3. Find image URLs in HTML
img_srcs = re.findall(r'src=["\'](http[^"\']+)["\']', html_content)
bg_urls = re.findall(r'url\(["\']?(http[^"\'\)]+)["\']?\)', html_content)
all_urls = sorted(list(set(img_srcs + bg_urls)))
print(f'Found {len(all_urls)} hosted image/asset URLs in HTML:')
for u in all_urls:
    print(' -', u)

with open(os.path.join(out_dir, 'image_urls.txt'), 'w', encoding='utf-8') as f:
    for u in all_urls:
        f.write(u + '\n')
