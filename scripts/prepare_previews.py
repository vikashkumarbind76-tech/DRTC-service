import os, shutil
from PIL import Image

artifact_dir = r"C:\Users\Vikash\.gemini\antigravity\brain\30ea19b8-8ecd-4f4c-855e-094b7954d7c0"
preview_dir = os.path.join(artifact_dir, "preview")
os.makedirs(preview_dir, exist_ok=True)

# Copy the specific full screenshots
steps_dir = os.path.join(artifact_dir, ".system_generated", "steps")

# Success page
src_success = os.path.join(steps_dir, "413", "media_0.png")
if os.path.exists(src_success):
    shutil.copyfile(src_success, os.path.join(preview_dir, "panel_07_success.png"))

# Admin Dashboard
src_admin_dash = os.path.join(steps_dir, "435", "media_0.png")
if os.path.exists(src_admin_dash):
    shutil.copyfile(src_admin_dash, os.path.join(preview_dir, "panel_08_admin_dashboard.png"))

# Admin Pricing
src_admin_pricing = os.path.join(steps_dir, "443", "media_0.png")
if os.path.exists(src_admin_pricing):
    shutil.copyfile(src_admin_pricing, os.path.join(preview_dir, "panel_08_admin_pricing.png"))

# Admin Gallery
src_admin_gallery = os.path.join(steps_dir, "449", "media_0.png")
if os.path.exists(src_admin_gallery):
    shutil.copyfile(src_admin_gallery, os.path.join(preview_dir, "panel_08_admin_gallery.png"))

# Mobile View
src_mobile = os.path.join(steps_dir, "459", "media_0.png")
if os.path.exists(src_mobile):
    shutil.copyfile(src_mobile, os.path.join(preview_dir, "panel_09_mobile.png"))

# Now let's crop high-precision section snapshots from the full page screenshot!
full_img = Image.open(os.path.join(artifact_dir, "full_page_screenshot.png"))
w, h = full_img.size

# Let's crop exact panels:
# 1. Hero: y: 0 to 1100
full_img.crop((0, 0, w, 1100)).save(os.path.join(preview_dir, "panel_01_hero.jpg"), quality=90)

# 2. Quick Pricing (5 cards): y: 1100 to 1900
full_img.crop((0, 1100, w, 1900)).save(os.path.join(preview_dir, "panel_01b_pricing_5cards.jpg"), quality=90)

# 3. Why Choose Us (6 cards): y: 1900 to 2800
full_img.crop((0, 1900, w, 2800)).save(os.path.join(preview_dir, "panel_01c_why_us.jpg"), quality=90)

# 4. Our Services (6 cards): y: 2800 to 4200
full_img.crop((0, 2800, w, 4200)).save(os.path.join(preview_dir, "panel_02_our_services.jpg"), quality=90)

# 5. Service Pricing (3+2 & Banner): y: 4200 to 5700
full_img.crop((0, 4200, w, 5700)).save(os.path.join(preview_dir, "panel_03_pricing_split.jpg"), quality=90)

# 6. About DRTC Service: y: 5700 to 6800
full_img.crop((0, 5700, w, 6800)).save(os.path.join(preview_dir, "panel_05_about.jpg"), quality=90)

# 7. Booking (Form + Table + 4 Badges): y: 6800 to 8000
full_img.crop((0, 6800, w, 8000)).save(os.path.join(preview_dir, "panel_04_booking.jpg"), quality=90)

# 8. Gallery (4 photos): y: 8000 to 8900
full_img.crop((0, 8000, w, 8900)).save(os.path.join(preview_dir, "panel_gallery.jpg"), quality=90)

# 9. Contact Us: y: 8900 to 9800
full_img.crop((0, 8900, w, 9800)).save(os.path.join(preview_dir, "panel_06_contact.jpg"), quality=90)

print("Saved all preview images successfully!")

