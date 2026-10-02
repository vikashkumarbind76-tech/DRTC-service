import uuid
from django.db import models
from django.utils import timezone


class ServicePackage(models.Model):
    """Capacity tiers and pricing based on the official DRTC price matrix."""
    capacity = models.CharField(max_length=50, help_text="e.g. 500 Liter, 1000 L, 2000 L, 3000 L, 5000 L")
    capacity_liters = models.PositiveIntegerField(help_text="Numeric capacity in liters")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Official price in INR")
    original_mrp = models.DecimalField(max_digits=8, decimal_places=2, help_text="Standard market price / MRP")
    is_popular = models.BooleanField(default=False, help_text="Mark as most popular / recommended")
    ideal_for = models.CharField(max_length=150, help_text="e.g. 1-2 BHK flats, 3-4 BHK bungalows, commercial")
    duration_mins = models.PositiveIntegerField(default=60, help_text="Estimated time in minutes")
    features_list = models.TextField(
        default="High Pressure Rotary Jet Washing\nSludge & Silt Vacuum Extraction\nAnti-Bacterial UV Disinfection\nSafe Food-Grade Sterilization\nClean Water Guarantee",
        help_text="One feature per line"
    )
    badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Best Value, Most Popular")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'capacity_liters']
        verbose_name = "Service Package"
        verbose_name_plural = "Service Packages"

    def __str__(self):
        return f"{self.capacity} - ₹{self.price}"

    @property
    def discount_percent(self):
        if self.original_mrp and self.original_mrp > self.price:
            diff = self.original_mrp - self.price
            return int(round((diff / self.original_mrp) * 100))
        return 0

    @property
    def savings(self):
        if self.original_mrp and self.original_mrp > self.price:
            return int(self.original_mrp - self.price)
        return 0

    def get_features(self):
        return [f.strip() for f in self.features_list.strip().split('\n') if f.strip()]


class Booking(models.Model):
    """Customer booking records with real-time status and WhatsApp sync."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed & Scheduled'),
        ('TECHNICIAN_ASSIGNED', 'Technician Assigned'),
        ('IN_PROGRESS', 'Cleaning In Progress'),
        ('COMPLETED', 'Service Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    TANK_TYPE_CHOICES = [
        ('OVERHEAD_PVC', 'Overhead PVC / Sintex Tank'),
        ('UNDERGROUND_SUMP', 'Underground RCC / Concrete Sump'),
        ('LOFT_TANK', 'Loft / Indoor Tank'),
        ('COMMERCIAL_STORAGE', 'Commercial Storage Reservoir'),
        ('MULTIPLE_TANKS', 'Multiple Tanks Combo'),
    ]

    PAYMENT_CHOICES = [
        ('PAY_ON_SERVICE', 'Pay After Cleaning (Cash / UPI on site)'),
        ('UPI_ADVANCE', 'Instant UPI / QR Code'),
        ('ONLINE', 'Online Payment'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)

    package = models.ForeignKey(ServicePackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    custom_capacity = models.CharField(max_length=100, blank=True, help_text="e.g. 1000 L or custom capacity")
    tank_type = models.CharField(max_length=50, choices=TANK_TYPE_CHOICES, default='OVERHEAD_PVC')
    number_of_tanks = models.PositiveIntegerField(default=1)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    preferred_date = models.DateField(default=timezone.now)
    preferred_time_slot = models.CharField(
        max_length=50,
        default="08:00 AM - 11:00 AM",
        help_text="e.g. Morning (8 AM - 11 AM), Afternoon (11 AM - 2 PM), Evening (2 PM - 6 PM)"
    )

    address = models.TextField(help_text="House/Flat No, Street, Colony")
    landmark = models.CharField(max_length=120, blank=True, help_text="e.g. Near Jhanda Chowk, Lal Building, Gamharia")
    area_locality = models.CharField(max_length=120, default="Gamharia, Jamshedpur")
    pincode = models.CharField(max_length=10, default="832108")

    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='PAY_ON_SERVICE')
    payment_status = models.CharField(
        max_length=20,
        choices=[('UNPAID', 'Unpaid (Due upon completion)'), ('PAID', 'Paid in Full')],
        default='UNPAID'
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    assigned_technician = models.CharField(max_length=100, blank=True, default="Rakesh (Lead Operator)")
    notes = models.TextField(blank=True, help_text="Special instructions or notes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def display_capacity(self):
        if self.custom_capacity:
            return self.custom_capacity
        if self.package:
            return self.package.capacity
        return "1000 L"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate branded booking ID like DRTC-8942
            random_part = uuid.uuid4().hex[:5].upper()
            self.booking_id = f"DRTC-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.customer_name} ({self.tank_type}, {self.preferred_date})"

    @property
    def clean_customer_phone(self):
        """Sanitized 12-digit format with 91 prefix for WhatsApp API."""
        digits = "".join(filter(str.isdigit, str(self.customer_phone or "")))
        if len(digits) == 10:
            return f"91{digits}"
        elif len(digits) == 12 and digits.startswith("91"):
            return digits
        elif len(digits) > 10 and digits.startswith("0"):
            return f"91{digits[1:]}"
        return digits or "917808611636"

    @property
    def clean_customer_tel(self):
        """Clean phone string for tel: dialing."""
        digits = "".join(filter(str.isdigit, str(self.customer_phone or "")))
        return digits or self.customer_phone

    def get_whatsapp_url(self):
        """Build instant WhatsApp link to Dinesh / Rakesh with pre-filled message."""
        phone = "917808611636"
        msg = (
            f"Hello DRTC Service! I have booked a tank cleaning appointment.\n\n"
            f"*Booking ID:* {self.booking_id}\n"
            f"*Name:* {self.customer_name}\n"
            f"*Phone:* {self.customer_phone}\n"
            f"*Capacity:* {self.custom_capacity or (self.package.capacity if self.package else 'Custom')}\n"
            f"*Date:* {self.preferred_date}\n"
            f"*Slot:* {self.preferred_time_slot}\n"
            f"*Address:* {self.address}, {self.landmark}, {self.area_locality}\n"
            f"*Total:* ₹{self.total_amount}\n\n"
            f"Please confirm my booking slot. Thank you!"
        )
        import urllib.parse
        return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"



class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, default="Tank Cleaning Inquiry")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"Inquiry from {self.name} ({self.phone})"


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100, default="Gamharia, Jamshedpur")
    tank_capacity = models.CharField(max_length=50, default="1000 L Overhead Tank")
    rating = models.PositiveSmallIntegerField(default=5)
    review_title = models.CharField(max_length=120, default="Exceptional Cleaning & Safe Water!")
    comment = models.TextField()
    verified_customer = models.BooleanField(default=True)
    date_added = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"
