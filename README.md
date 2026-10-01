# DRTC SERVICE - Dinesh Rakesh Tank Cleaning Service

A premium, responsive full-stack Django web application and interactive booking storefront designed specifically for **DRTC SERVICE (Dinesh Rakesh Tank Cleaning Service)** in Gamharia & Jamshedpur.

> **Tagline:** *"CLEANER TANKS, SAFER TOMORROW"*

---

## 🌟 Brand & Visual Identity

- **Wordmark & Typography:** Two-tone metallic Gold / Electric Cyan / Crisp White branding using **Anton** for bold uppercase display headings and **Inter** for crisp scannable UI copy.
- **Aesthetic:** Dark, high-contrast, premium urban editorial style featuring deep obsidian surfaces (`#05070c`), rich charcoal cards, and purposeful accents for CTAs, prices, and status indicators.
- **Official Contact Credentials:**
  - **Dinesh (Owner):** +91 7808611636
  - **Rakesh (Operator):** +91 6352561343
  - **Address:** Shantinagar, Gamharia, Near By Jhanda Chowk, 832108
  - **Email:** drtcservice@gmail.com

---

## 💧 Official Capacity & Price Matrix (From Business Media)

| S.No. | Capacity | Official Rate | Regular MRP | Estimated Duration | Ideal For |
|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **500 Liter** | **₹250** | ₹350 | ~45 Mins | 1-2 BHK Flats & Nuclear Families |
| 2 | **1000 L** | **₹400** | ₹600 | ~60 Mins | Standard 2-3 BHK Homes *(Most Popular)* |
| 3 | **2000 L** | **₹650** | ₹950 | ~90 Mins | Large Independent Homes & Duplexes |
| 4 | **3000 L** | **₹900** | ₹1,300 | ~120 Mins | Apartment Buildings & Commercial |
| 5 | **5000 L** | **₹1,100** | ₹1,600 | ~180 Mins | Societies, Hospitals & Industries |

---

## ⚡ Core Features & Interactive Capabilities

1. **Fixed Translucent Glass Navigation:** Quick access to Pricing, Calculator, 6-Stage Process, Official Boards, Reviews, Booking Tracker, and Direct Call/Book CTAs.
2. **Impactful Hero Showcase:** High-resolution 3D tank with energetic water splash, live "Available Today in Gamharia & Jamshedpur" status badge, and floating price/UV tags.
3. **Interactive Multi-Tank & Sump Calculator:** Real-time calculation based on tank capacity, placement (overhead vs concrete underground sump), and tank quantity with instant 1-click WhatsApp quote.
4. **Universal Booking Engine & Modal:** Customers can select capacity, preferred date & time slot, enter their Gamharia/Jamshedpur address, and receive a branded digital booking card with a unique Booking ID (e.g. `DRTC-9821`).
5. **Direct WhatsApp & Phone Integration:** Pre-fills all booking specifications and launches a direct chat with Dinesh & Rakesh.
6. **Live Booking Status Tracker (`/booking/track/`):** Customers can check scheduled date, assigned technician, and service status anytime.
7. **Official Visiting Card & Price Board Lightbox:** Full-screen zoomable inspection of the authentic business media provided by the client.
8. **6-Stage Scientific Cleaning Process Visualizer:**
   - Step 01: Mechanized Dewatering
   - Step 02: Sludge & Silt Extraction
   - Step 03: High Pressure Rotary Jet Scrub
   - Step 04: Industrial Slurry Vacuuming
   - Step 05: Food-Grade Anti-Bacterial Spray
   - Step 06: UV Germicidal Radiation Treatment
9. **Django Operations Admin Dashboard (`/admin/`):** Manage booking records, change statuses, manage service packages, review inquiries, and export customer data.
10. **Sticky Mobile Action Bar:** Rapid 1-tap Call and WhatsApp buttons optimized for mobile conversions.

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- Django 6.0+

### 2. Run Database Migrations & Seed Data
```bash
python manage.py migrate
python manage.py seed_data
```
*Creates initial packages, authentic reviews, demo tracking data, and superuser (`admin` / `admin123`).*

### 3. Collect Static Files (Production Ready with Whitenoise)
```bash
python manage.py collectstatic --noinput
```

### 4. Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

---

## 🔐 Admin Credentials

- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username:** `admin`
- **Password:** `admin123`
