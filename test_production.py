import os, django, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from django.test import Client
from django.conf import settings
from django.contrib.auth.models import User
from drtc_app.models import ServicePackage, Booking, CustomerReview, ContactInquiry

c = Client()
secret_admin = getattr(settings, 'DJANGO_ADMIN_URL', 'drtc-management-hub-786/').strip('/') + '/'

urls = [
    ('/', 'Home page', (200,)),
    ('/track/', 'Booking Tracker (Alias)', (200,)),
    ('/booking/track/', 'Booking Tracker (Canonical)', (200,)),
    ('/privacy-policy/', 'Privacy Policy (Canonical)', (200,)),
    ('/privacy/', 'Privacy Policy (Alias)', (200,)),
    ('/terms/', 'Terms & Conditions (Alias)', (200,)),
    ('/terms-and-conditions/', 'Terms & Conditions (Canonical)', (200,)),
    ('/api/live-stats/', 'Live Stats API', (200,)),
    ('/api/quote/?capacity=1000&count=1', 'Quote API 1000L', (200,)),
    ('/api/quote/?capacity=8000&count=1', 'Quote API 8000L', (200,)),
    ('/api/quote/?capacity=150000&count=1', 'Quote API 150000L', (200,)),
    ('/admin/', 'Admin Decoy Trap / Dev Redirect', (302, 404)),
    (f'/{secret_admin}', 'Secret Operations Portal (Redirect)', (302,)),
    (f'/{secret_admin}login/', 'Secret Operations Login Page', (200,)),
]

print('=== URL STATUS & SECURITY TESTS ===')
all_ok = True
for url, name, expected_statuses in urls:
    r = c.get(url, follow=False)
    status = r.status_code
    ok = status in expected_statuses
    mark = 'OK  ' if ok else 'FAIL'
    if not ok:
        all_ok = False
    print('  [%s] %s  %-35s %s' % (mark, status, name, url))

print()
print('=== API CORRECTNESS TESTS ===')

r = c.get('/api/quote/?capacity=1000&count=1')
data = json.loads(r.content)
ok = data.get('total') == 400
print('  [%s] 1000L quote total=%s (expected 400)' % ('OK  ' if ok else 'FAIL', data.get('total')))

r = c.get('/api/quote/?capacity=8000&count=1')
data = json.loads(r.content)
ok = data.get('total') == 1680
print('  [%s] 8000L quote total=%s (expected 1680)' % ('OK  ' if ok else 'FAIL', data.get('total')))

r = c.get('/api/quote/?capacity=150000&count=1')
data = json.loads(r.content)
ok = data.get('total') == 36830
print('  [%s] 150000L quote total=%s (expected 36830)' % ('OK  ' if ok else 'FAIL', data.get('total')))

r = c.get('/api/live-stats/')
data = json.loads(r.content)
ok = data.get('status') == 'success'
print('  [%s] Live stats API status=%s' % ('OK  ' if ok else 'FAIL', data.get('status')))

print()
print('=== DATABASE COUNTS ===')
print('  ServicePackages: %d' % ServicePackage.objects.count())
print('  Bookings: %d' % Booking.objects.count())
print('  Reviews: %d' % CustomerReview.objects.count())
print('  ContactInquiries: %d' % ContactInquiry.objects.count())
print('  Admin users: %d' % User.objects.filter(is_superuser=True).count())
superusers = list(User.objects.filter(is_superuser=True).values_list('username', flat=True))
print('  Superuser accounts: %s' % superusers)

print()
print('=== BOOKING FORM POST TEST ===')
import datetime

r = c.post('/api/booking/create/', {
    'customer_name': 'Test Customer',
    'customer_phone': '9835123456',
    'address': 'House No 12, Near Jhanda Chowk, Gamharia',
    'custom_capacity': '1000 L',
    'tank_type': 'OVERHEAD_PVC',
    'number_of_tanks': '1',
    'preferred_date': str(datetime.date.today()),
    'preferred_time_slot': '08:00 AM - 11:00 AM',
    'area_locality': 'Gamharia',
    'payment_method': 'PAY_ON_SERVICE',
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', content_type='application/x-www-form-urlencoded')

created_booking_id = None
if r.status_code == 200:
    data = json.loads(r.content)
    ok = data.get('status') == 'success'
    created_booking_id = data.get('booking_id')
    print('  [%s] Booking create: status=%s, booking_id=%s, amount=%s' % (
        'OK  ' if ok else 'FAIL', data.get('status'), created_booking_id, data.get('total_amount')))
else:
    print('  [FAIL] Booking create returned HTTP %s' % r.status_code)

print()
print('=== BOOKING TRACKING & SUCCESS PAGE TEST ===')
if created_booking_id:
    # 1. Booking success receipt page
    r_success = c.get(f'/booking/success/{created_booking_id}/')
    ok_succ = r_success.status_code == 200 and created_booking_id in r_success.content.decode('utf-8')
    print('  [%s] Booking success view for %s (HTTP %s)' % ('OK  ' if ok_succ else 'FAIL', created_booking_id, r_success.status_code))

    # 2. Tracking page search
    r_track = c.get(f'/booking/track/?q={created_booking_id}')
    ok_track = r_track.status_code == 200 and created_booking_id in r_track.content.decode('utf-8')
    print('  [%s] Booking track HTML search for %s (HTTP %s)' % ('OK  ' if ok_track else 'FAIL', created_booking_id, r_track.status_code))

    # 3. Tracking API real-time status
    r_track_api = c.get(f'/api/booking/status/{created_booking_id}/')
    ok_api = r_track_api.status_code == 200 and json.loads(r_track_api.content).get('found') is True
    print('  [%s] Booking status API for %s (HTTP %s)' % ('OK  ' if ok_api else 'FAIL', created_booking_id, r_track_api.status_code))

    # Clean up test booking
    Booking.objects.filter(booking_id=created_booking_id).delete()
    print('       (test booking cleaned up)')

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
login_url = f'/{secret_admin}login/'
res_login = c.post(login_url, {'username': 'admin', 'password': 'admin123'}, follow=True)
login_ok = res_login.status_code == 200 and ('Bookings slated for today' in res_login.content.decode('utf-8') or 'COMMAND & DISPATCH' in res_login.content.decode('utf-8'))
print('  [%s] Admin login & dashboard load with credentials (HTTP %s)' % ('OK  ' if login_ok else 'FAIL', res_login.status_code))

print()
print('=== HOME PAGE CONTENT CHECK ===')
r = c.get('/')
html = r.content.decode('utf-8', errors='replace')
checks = [
    ('DRTC SERVICE', 'Brand name in page'),
    ('CLEANER TANKS', 'Hero headline'),
    ('TRANSPARENT TANK CLEANING PACKAGES', 'Pricing section heading'),
    ('OFFICIAL CAPACITY', 'Pricing section tag'),
    ('FREQUENTLY ASKED QUESTIONS', 'FAQ section'),
    ('SCHEDULE SERVICE OR CALL DIRECTLY', 'Contact section'),
    ('drtc_logo.png', 'Logo image referenced'),
    ('tank_feature_cutout.png', 'Hero tank image'),
    ('styles.css', 'CSS stylesheet linked'),
    ('main.js', 'JS file linked'),
    ('bookingModal', 'Booking modal present'),
    ('mobile-bottom-bar', 'Mobile bottom bar present'),
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
