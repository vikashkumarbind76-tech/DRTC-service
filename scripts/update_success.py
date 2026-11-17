success_template = '''{% extends 'base.html' %}
{% load static %}

{% block title %}Booking Request Submitted - {{ booking.booking_id }} | DRTC Service{% endblock %}

{% block content %}
<section class="section" style="padding-top: 130px; padding-bottom: 80px; min-height: 85vh; display: flex; align-items: center; justify-content: center; background: #04090e;">
  <div class="container" style="max-width: 680px; width: 100%;">
    <div class="success-card-mockup">
      <!-- Green Checkmark Icon Circle (Exact from Mockup) -->
      <div class="success-circle-check">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.8">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>

      <h1 class="success-title-mockup">BOOKING REQUEST SUBMITTED!</h1>
      <p class="success-desc-mockup">
        Your tank cleaning request has been received. We will contact you soon to confirm the details.
      </p>

      <!-- Reference Box (Exact from Mockup) -->
      <div class="reference-badge-box">
        <span class="ref-label">Reference No.</span>
        <span class="ref-val">{{ booking.booking_id }}</span>
      </div>

      <!-- Action Buttons Row (Exact from Mockup) -->
      <div class="success-actions-row">
        <a href="{% url 'home' %}" class="btn btn-cyan-pill" style="flex: 1; padding: 0.85rem 1.25rem;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          <span>BACK TO HOME</span>
        </a>

        <a href="{% url 'booking_track' %}?booking_id={{ booking.booking_id }}" class="btn btn-outline-pill" style="flex: 1; padding: 0.85rem 1.25rem;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>VIEW MY BOOKINGS</span>
        </a>
      </div>

      <!-- Quick Summary Specs -->
      <div class="success-specs-box">
        <div class="success-spec-row">
          <span>Customer:</span>
          <strong>{{ booking.customer_name }} ({{ booking.customer_phone }})</strong>
        </div>
        <div class="success-spec-row">
          <span>Capacity:</span>
          <strong style="color: #00f0ff;">{{ booking.display_capacity }}</strong>
        </div>
        <div class="success-spec-row">
          <span>Amount:</span>
          <strong style="color: #00f0ff; font-size: 1.15rem;">₹{{ booking.total_amount|floatformat:0 }}</strong>
        </div>
        <div class="success-spec-row">
          <span>Address:</span>
          <span style="text-align: right; max-width: 60%;">{{ booking.address }}</span>
        </div>
      </div>

      {% if whatsapp_url %}
      <div style="margin-top: 1.5rem;">
        <a href="{{ whatsapp_url }}" target="_blank" class="btn btn-outline-pill" style="border-color: rgba(37, 211, 102, 0.4); color: #25d366 !important; width: 100%; justify-content: center;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.664-.698c.993.541 1.956.818 2.801.819 3.178 0 5.767-2.587 5.767-5.766.002-3.181-2.584-5.766-5.772-5.766zm9.969 5.768c0 5.485-4.467 9.953-9.969 9.953-1.748 0-3.376-.452-4.79-1.242l-5.241 1.373 1.4-5.109c-.89-1.488-1.398-3.235-1.398-5.093 0-5.486 4.469-9.953 9.969-9.953 5.486 0 10.029 4.467 10.029 9.953z" />
          </svg>
          <span>Chat on WhatsApp With Dinesh &amp; Rakesh</span>
        </a>
      </div>
      {% endif %}
    </div>
  </div>
</section>
{% endblock %}
'''

with open('templates/booking_success.html', 'w', encoding='utf-8') as f:
    f.write(success_template)

print('Updated booking_success.html successfully!')

