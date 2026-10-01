from django.contrib import admin
from .models import ServicePackage, Booking, ContactInquiry, CustomerReview


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('capacity', 'price', 'original_mrp', 'discount_percent_display', 'duration_mins', 'is_popular', 'order')
    list_editable = ('price', 'original_mrp', 'is_popular', 'order')
    search_fields = ('capacity', 'ideal_for')
    ordering = ('order',)

    def discount_percent_display(self, obj):
        return f"{obj.discount_percent}% OFF"
    discount_percent_display.short_description = "Discount"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id',
        'customer_name',
        'customer_phone',
        'get_capacity_display',
        'total_amount',
        'preferred_date',
        'preferred_time_slot',
        'status',
        'payment_status',
        'created_at'
    )
    list_filter = ('status', 'payment_status', 'preferred_date', 'tank_type')
    search_fields = ('booking_id', 'customer_name', 'customer_phone', 'address', 'landmark')
    list_editable = ('status', 'payment_status')
    date_hierarchy = 'preferred_date'
    readonly_fields = ('booking_id', 'created_at', 'updated_at')

    def get_capacity_display(self, obj):
        return obj.custom_capacity or (obj.package.capacity if obj.package else "Custom")
    get_capacity_display.short_description = "Capacity"


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    list_editable = ('is_resolved',)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'locality', 'tank_capacity', 'rating', 'date_added', 'verified_customer')
    list_filter = ('rating', 'verified_customer', 'date_added')
    search_fields = ('customer_name', 'locality', 'comment')
