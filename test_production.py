import os, django, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from drtc_app.models import ServicePackage, Booking, CustomerReview, ContactInquiry

c = Client()

urls = [
    ('/', 'Home page'),
    ('/track/', 'Booking Tracker'),
    ('/privacy-policy/', 'Privacy Policy'),
    ('/terms/', 'Terms & Conditions'),
    ('/api/live-stats/', 'Live Stats API'),
    ('/api/quote/?capacity=1000&count=1', 'Quote API 1000L'),
    ('/api/quote/?capacity=8000&count=1', 'Quote API 8000L'),
    ('/api/quote/?capacity=150000&count=1', 'Quote API 150000L'),
    ('/admin/', 'Admin (redirect)'),
    ('/admin/login/', 'Admin Login'),
]

print('=== URL STATUS TESTS ===')
all_ok = True
for url, name in urls:
    r = c.get(url, follow=False)
    status = r.status_code
    ok = status in (200, 301, 302)
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
from django.test import RequestFactory
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

if r.status_code == 200:
    data = json.loads(r.content)
    ok = data.get('status') == 'success'
    print('  [%s] Booking create: status=%s, booking_id=%s, amount=%s' % (
        'OK  ' if ok else 'FAIL', data.get('status'), data.get('booking_id'), data.get('total_amount')))
    # Clean up test booking
    if data.get('status') == 'success':
        from drtc_app.models import Booking
        Booking.objects.filter(booking_id=data.get('booking_id')).delete()
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
