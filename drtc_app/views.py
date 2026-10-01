import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import ServicePackage, Booking, CustomerReview, ContactInquiry


def home_view(request):
    """Main presentation storefront for DRTC Tank Cleaning Service."""
    packages = ServicePackage.objects.all().order_by('order')
    reviews = CustomerReview.objects.all().order_by('-date_added')
    
    # Context data reflecting the media provided by user
    business_info = {
        'brand_name': 'DRTC SERVICE',
        'sub_brand': 'DINESH RAKESH TANK CLEANING SERVICE',
        'tagline': 'CLEANER TANKS, SAFER TOMORROW',
        'dinesh_phone': '7808611636',
        'rakesh_phone': '6352561343',
        'email': 'arjunraja20022@gmail.com',
        'address': 'SHANTINAGAR, GAMHARIA, NEAR BY JHANDA CHOWK',
        'city': 'Gamharia, Jamshedpur',
        'pincode': '832108',
        'value_props': [
            {'icon': 'shield-check', 'title': 'Safe Cleaning', 'desc': 'Scientific 6-stage mechanized cleaning with food-grade disinfectants.'},
            {'icon': 'droplet-check', 'title': 'Hygienic Water', 'desc': 'Germ-free, odor-free, pure drinking water for your loved ones.'},
            {'icon': 'cog-outline', 'title': 'Professional Service', 'desc': 'Trained & certified technicians with heavy-duty safety gear.'},
            {'icon': 'currency-inr', 'title': 'Reliable & Affordable', 'desc': 'Starting at just ₹250. Transparent pricing with zero hidden fees.'},
        ],
        'cleaning_stages': [
            {
                'step': '01',
                'title': 'Mechanized Dewatering',
                'desc': 'Emptying stale contaminated water using high-capacity submersible drainage pumps without damaging internal plumbing.',
                'tag': 'Rapid Drainage'
            },
            {
                'step': '02',
                'title': 'Sludge & Silt Extraction',
                'desc': 'High-pressure slurry pumps extract thick settling mud, algae, sand, and decomposing organic sediment from the base.',
                'tag': 'Heavy Mud Removal'
            },
            {
                'step': '03',
                'title': 'High Pressure Rotary Jet Scrub',
                'desc': 'Industrial rotary jet nozzles blast the tank ceiling, vertical corrugated walls, and joints at 150+ bar pressure.',
                'tag': 'Deep Wall Descaling'
            },
            {
                'step': '04',
                'title': 'Industrial Slurry Vacuuming',
                'desc': 'Heavy-duty wet industrial vacuum suction extracts all remaining suspended particles and microscopic residue.',
                'tag': 'Zero Residue'
            },
            {
                'step': '05',
                'title': 'Food-Grade Anti-Bacterial Spray',
                'desc': 'Specialized non-toxic, odorless, food-safe antibacterial solution sterilizes surfaces against fungi, spores, and biofilm.',
                'tag': 'Eco-Friendly Disinfection'
            },
            {
                'step': '06',
                'title': 'UV Germicidal Radiation Treatment',
                'desc': 'Medical-grade Ultraviolet (UV) germicidal radiator is exposed to eliminate dormant bacteria, viruses, and microbial pathogens.',
                'tag': '100% Germ-Free Safe'
            },
        ]
    }

    context = {
        'packages': packages,
        'reviews': reviews,
        'business': business_info,
        'today': timezone.now().date(),
    }
    return render(request, 'index.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def api_create_booking(request):
    """Handle booking requests via AJAX or form post."""
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get('customer_name', '').strip()
        phone = data.get('customer_phone', '').strip()
        address = data.get('address', '').strip()
        package_id = data.get('package_id')
        custom_cap = data.get('custom_capacity', '').strip()
        tank_type = data.get('tank_type', 'OVERHEAD_PVC')
        number_of_tanks = int(data.get('number_of_tanks', 1))
        preferred_date = data.get('preferred_date') or timezone.now().date().isoformat()
        preferred_time_slot = data.get('preferred_time_slot', '08:00 AM - 11:00 AM')
        landmark = data.get('landmark', '').strip()
        area_locality = data.get('area_locality', 'Gamharia, Jamshedpur').strip()
        notes = data.get('notes', '').strip()
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
            # Fallback estimation based on official price board
            cap_map = {
                '500': Decimal('250.00'),
                '1000': Decimal('400.00'),
                '2000': Decimal('650.00'),
                '3000': Decimal('900.00'),
                '5000': Decimal('1100.00'),
            }
            matched = False
            for k, val in cap_map.items():
                if k in str(custom_cap):
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
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', 'General Inquiry').strip()
    message = request.POST.get('message', '').strip()

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

    # Price slabs directly from DRTC board:
    # 500L: 250, 1000L: 400, 2000L: 650, 3000L: 900, 5000L: 1100
    if capacity <= 500:
        base_rate = 250
        duration = 45
    elif capacity <= 1000:
        base_rate = 400
        duration = 60
    elif capacity <= 2000:
        base_rate = 650
        duration = 90
    elif capacity <= 3000:
        base_rate = 900
        duration = 120
    else:
        # Scale for 5000L or bigger
        base_rate = 1100 + ((capacity - 5000) // 1000) * 200 if capacity > 5000 else 1100
        duration = 180

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
