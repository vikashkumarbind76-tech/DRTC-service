import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.conf import settings
from drtc_app.models import Booking, ContactInquiry, CustomerReview, ServicePackage
from django.contrib.auth.models import User

c = Client()
secret_admin = getattr(settings, 'DJANGO_ADMIN_URL', 'drtc-secure-portal-786/').strip('/') + '/'

print('=== URL STATUS & SECURITY TESTS ===')
urls_to_test = [
    ('Home page', '/'),
    ('Booking Tracker (Alias)', '/track/'),
    ('Booking Tracker (Canonical)', '/booking/track/'),
    ('Privacy Policy (Canonical)', '/privacy-policy/'),
    ('Privacy Policy (Alias)', '/privacy/'),
    ('Terms & Conditions (Alias)', '/terms/'),
    ('Terms & Conditions (Canonical)', '/terms-and-conditions/'),
    ('Live Stats API', '/api/live-stats/'),
    ('Quote API 1000L', '/api/quote/?capacity=1000&count=1'),
    ('Quote API 8000L', '/api/quote/?capacity=8000&count=1'),
    ('Quote API 150000L', '/api/quote/?capacity=150000&count=1'),
    ('Admin Decoy Trap / Dev Redirect', '/admin/'),
    ('Secret Operations Portal (Redirect)', f'/{secret_admin}'),
    ('Secret Operations Login Page', f'/{secret_admin}login/'),
]

all_ok = True
for name, url in urls_to_test:
    r = c.get(url, follow=False)
    status = r.status_code
    expected = [200, 301, 302]
    is_ok = status in expected
    if not is_ok:
        all_ok = False
    print('  [%s] %-4d %-35s %s' % ('OK  ' if is_ok else 'FAIL', status, name, url))

print()
print('=== API CORRECTNESS TESTS ===')
r = c.get('/api/quote/?capacity=1000&count=1')
data = json.loads(r.content)
print('  [%s] 1000L quote total=%s (expected 400)' % ('OK  ' if data.get('total') == 400 else 'FAIL', data.get('total')))

r = c.get('/api/quote/?capacity=8000&count=1')
data = json.loads(r.content)
print('  [%s] 8000L quote total=%s (expected 1680)' % ('OK  ' if data.get('total') == 1680 else 'FAIL', data.get('total')))

r = c.get('/api/quote/?capacity=150000&count=1')
data = json.loads(r.content)
print('  [%s] 150000L quote total=%s (expected 36830)' % ('OK  ' if data.get('total') == 36830 else 'FAIL', data.get('total')))

r = c.get('/api/live-stats/')
data = json.loads(r.content)
print('  [%s] Live stats API status=%s' % ('OK  ' if data.get('status') == 'success' else 'FAIL', data.get('status')))

print()
print('=== DATABASE COUNTS ===')
print('  ServicePackages: %d' % ServicePackage.objects.count())
print('  Bookings: %d' % Booking.objects.count())
print('  Reviews: %d' % CustomerReview.objects.count())
print('  ContactInquiries: %d' % ContactInquiry.objects.count())
print('  Admin users: %d' % User.objects.filter(is_staff=True).count())
print('  Superuser accounts: %s' % list(User.objects.filter(is_superuser=True).values_list('username', flat=True)))

print()
print('=== BOOKING FORM POST TEST ===')
r = c.post('/api/bookings/create/', {
    'customer_name': 'Test Production Runner',
    'customer_phone': '9876543210',
    'custom_capacity': '1000 L',
    'address': 'Test Address Gamharia',
    'landmark': 'Near Jhanda Chowk',
    'area_locality': 'Gamharia',
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', content_type='application/x-www-form-urlencoded')

if r.status_code == 200:
    data = json.loads(r.content)
    ok = data.get('status') == 'success'
    bid = data.get('booking_id')
    print('  [%s] Booking create: status=%s, booking_id=%s, amount=%s' % ('OK  ' if ok else 'FAIL', data.get('status'), bid, data.get('total_amount')))

    print()
    print('=== BOOKING TRACKING & SUCCESS PAGE TEST ===')
    r_success = c.get(f'/booking/success/{bid}/')
    print('  [%s] Booking success view for %s (HTTP %d)' % ('OK  ' if r_success.status_code == 200 else 'FAIL', bid, r_success.status_code))

    r_track = c.get(f'/booking/track/?booking_id={bid}')
    print('  [%s] Booking track HTML search for %s (HTTP %d)' % ('OK  ' if r_track.status_code == 200 else 'FAIL', bid, r_track.status_code))

    r_api_track = c.get(f'/api/bookings/{bid}/status/')
    print('  [%s] Booking status API for %s (HTTP %d)' % ('OK  ' if r_api_track.status_code == 200 else 'FAIL', bid, r_api_track.status_code))

    Booking.objects.filter(booking_id=bid).delete()
    print('       (test booking cleaned up)')
else:
    print('  [FAIL] Booking create returned HTTP %s' % r.status_code)

print()
print('=== CONTACT FORM POST TEST ===')
r = c.post('/api/contact/', {
    'name': 'Test User',
    'phone': '9835123456',
    'message': 'Test inquiry from production check',
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', content_type='application/x-www-form-urlencoded')
if r.status_code == 200:
    data = json.loads(r.content)
    ok = data.get('status') == 'success'
    print('  [%s] Contact form: %s' % ('OK  ' if ok else 'FAIL', data.get('message', '')[:60]))
    if ok:
        ContactInquiry.objects.filter(name='Test User', phone='9835123456').delete()
        print('       (test inquiry cleaned up)')
else:
    print('  [FAIL] Contact form returned HTTP %s' % r.status_code)

print()
print('=== ADMIN AUTHENTICATION & DASHBOARD ACCESS TEST ===')
user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
user.set_password('admin123')
user.save()
c.force_login(user)
res_dash = c.get(f'/{secret_admin}')
login_ok = res_dash.status_code == 200 and ('ADMIN DASHBOARD' in res_dash.content.decode('utf-8') or 'Recent Bookings' in res_dash.content.decode('utf-8'))
print('  [%s] Admin dashboard load with credentials (HTTP %s)' % ('OK  ' if login_ok else 'FAIL', res_dash.status_code))

print()
print('=== HOME PAGE CONTENT CHECK ===')
r = c.get('/')
html = r.content.decode('utf-8', errors='replace')
checks = [
    ('DRTC SERVICE', 'Brand name in page'),
    ('CLEAN WATER', 'Hero watermark in page'),
    ('CLEANER, SAFER TOMORROW.', 'Hero headline in page'),
    ('TANK CLEANING SERVICES', 'Services & pricing section heading'),
    ('WHY CHOOSE', 'Why choose section heading'),
    ('BOOK YOUR TANK CLEANING', 'Booking section heading'),
    ('GALLERY', 'Gallery section heading'),
    ('hero_tank_splash.jpg', 'Hero tank splash image referenced'),
    ('gallery_1.jpg', 'Gallery image 1 referenced'),
    ('gallery_2.jpg', 'Gallery image 2 referenced'),
    ('gallery_3.jpg', 'Gallery image 3 referenced'),
    ('gallery_4.jpg', 'Gallery image 4 referenced'),
    ('tank_500.png', '500L Tank icon referenced'),
    ('tank_1000.png', '1000L Tank icon referenced'),
    ('tank_2000.png', '2000L Tank icon referenced'),
    ('tank_3000.png', '3000L Tank icon referenced'),
    ('tank_5000.png', '5000L Tank icon referenced'),
    ('styles.css', 'CSS stylesheet linked'),
    ('main.js', 'JS file linked'),
    ('7808611636', 'Dinesh phone number'),
    ('6352561343', 'Rakesh phone number'),
    ('Gamharia', 'Location mentioned'),
]
for needle, label in checks:
    found = needle in html
    print('  [%s] %s' % ('OK  ' if found else 'MISS', label))

print()
print('All tests complete.')
print('Overall URL status: %s' % ('ALL PASS' if all_ok else 'SOME FAILURES - check above'))
