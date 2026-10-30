import json
import datetime
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from drtc_app.models import ServicePackage, Booking, CustomerReview, ContactInquiry, AdminLoginAttempt
from drtc_app.security import record_failed_attempt, get_ip_attempt_status, clear_failed_attempts, MAX_FAILED_ATTEMPTS


class ModelTests(TestCase):
    def setUp(self):
        self.pkg = ServicePackage.objects.create(
            capacity="1000 L",
            capacity_liters=1000,
            price=Decimal("400.00"),
            original_mrp=Decimal("600.00"),
            is_popular=True,
            ideal_for="2-3 BHK",
            duration_mins=60,
            features_list="Rotary Jet Washing\nSludge Vacuum\nUV Disinfection",
            order=2
        )

    def test_service_package_properties(self):
        self.assertEqual(self.pkg.discount_percent, 33)
        self.assertEqual(self.pkg.savings, 200)
        features = self.pkg.get_features()
        self.assertEqual(len(features), 3)
        self.assertIn("UV Disinfection", features)
        self.assertEqual(str(self.pkg), "1000 L - ₹400.00")

    def test_booking_creation_and_properties(self):
        booking = Booking.objects.create(
            customer_name="Ramesh Sharma",
            customer_phone="9835123456",
            package=self.pkg,
            total_amount=Decimal("400.00"),
            address="Near Kali Mandir, Gamharia",
            area_locality="Gamharia"
        )
        self.assertTrue(booking.booking_id.startswith("DRTC-"))
        self.assertEqual(booking.clean_customer_phone, "919835123456")
        self.assertEqual(booking.clean_customer_tel, "9835123456")
        self.assertEqual(booking.display_capacity, "1000 L")
        wa_url = booking.get_whatsapp_url()
        self.assertIn("https://wa.me/917808611636?text=", wa_url)
        self.assertIn(booking.booking_id, wa_url)


class EndpointAndAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.pkg = ServicePackage.objects.create(
            capacity="1000 L",
            capacity_liters=1000,
            price=Decimal("400.00"),
            original_mrp=Decimal("600.00"),
            order=1
        )
        self.booking = Booking.objects.create(
            customer_name="Test Customer",
            customer_phone="9835111222",
            package=self.pkg,
            total_amount=Decimal("400.00"),
            address="Shantinagar, Gamharia",
            status="CONFIRMED"
        )

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "DRTC SERVICE")
        self.assertContains(res, "CLEANER TANKS")

    def test_privacy_and_terms(self):
        r_priv = self.client.get('/privacy-policy/')
        self.assertEqual(r_priv.status_code, 200)
        self.assertContains(r_priv, "Privacy Policy")

        r_terms = self.client.get('/terms-and-conditions/')
        self.assertEqual(r_terms.status_code, 200)
        self.assertContains(r_terms, "Terms of Service")

    def test_calculator_api(self):
        res = self.client.get('/api/quote/?capacity=1000&count=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['total'], 800)
        self.assertEqual(data['price_per_tank'], 400)
        self.assertEqual(data['count'], 2)

    def test_live_stats_api(self):
        res = self.client.get('/api/live-stats/')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['total_bookings'], 1)

    def test_booking_track_view_and_api(self):
        # HTML View
        res_html = self.client.get(f'/booking/track/?q={self.booking.booking_id}')
        self.assertEqual(res_html.status_code, 200)
        self.assertContains(res_html, self.booking.booking_id)

        # JSON Status API
        res_api = self.client.get(f'/api/booking/status/{self.booking.booking_id}/')
        self.assertEqual(res_api.status_code, 200)
        data = json.loads(res_api.content)
        self.assertTrue(data['found'])
        self.assertEqual(data['status'], 'CONFIRMED')

    def test_create_booking_api(self):
        payload = {
            'customer_name': 'New Customer',
            'customer_phone': '9835999888',
            'address': 'Plot 4, Main Road, Gamharia',
            'custom_capacity': '2000 L',
            'tank_type': 'OVERHEAD_PVC',
            'number_of_tanks': 1,
            'preferred_date': str(datetime.date.today()),
            'preferred_time_slot': '08:00 AM - 11:00 AM',
            'payment_method': 'PAY_ON_SERVICE',
        }
        res = self.client.post('/api/booking/create/', payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['booking_id'].startswith('DRTC-'))
        self.assertEqual(data['total_amount'], 650.0)

    def test_contact_form_api(self):
        payload = {
            'name': 'Inquirer',
            'phone': '9835777666',
            'message': 'Need quotation for 3 water tanks.'
        }
        res = self.client.post('/api/contact/', payload, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(ContactInquiry.objects.filter(phone='9835777666').exists())


class SecurityAndAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser('admin', 'admin@drtc.com', 'admin123')
        self.secret_path = getattr(settings, 'DJANGO_ADMIN_URL', 'drtc-management-hub-786/').strip('/') + '/'

    def test_decoy_trap_returns_404(self):
        with self.settings(DEBUG=False):
            res = self.client.get('/admin/')
            self.assertEqual(res.status_code, 404)
            res_sub = self.client.get('/admin/login/')
            self.assertEqual(res_sub.status_code, 404)
        with self.settings(DEBUG=True):
            res_dev = self.client.get('/admin/')
            self.assertEqual(res_dev.status_code, 302)

    def test_secret_admin_portal_accessible(self):
        res = self.client.get(f'/{self.secret_path}')
        self.assertEqual(res.status_code, 302)  # Redirects to login
        res_login = self.client.get(f'/{self.secret_path}login/')
        self.assertEqual(res_login.status_code, 200)

    def test_admin_authentication_and_redirect(self):
        login_url = f'/{self.secret_path}login/'
        res = self.client.post(login_url, {'username': 'admin', 'password': 'admin123'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context['user'].is_authenticated)

    def test_brute_force_lockout_mechanism(self):
        test_ip = '192.168.1.99'
        for i in range(MAX_FAILED_ATTEMPTS):
            AdminLoginAttempt.objects.create(
                ip_address=test_ip,
                username='hacker',
                user_agent='TestAgent'
            )
        is_locked, rem_mins, count = get_ip_attempt_status(test_ip)
        self.assertTrue(is_locked)
        self.assertGreater(rem_mins, 0)
        self.assertEqual(count, MAX_FAILED_ATTEMPTS)

        # Clear attempts
        clear_failed_attempts(test_ip)
        is_locked, _, count = get_ip_attempt_status(test_ip)
        self.assertFalse(is_locked)
        self.assertEqual(count, 0)
