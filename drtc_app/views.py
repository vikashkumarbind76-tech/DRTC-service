import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import ServicePackage, Booking, CustomerReview, ContactInquiry


BUSINESS_INFO = {
    'brand_name': 'DRTC SERVICE',
    'sub_brand': 'DINESH RAKESH TANK CLEANING SERVICE',
    'tagline': 'CLEANER TANKS, SAFER TOMORROW',
    'dinesh_phone': '7808611636',
    'rakesh_phone': '6352561343',
    'email': 'drtcservice@gmail.com',
    'address': 'SHANTINAGAR, GAMHARIA, NEAR BY JHANDA CHOWK',
    'city': 'Gamharia, Jamshedpur',
    'district': 'Seraikela-Kharsawan',
    'state': 'Jharkhand',
    'pincode': '832108',
    'grievance_officer': 'Dinesh Kumar',
    'grievance_email': 'drtcservice@gmail.com',
    'grievance_phone': '+91 7808611636',
    'value_props': [
        {'icon': 'shield-check', 'title': 'Safe Cleaning', 'desc': 'Scientific mechanized cleaning with food-grade disinfectants.'},
        {'icon': 'droplet-check', 'title': 'Hygienic Water', 'desc': 'Germ-free, odor-free, pure drinking water for your loved ones.'},
        {'icon': 'cog-outline', 'title': 'Professional Service', 'desc': 'Trained & certified technicians with heavy-duty safety gear.'},
        {'icon': 'currency-inr', 'title': 'Reliable & Affordable', 'desc': 'Starting at just ₹250. Transparent pricing with zero hidden fees.'},
    ],
}


def home_view(request):
    """Main presentation storefront for DRTC Tank Cleaning Service with live metrics."""
    packages = ServicePackage.objects.all().order_by('order')
    reviews = CustomerReview.objects.all().order_by('-date_added')
    
    total_bookings = Booking.objects.count()
    clean_tanks_delivered = total_bookings
    today = timezone.localdate()
    today_bookings = Booking.objects.filter(preferred_date=today).count()
    active_bookings = Booking.objects.filter(status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']).count()
    cheapest = packages.first()
    starting_price = int(cheapest.price) if cheapest else 250

    business_info = BUSINESS_INFO

    context = {
        'packages': packages,
        'reviews': reviews,
        'business': business_info,
        'today': timezone.now().date(),
        'total_bookings': total_bookings,
        'clean_tanks_delivered': clean_tanks_delivered,
        'today_bookings': today_bookings,
        'active_bookings': active_bookings,
        'starting_price': starting_price,
    }
    return render(request, 'index.html', context)


def api_live_stats(request):
    """Return live real-time booking statistics for dynamic website updates."""
    total_bookings = Booking.objects.count()
    clean_tanks_delivered = total_bookings
    today = timezone.localdate()
    today_bookings = Booking.objects.filter(preferred_date=today).count()
    active_bookings = Booking.objects.filter(status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']).count()

    latest_booking = Booking.objects.order_by('-created_at').first()
    latest_data = None
    if latest_booking:
        parts = latest_booking.customer_name.strip().split()
        masked_name = f"{parts[0]} {parts[-1][0]}." if len(parts) > 1 else (parts[0] if parts else "Customer")
        latest_data = {
            'booking_id': latest_booking.booking_id,
            'customer_name': masked_name,
            'capacity': latest_booking.display_capacity,
            'locality': latest_booking.area_locality or "Gamharia",
            'status': latest_booking.status,
            'status_display': latest_booking.get_status_display(),
            'total_amount': float(latest_booking.total_amount),
        }

    return JsonResponse({
        'status': 'success',
        'total_bookings': total_bookings,
        'clean_tanks_delivered': clean_tanks_delivered,
        'today_bookings': today_bookings,
        'active_bookings': active_bookings,
        'rating': 4.98,
        'starting_price': 250,
        'latest_booking': latest_data,
        'timestamp': timezone.now().isoformat(),
    })


def api_booking_status(request, booking_id):
    """Real-time status endpoint for a specific booking."""
    booking = Booking.objects.filter(booking_id__iexact=booking_id).first()
    if not booking:
        return JsonResponse({'found': False}, status=404)
    return JsonResponse({
        'found': True,
        'booking_id': booking.booking_id,
        'status': booking.status,
        'status_display': booking.get_status_display(),
        'assigned_technician': booking.assigned_technician,
        'preferred_date': str(booking.preferred_date),
        'preferred_time_slot': booking.preferred_time_slot,
        'total_amount': float(booking.total_amount),
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_create_booking(request):
    """Handle booking requests via AJAX or form post."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            # Handle edge-case where client passes dict or raw body with application/x-www-form-urlencoded
            if not data.get('customer_name') and len(data) == 1:
                first_key = list(data.keys())[0]
                if first_key.startswith('{') and first_key.endswith('}'):
                    try:
                        import ast
                        parsed_dict = ast.literal_eval(first_key)
                        if isinstance(parsed_dict, dict):
                            data = parsed_dict
                    except Exception:
                        pass
            if not data.get('customer_name') and request.body:
                try:
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(request.body.decode('utf-8'))
                    if parsed:
                        data = {k: v[0] for k, v in parsed.items()}
                except Exception:
                    pass

        name = str(data.get('customer_name', '')).strip()
        phone = str(data.get('customer_phone', '')).strip()
        address = str(data.get('address', '')).strip()
        package_id = data.get('package_id')
        custom_cap = str(data.get('custom_capacity', '')).strip()
        tank_type = data.get('tank_type', 'OVERHEAD_PVC')
        number_of_tanks = int(data.get('number_of_tanks', 1))
        preferred_date = data.get('preferred_date') or timezone.now().date().isoformat()
        preferred_time_slot = data.get('preferred_time_slot', '08:00 AM - 11:00 AM')
        landmark = str(data.get('landmark', '')).strip()
        area_locality = str(data.get('area_locality', 'Gamharia, Jamshedpur')).strip()
        notes = str(data.get('notes', '')).strip()
        payment_method = data.get('payment_method', 'PAY_ON_SERVICE')

        if not name or not phone or not address:
            return JsonResponse({'status': 'error', 'message': 'Name, Phone and Address are required.'}, status=400)

        package = None
        total = Decimal('0.00')

        if package_id:
            try:
                package = ServicePackage.objects.get(id=package_id)
                total = package.price * number_of_tanks
                if not custom_cap:
                    custom_cap = package.capacity
            except ServicePackage.DoesNotExist:
                pass

        if total == Decimal('0.00'):
            # Fallback estimation based on official DRTC price board (all 25 tiers)
            cap_map = {
                '500':    Decimal('250.00'),
                '1000':   Decimal('400.00'),
                '2000':   Decimal('650.00'),
                '3000':   Decimal('900.00'),
                '5000':   Decimal('1100.00'),
                '8000':   Decimal('1680.00'),
                '10000':  Decimal('2200.00'),
                '15000':  Decimal('3080.00'),
                '20000':  Decimal('3820.00'),
                '25000':  Decimal('4740.00'),
                '30000':  Decimal('5490.00'),
                '40000':  Decimal('6390.00'),
                '45000':  Decimal('7200.00'),
                '50000':  Decimal('7600.00'),
                '60000':  Decimal('8210.00'),
                '65000':  Decimal('9000.00'),
                '70000':  Decimal('9600.00'),
                '80000':  Decimal('11210.00'),
                '85000':  Decimal('13870.00'),
                '90000':  Decimal('15500.00'),
                '100000': Decimal('18780.00'),
                '105000': Decimal('20810.00'),
                '120000': Decimal('25950.00'),
                '125000': Decimal('29590.00'),
                '150000': Decimal('36830.00'),
            }
            matched = False
            # Strip commas/spaces for numeric match
            cap_str = str(custom_cap).replace(',', '').replace(' ', '').replace('L', '').replace('l', '').strip()
            for k, val in cap_map.items():
                if cap_str == k:
                    total = val * number_of_tanks
                    matched = True
                    break
            if not matched:
                # partial match fallback
                for k, val in cap_map.items():
                    if k in str(custom_cap).replace(',', ''):
                        total = val * number_of_tanks
                        matched = True
                        break
            if not matched:
                total = Decimal('400.00') * number_of_tanks

        booking = Booking.objects.create(
            customer_name=name,
            customer_phone=phone,
            package=package,
            custom_capacity=custom_cap,
            tank_type=tank_type,
            number_of_tanks=number_of_tanks,
            total_amount=total,
            preferred_date=preferred_date,
            preferred_time_slot=preferred_time_slot,
            address=address,
            landmark=landmark,
            area_locality=area_locality,
            payment_method=payment_method,
            notes=notes
        )

        whatsapp_url = booking.get_whatsapp_url()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'booking_id': booking.booking_id,
                'total_amount': float(booking.total_amount),
                'customer_name': booking.customer_name,
                'whatsapp_url': whatsapp_url,
                'message': f"Booking #{booking.booking_id} created successfully! Our team will contact you shortly."
            })
        else:
            messages.success(request, f"Booking #{booking.booking_id} submitted! Our team will reach you soon.")
            return redirect('booking_success', booking_id=booking.booking_id)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def booking_success_view(request, booking_id):
    """Confirmation page with digital receipt and direct WhatsApp confirmation."""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, 'booking_success.html', {
        'booking': booking,
        'whatsapp_url': booking.get_whatsapp_url(),
        'dinesh_phone': '7808611636',
        'rakesh_phone': '6352561343',
    })


def booking_track_view(request):
    """Search and track booking status by ID or phone number."""
    query = request.GET.get('q', '').strip()
    booking = None
    not_found = False

    if query:
        booking = Booking.objects.filter(booking_id__iexact=query).first()
        if not booking:
            booking = Booking.objects.filter(customer_phone__icontains=query).first()
        if not booking:
            not_found = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if booking:
            return JsonResponse({
                'found': True,
                'booking_id': booking.booking_id,
                'customer_name': booking.customer_name,
                'capacity': booking.custom_capacity or (booking.package.capacity if booking.package else "Custom"),
                'date': str(booking.preferred_date),
                'slot': booking.preferred_time_slot,
                'status': booking.get_status_display(),
                'status_code': booking.status,
                'total_amount': float(booking.total_amount),
                'technician': booking.assigned_technician,
            })
        else:
            return JsonResponse({'found': False, 'message': 'No booking found matching your criteria.'})

    return render(request, 'booking_track.html', {
        'query': query,
        'booking': booking,
        'not_found': not_found
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_contact(request):
    """Receive contact and emergency inquiry messages."""
    data = request.POST
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
    elif not data.get('name') and len(data) == 1:
        first_key = list(data.keys())[0]
        if first_key.startswith('{') and first_key.endswith('}'):
            try:
                import ast
                parsed_dict = ast.literal_eval(first_key)
                if isinstance(parsed_dict, dict):
                    data = parsed_dict
            except Exception:
                pass
    elif not data.get('name') and request.body:
        try:
            import urllib.parse
            parsed = urllib.parse.parse_qs(request.body.decode('utf-8'))
            if parsed:
                data = {k: v[0] for k, v in parsed.items()}
        except Exception:
            pass

    name = str(data.get('name', '')).strip()
    phone = str(data.get('phone', '')).strip()
    email = str(data.get('email', '')).strip()
    subject = str(data.get('subject', 'General Inquiry')).strip()
    message = str(data.get('message', '')).strip()

    if not name or not phone or not message:
        return JsonResponse({'status': 'error', 'message': 'Name, Phone and Message are required.'}, status=400)

    ContactInquiry.objects.create(
        name=name,
        phone=phone,
        email=email,
        subject=subject,
        message=message
    )

    return JsonResponse({
        'status': 'success',
        'message': 'Thank you! Your message has been received. Dinesh & Rakesh will get back to you immediately.'
    })


def api_calculate_quote(request):
    """Real-time dynamic price calculation based on the official price matrix."""
    capacity = int(request.GET.get('capacity', 1000))
    count = int(request.GET.get('count', 1))
    tank_type = request.GET.get('type', 'OVERHEAD_PVC')

    # Official DRTC price slabs — all 25 individual tiers
    if capacity <= 500:
        base_rate = 250;   duration = 45
    elif capacity <= 1000:
        base_rate = 400;   duration = 60
    elif capacity <= 2000:
        base_rate = 650;   duration = 90
    elif capacity <= 3000:
        base_rate = 900;   duration = 120
    elif capacity <= 5000:
        base_rate = 1100;  duration = 180
    elif capacity <= 8000:
        base_rate = 1680;  duration = 210
    elif capacity <= 10000:
        base_rate = 2200;  duration = 240
    elif capacity <= 15000:
        base_rate = 3080;  duration = 270
    elif capacity <= 20000:
        base_rate = 3820;  duration = 300
    elif capacity <= 25000:
        base_rate = 4740;  duration = 330
    elif capacity <= 30000:
        base_rate = 5490;  duration = 360
    elif capacity <= 40000:
        base_rate = 6390;  duration = 420
    elif capacity <= 45000:
        base_rate = 7200;  duration = 450
    elif capacity <= 50000:
        base_rate = 7600;  duration = 480
    elif capacity <= 60000:
        base_rate = 8210;  duration = 510
    elif capacity <= 65000:
        base_rate = 9000;  duration = 540
    elif capacity <= 70000:
        base_rate = 9600;  duration = 570
    elif capacity <= 80000:
        base_rate = 11210; duration = 600
    elif capacity <= 85000:
        base_rate = 13870; duration = 630
    elif capacity <= 90000:
        base_rate = 15500; duration = 660
    elif capacity <= 100000:
        base_rate = 18780; duration = 720
    elif capacity <= 105000:
        base_rate = 20810; duration = 750
    elif capacity <= 120000:
        base_rate = 25950; duration = 780
    elif capacity <= 125000:
        base_rate = 29590; duration = 840
    else:
        base_rate = 36830; duration = 900

    # Guaranteed official DRTC rates for plastic / PVC / Sintex water tanks
    total = int(round(base_rate * count))
    original_mrp = int(round(total * 1.45))
    savings = original_mrp - total

    return JsonResponse({
        'capacity': capacity,
        'count': count,
        'total': total,
        'original_mrp': original_mrp,
        'savings': savings,
        'estimated_duration_mins': duration * count,
        'price_per_tank': base_rate
    })


def privacy_policy_view(request):
    """Dedicated Privacy Policy page for DRTC Tank Cleaning Service compliant with DPDP Act 2023 & IT Rules."""
    context = {
        'page_title': 'Privacy Policy',
        'last_updated': 'October 4, 2026',
        'business': BUSINESS_INFO,
    }
    return render(request, 'privacy_policy.html', context)


def terms_view(request):
    """Dedicated Terms and Conditions page for DRTC Tank Cleaning Service compliant with Indian law."""
    context = {
        'page_title': 'Terms & Conditions',
        'last_updated': 'October 4, 2026',
        'business': BUSINESS_INFO,
    }
    return render(request, 'terms_and_conditions.html', context)
