from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom admin header and title
admin.site.site_header = "DRTC Service - Operations Dashboard"
admin.site.site_title = "DRTC Admin Portal"
admin.site.index_title = "Dinesh Rakesh Tank Cleaning Service Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drtc_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
