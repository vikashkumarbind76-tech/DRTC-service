import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drtc_app.models import ServicePackage, CustomerReview, Booking
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed database with official DRTC service packages and reviews"

    def handle(self, *args, **options):
        self.stdout.write("Seeding DRTC data...")

        # 1. Superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@drtcservice.com", "admin123")
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created (password: admin123)"))

        # 2. Official Packages (from DRTC price chart)
        packages_data = [
            {
                "capacity": "500 Liter",
                "capacity_liters": 500,
                "price": 250.00,
                "original_mrp": 350.00,
                "is_popular": False,
                "ideal_for": "1-2 BHK Flats & Small Nuclear Families",
                "duration_mins": 45,
                "badge_text": "Quick Clean",
                "features_list": "Mechanized Dewatering\nSludge & Mud Extraction\nHigh Pressure Rotary Jet Scrub\nAnti-Bacterial UV Disinfection\nSafe Food-Grade Sterilization",
                "order": 1,
            },
            {
                "capacity": "1000 L",
                "capacity_liters": 1000,
                "price": 400.00,
                "original_mrp": 600.00,
                "is_popular": True,
                "ideal_for": "Standard 2-3 BHK Homes & Duplexes",
                "duration_mins": 60,
                "badge_text": "Most Popular",
                "features_list": "Full 6-Stage Scientific Cleaning\nComplete Sludge Removal\nRotary Jet Pressure Wash (Walls & Base)\nAnti-Bacterial Chemical Spray\nUV Germicidal Radiation Sterilization\nClean Odorless Water Guarantee",
                "order": 2,
            },
            {
                "capacity": "2000 L",
                "capacity_liters": 2000,
                "price": 650.00,
                "original_mrp": 950.00,
                "is_popular": False,
                "ideal_for": "Large Independent Houses & Joint Families",
                "duration_mins": 90,
                "badge_text": "Best Value",
                "features_list": "Full 6-Stage Scientific Cleaning\nDeep Vacuum Sludge Extraction\nHeavy Duty Jet Wall Scrubbing\nOrganic Disinfection Treatment\nUV Lamp Sanitization\nNo Water Wastage Tech",
                "order": 3,
            },
            {
                "capacity": "3000 L",
                "capacity_liters": 3000,
                "price": 900.00,
                "original_mrp": 1300.00,
                "is_popular": False,
                "ideal_for": "Apartment Buildings, Hostels & Commercial Units",
                "duration_mins": 120,
                "badge_text": "High Capacity",
                "features_list": "Multi-Layer Rotary High Pressure Jet\nIndustrial Sludge Suction\nBio-Enzyme & Anti-Bacterial Wash\nUV Ray Pathogen Elimination\nComplete Tank Inspection Report",
                "order": 4,
            },
            {
                "capacity": "5000 L",
                "capacity_liters": 5000,
                "price": 1100.00,
                "original_mrp": 1600.00,
                "is_popular": False,
                "ideal_for": "Societies, Hospitals, Schools & Industrial Plants",
                "duration_mins": 180,
                "badge_text": "Mega Saver",
                "features_list": "Full Commercial Grade 6-Stage Process\nDual-Pump High Flow Dewatering\nIndustrial Slurry Vacuuming\nDouble-Pass UV Sterilization\nFormal Quality & Hygiene Clearance",
                "order": 5,
            },
        ]

        for pkg in packages_data:
            obj, created = ServicePackage.objects.update_or_create(
                capacity=pkg["capacity"],
                defaults=pkg
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} package: {obj.capacity} @ Rs.{obj.price}")

        # 3. Authentic Customer Reviews
        reviews_data = [
            {
                "customer_name": "Rajesh Sharma",
                "locality": "Shantinagar, Gamharia",
                "tank_capacity": "1000 L Sintex Tank",
                "rating": 5,
                "review_title": "Remarkable cleaning! Water is crystal clear now",
                "comment": "Dinesh ji and Rakesh arrived promptly at our house near Jhanda Chowk. The amount of mud they removed from the bottom of our 1000L tank was unbelievable. Their high-pressure jet and UV treatment are very professional. Highly recommended!",
                "date_added": timezone.now().date() - timedelta(days=3),
            },
            {
                "customer_name": "Amit Mahato",
                "locality": "Gamharia Industrial Area",
                "tank_capacity": "5000 L Concrete Sump",
                "rating": 5,
                "review_title": "Best commercial tank cleaning service in town",
                "comment": "We booked them for our 5000L factory overhead tank. Their mechanized pumps and vacuum suction cleaned the entire tank within 3 hours. Transparent price of ₹1100 with zero hassle. Exceptional work!",
                "date_added": timezone.now().date() - timedelta(days=6),
            },
            {
                "customer_name": "Pooja Verma",
                "locality": "Adityapur, Jamshedpur",
                "tank_capacity": "500 L Overhead Tank",
                "rating": 5,
                "review_title": "Very affordable at ₹250 and extremely polite staff",
                "comment": "Quick booking on WhatsApp and arrived on time. The operator Rakesh wore proper boots and mask. After cleaning, they sanitized the tank thoroughly with food-grade spray and UV lamp. Safe water for my baby!",
                "date_added": timezone.now().date() - timedelta(days=9),
            },
            {
                "customer_name": "Sanjay Singh",
                "locality": "Lal Building, Gamharia",
                "tank_capacity": "2000 L RCC Sump",
                "rating": 5,
                "review_title": "Professional de-sludging without wasting extra water",
                "comment": "Our underground sump had thick algae and sediment buildup for 2 years. DRTC’s slurry vacuum machine took out everything without messing up our courtyard. Honest pricing of ₹650.",
                "date_added": timezone.now().date() - timedelta(days=12),
            },
        ]

        for rev in reviews_data:
            CustomerReview.objects.get_or_create(
                customer_name=rev["customer_name"],
                defaults=rev
            )

        # 4. Sample Booking for live tracking demo
        pkg_1000 = ServicePackage.objects.filter(capacity="1000 L").first()
        if not Booking.objects.filter(booking_id="DRTC-9821").exists():
            Booking.objects.create(
                booking_id="DRTC-9821",
                customer_name="Vikram Choudhary",
                customer_phone="9835123456",
                customer_email="vikram.c@gmail.com",
                package=pkg_1000,
                custom_capacity="1000 L",
                tank_type="OVERHEAD_PVC",
                number_of_tanks=1,
                total_amount=400.00,
                preferred_date=timezone.now().date() + timedelta(days=1),
                preferred_time_slot="08:00 AM - 11:00 AM",
                address="Plot 42, Near DAV Public School",
                landmark="Near Jhanda Chowk",
                area_locality="Shantinagar, Gamharia",
                payment_method="PAY_ON_SERVICE",
                payment_status="UNPAID",
                status="CONFIRMED",
                assigned_technician="Rakesh (Lead Operator)",
                notes="Overhead tank on 2nd floor roof terrace."
            )

        self.stdout.write(self.style.SUCCESS("DRTC seed data successfully loaded!"))
