import csv
import urllib.parse
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import ServicePackage, Booking, ContactInquiry, CustomerReview


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = (
        'capacity_display',
        'price_display',
        'mrp_display',
        'savings_display',
        'duration_display',
        'popularity_display',
        'order',
    )
    list_editable = ('order',)
    search_fields = ('capacity', 'ideal_for', 'badge_text')
    ordering = ('order', 'capacity_liters')
    fieldsets = (
        ("Package Identity", {
            "fields": ("capacity", "capacity_liters", "badge_text", "is_popular", "order")
        }),
        ("Pricing & Economics", {
            "fields": ("price", "original_mrp", "ideal_for", "duration_mins")
        }),
        ("Service Features & Specifications", {
            "fields": ("features_list",)
        }),
    )

    def capacity_display(self, obj):
        badge = f' <span class="drtc-badge amber" style="font-size:0.68rem; margin-left:6px;">{obj.badge_text}</span>' if obj.badge_text else ''
        return format_html(
            '<div style="font-weight:700; color:#ffffff; font-size:0.95rem;">{} {}'
            '<small style="display:block; color:#94a3b8; font-weight:400; font-size:0.75rem;">{}</small></div>',
            obj.capacity,
            mark_safe(badge),
            obj.ideal_for or ""
        )
    capacity_display.short_description = "Capacity / Package"

    def price_display(self, obj):
        return format_html(
            '<span style="font-family:\'JetBrains Mono\',monospace; font-size:1.05rem; font-weight:800; color:#fbbf24;">₹{}</span>',
            int(obj.price)
        )
    price_display.short_description = "DRTC Rate"

    def mrp_display(self, obj):
        if obj.original_mrp:
            return format_html(
                '<span style="text-decoration:line-through; color:#64748b; font-size:0.85rem;">₹{}</span>',
                int(obj.original_mrp)
            )
        return "-"
    mrp_display.short_description = "Market MRP"

    def savings_display(self, obj):
        if obj.discount_percent > 0:
            return format_html(
                '<span class="drtc-badge emerald">SAVE {}% (₹{})</span>',
                obj.discount_percent,
                obj.savings
            )
        return mark_safe('<span style="color:#64748b;">Standard</span>')
    savings_display.short_description = "Discount"

    def duration_display(self, obj):
        return format_html(
            '<span style="color:#cbd5e1;">⏱️ ~{} mins</span>',
            obj.duration_mins
        )
    duration_display.short_description = "Est. Time"

    def popularity_display(self, obj):
        if obj.is_popular:
            return mark_safe('<span class="drtc-badge cyan">★ MOST POPULAR</span>')
        return mark_safe('<span style="color:#64748b; font-size:0.75rem;">Standard Tier</span>')
    popularity_display.short_description = "Badge"


class OperationalStatusFilter(admin.SimpleListFilter):
    """Instant filter for critical daily operational buckets."""
    title = 'Operational Status'
    parameter_name = 'operational_status'

    def lookups(self, request, model_admin):
        return (
            ('today', "📅 Today's Schedule"),
            ('pending', "⏳ Pending Confirmation"),
            ('active', "⚡ Active Jobs (Confirmed / In-Progress)"),
            ('completed', "🏆 Completed Jobs"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'today':
            return queryset.filter(preferred_date=timezone.localdate())
        elif val == 'pending':
            return queryset.filter(status='PENDING')
        elif val == 'active':
            return queryset.filter(status__in=['CONFIRMED', 'TECHNICIAN_ASSIGNED', 'IN_PROGRESS'])
        elif val == 'completed':
            return queryset.filter(status='COMPLETED')
        return queryset


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id_display',
        'customer_display',
        'contact_actions',
        'service_display',
        'schedule_display',
        'amount_display',
        'status_pill',
        'payment_pill',
        'created_at_display',
    )
    list_filter = (
        OperationalStatusFilter,
        'status',
        'payment_status',
        'tank_type',
        'preferred_date',
        'payment_method',
    )
    search_fields = (
        'booking_id',
        'customer_name',
        'customer_phone',
        'customer_email',
        'address',
        'landmark',
        'area_locality',
    )
    date_hierarchy = 'preferred_date'
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'whatsapp_quick_dispatch')
    actions = [
        'mark_as_confirmed',
        'mark_as_in_progress',
        'mark_as_completed',
        'mark_as_paid',
        'export_bookings_csv',
    ]

    fieldsets = (
        ("📋 Booking & Quick Dispatch", {
            "fields": (
                ("booking_id", "status"),
                ("created_at", "updated_at"),
                "whatsapp_quick_dispatch",
            )
        }),
        ("👤 Customer Details", {
            "fields": (
                ("customer_name", "customer_phone"),
                "customer_email",
            )
        }),
        ("💧 Tank & Service Specifications", {
            "fields": (
                ("package", "custom_capacity"),
                ("tank_type", "number_of_tanks"),
            )
        }),
        ("📅 Schedule & Field Assignment", {
            "fields": (
                ("preferred_date", "preferred_time_slot"),
                "assigned_technician",
            )
        }),
        ("📍 Service Location & Address", {
            "fields": (
                "address",
                ("landmark", "area_locality", "pincode"),
            )
        }),
        ("💰 Financials & Billing", {
            "fields": (
                ("total_amount", "payment_status"),
                "payment_method",
            )
        }),
        ("📝 Operations Notes", {
            "fields": ("notes",),
            "classes": ("collapse",)
        }),
    )

    def booking_id_display(self, obj):
        return format_html(
            '<div style="font-family:\'JetBrains Mono\',monospace; font-weight:700; color:#fbbf24; background:rgba(245,158,11,0.12); padding:4px 8px; border-radius:6px; border:1px solid rgba(245,158,11,0.3); display:inline-block;">'
            '#{}</div>',
            obj.booking_id
        )
    booking_id_display.short_description = "Booking ID"

    def customer_display(self, obj):
        return format_html(
            '<div style="font-weight:700; color:#ffffff;">{}</div>'
            '<div style="font-size:0.75rem; color:#94a3b8;">📍 {}</div>',
            obj.customer_name,
            obj.landmark or obj.area_locality
        )
    customer_display.short_description = "Customer & Location"

    def contact_actions(self, obj):
        wa_text = urllib.parse.quote(
            f"Hello {obj.customer_name}, this is DRTC Tank Cleaning regarding your booking #{obj.booking_id} scheduled for {obj.preferred_date}."
        )
        wa_url = f"https://wa.me/{obj.clean_customer_phone}?text={wa_text}"
        call_url = f"tel:{obj.clean_customer_tel}"

        return format_html(
            '<div style="display:flex; gap:6px; align-items:center;">'
            '<a href="{}" target="_blank" class="drtc-btn-action wa" title="WhatsApp Customer">'
            '💬 WhatsApp</a>'
            '<a href="{}" class="drtc-btn-action call" title="Call Customer">'
            '📞 Call</a>'
            '</div>',
            wa_url,
            call_url
        )
    contact_actions.short_description = "Instant Contact"

    def service_display(self, obj):
        cap = obj.custom_capacity or (obj.package.capacity if obj.package else "Custom")
        return format_html(
            '<div style="font-weight:600; color:#38bdf8;">{}</div>'
            '<small style="color:#64748b;">{} (Qty: {})</small>',
            cap,
            obj.get_tank_type_display(),
            obj.number_of_tanks
        )
    service_display.short_description = "Tank & Capacity"

    def schedule_display(self, obj):
        today = timezone.localdate()
        is_today = obj.preferred_date == today
        date_badge = '<span class="drtc-badge amber" style="font-size:0.65rem; margin-left:4px;">TODAY</span>' if is_today else ''
        return format_html(
            '<div style="font-weight:600; color:#f1f5f9;">{} {}</div>'
            '<small style="color:#94a3b8;">{}</small>',
            obj.preferred_date.strftime("%d %b %Y"),
            mark_safe(date_badge),
            obj.preferred_time_slot
        )
    schedule_display.short_description = "Scheduled Slot"

    def amount_display(self, obj):
        return format_html(
            '<span style="font-family:\'JetBrains Mono\',monospace; font-weight:800; color:#fbbf24; font-size:0.95rem;">₹{}</span>',
            int(obj.total_amount)
        )
    amount_display.short_description = "Amount"

    def status_pill(self, obj):
        colors = {
            'PENDING': 'amber',
            'CONFIRMED': 'cyan',
            'TECHNICIAN_ASSIGNED': 'purple',
            'IN_PROGRESS': 'purple',
            'COMPLETED': 'emerald',
            'CANCELLED': 'rose',
        }
        color = colors.get(obj.status, 'cyan')
        return format_html(
            '<span class="drtc-badge {}"><span class="drtc-dot"></span>{}</span>',
            color,
            obj.get_status_display()
        )
    status_pill.short_description = "Service Status"

    def payment_pill(self, obj):
        if obj.payment_status == 'PAID':
            return mark_safe('<span class="drtc-badge emerald">✓ PAID</span>')
        return mark_safe('<span class="drtc-badge amber">⏳ UNPAID</span>')
    payment_pill.short_description = "Payment"

    def created_at_display(self, obj):
        return format_html(
            '<span style="color:#64748b; font-size:0.78rem;">{}</span>',
            obj.created_at.strftime("%d %b, %H:%M")
        )
    created_at_display.short_description = "Booked At"

    def whatsapp_quick_dispatch(self, obj):
        if not obj.pk:
            return "Save record first to generate dispatch link."
        wa_url = obj.get_whatsapp_url()
        return format_html(
            '<a href="{}" target="_blank" class="drtc-btn-action wa" style="padding:8px 16px; font-size:0.9rem;">'
            '💬 Launch Dispatch WhatsApp Message to Customer &amp; Technician'
            '</a>',
            wa_url
        )
    whatsapp_quick_dispatch.short_description = "Dispatch Hub"

    # --- Batch Operations Actions ---
    @admin.action(description="⚡ Mark selected as Confirmed & Scheduled")
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        self.message_user(request, f"{updated} booking(s) marked as Confirmed.")

    @admin.action(description="🔧 Mark selected as Cleaning In Progress")
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f"{updated} booking(s) marked as In Progress.")

    @admin.action(description="🏆 Mark selected as Service Completed")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} booking(s) marked as Completed.")

    @admin.action(description="💰 Mark payment as Paid in Full")
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status='PAID')
        self.message_user(request, f"{updated} booking(s) marked as Paid.")

    @admin.action(description="📥 Export selected bookings to CSV")
    def export_bookings_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="drtc_bookings_{timezone.localdate()}.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Booking ID', 'Customer Name', 'Phone', 'Email',
            'Capacity', 'Tank Type', 'Scheduled Date', 'Time Slot',
            'Address', 'Landmark', 'Amount', 'Status', 'Payment'
        ])
        for b in queryset:
            writer.writerow([
                b.booking_id, b.customer_name, b.customer_phone, b.customer_email or '',
                b.custom_capacity or (b.package.capacity if b.package else ''),
                b.get_tank_type_display(), b.preferred_date, b.preferred_time_slot,
                b.address, b.landmark, b.total_amount, b.status, b.payment_status
            ])
        return response


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_actions', 'email_display', 'subject', 'status_badge', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    actions = ['mark_resolved', 'mark_unresolved']

    def phone_actions(self, obj):
        wa_url = f"https://wa.me/91{obj.phone}?text=Hello%20{urllib.parse.quote(obj.name)},%20this%20is%20DRTC%20Tank%20Cleaning."
        return format_html(
            '<div style="display:flex; gap:6px; align-items:center;">'
            '<span style="font-weight:600; color:#ffffff;">{}</span>'
            '<a href="{}" target="_blank" class="drtc-btn-action wa">💬 WhatsApp</a>'
            '<a href="tel:{}" class="drtc-btn-action call">📞</a>'
            '</div>',
            obj.phone,
            wa_url,
            obj.phone
        )
    phone_actions.short_description = "Phone & WhatsApp"

    def email_display(self, obj):
        if obj.email:
            return format_html('<a href="mailto:{}" style="color:#38bdf8;">{}</a>', obj.email, obj.email)
        return "-"
    email_display.short_description = "Email"

    def status_badge(self, obj):
        if obj.is_resolved:
            return mark_safe('<span class="drtc-badge emerald">✓ RESOLVED</span>')
        return mark_safe('<span class="drtc-badge amber">⏳ OPEN LEAD</span>')
    status_badge.short_description = "Resolution"

    @admin.action(description="Mark selected inquiries as Resolved")
    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, "Selected inquiries marked as Resolved.")

    @admin.action(description="Mark selected inquiries as Open")
    def mark_unresolved(self, request, queryset):
        queryset.update(is_resolved=False)
        self.message_user(request, "Selected inquiries marked as Open.")


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'locality', 'tank_capacity', 'stars_display', 'verified_badge', 'date_added')
    list_filter = ('rating', 'verified_customer', 'date_added')
    search_fields = ('customer_name', 'locality', 'comment', 'review_title')

    def stars_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color:#fbbf24; font-size:1.1rem; letter-spacing:1px;">{}</span> <small style="color:#94a3b8;">({}/5)</small>',
            stars,
            obj.rating
        )
    stars_display.short_description = "Customer Rating"

    def verified_badge(self, obj):
        if obj.verified_customer:
            return mark_safe('<span class="drtc-badge emerald">✓ Verified Customer</span>')
        return mark_safe('<span style="color:#64748b;">Unverified</span>')
    verified_badge.short_description = "Verification"
