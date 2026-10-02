from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom admin header and title
admin.site.site_header = "DRTC Service - Operations Dashboard"
admin.site.site_title = "DRTC Admin Portal"
admin.site.index_title = "Dinesh Rakesh Tank Cleaning Service Management"

from functools import wraps

original_admin_index = admin.site.index

@wraps(original_admin_index)
def drtc_admin_index(request, extra_context=None):
    from drtc_app.models import Booking, ContactInquiry, CustomerReview, ServicePackage
    from django.utils import timezone
    from django.db.models import Sum

    today = timezone.localdate()
    total_bookings = Booking.objects.count()
    today_bookings = Booking.objects.filter(preferred_date=today).count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    active_jobs = Booking.objects.filter(status__in=['CONFIRMED', 'TECHNICIAN_ASSIGNED', 'IN_PROGRESS']).count()
    completed_jobs = Booking.objects.filter(status='COMPLETED').count()
    total_revenue = Booking.objects.filter(status='COMPLETED').aggregate(total=Sum('total_amount'))['total'] or 0
    unresolved_inquiries = ContactInquiry.objects.filter(is_resolved=False).count()
    recent_bookings = Booking.objects.select_related('package')[:8]
    packages_count = ServicePackage.objects.count()
    reviews_count = CustomerReview.objects.count()

    kpi = {
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'pending_bookings': pending_bookings,
        'active_jobs': active_jobs,
        'completed_jobs': completed_jobs,
        'total_revenue': int(total_revenue),
        'unresolved_inquiries': unresolved_inquiries,
        'recent_bookings': recent_bookings,
        'packages_count': packages_count,
        'reviews_count': reviews_count,
        'today_str': timezone.now().strftime("%A, %d %B %Y"),
        'today_iso': today.isoformat(),
    }
    context = extra_context or {}
    context['kpi'] = kpi
    return original_admin_index(request, extra_context=context)

admin.site.index = drtc_admin_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drtc_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
