import os

# 1. READ ORIGINAL INDEX TO KEEP CALCULATOR, VIDEO, REVIEWS, FAQ
with open('templates/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract extra_css block
extra_css_idx = orig.find('{% block extra_css %}')
extra_css_end = orig.find('{% endblock %}', extra_css_idx)
extra_css_block = orig[extra_css_idx:extra_css_end + len('{% endblock %}')]

# Extract calculator box
calc_start = orig.find('<!-- =================================================================\n         INTERACTIVE DYNAMIC CALCULATOR')
if calc_start == -1:
    calc_start = orig.find('<div class="calculator-box" id="calculator">')
calc_end = orig.find('<!-- =================================================================\n     SERVICE OVERVIEW & PROCESS VIDEO')
if calc_end != -1:
    calc_block = orig[calc_start:calc_end].strip()
else:
    calc_block = ""

# Extract video to reviews to faq
video_start = orig.find('<!-- =================================================================\n     SERVICE OVERVIEW & PROCESS VIDEO')
contact_start = orig.find('<!-- =================================================================\n     CONTACT & DIRECT ACTION SECTION')
if video_start != -1 and contact_start != -1:
    middle_legacy = orig[video_start:contact_start].strip()
else:
    middle_legacy = ""

# Extract extra_js
extra_js_idx = orig.find('{% block extra_js %}')
extra_js_block = orig[extra_js_idx:]

complete_index = f'''{{% extends 'base.html' %}}
{{% load static %}}

{extra_css_block}

{{% block content %}}
<!-- =================================================================
     PANEL 1: HERO SECTION (EXACT FIGMA MOCKUP REPLICA)
     ================================================================= -->
<section class="hero-clean-section" id="home">
  <!-- Giant Background Watermark -->
  <div class="section-watermark">CLEAN WATER</div>

  <div class="container">
    <div class="hero-clean-grid">
      <!-- Left Column: Content -->
      <div class="hero-text-col">
        <div class="hero-tagline">DINESH RAKESH TANK CLEANING SERVICE</div>

        <h1 class="hero-headline-clean">
          PROFESSIONAL WATER<br>
          TANK CLEANING FOR A<br>
          <span class="text-cyan-neon">CLEANER, SAFER TOMORROW.</span>
        </h1>

        <p class="hero-desc-clean">
          Protect your water quality with professional tank cleaning services. We help maintain cleaner storage tanks and a healthier environment through reliable cleaning solutions.
        </p>

        <div class="hero-actions-row">
          <a href="#booking" class="btn btn-cyan-pill open-booking-modal-btn" data-capacity="1000 L">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>BOOK TANK CLEANING</span>
          </a>

          <a href="#services" class="btn btn-outline-pill">
            <span>VIEW OUR SERVICES</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </a>
        </div>

        <!-- 4 Feature Pills in a row -->
        <div class="hero-feature-pills">
          <div class="hero-feature-pill">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
              <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
            </svg>
            <span>Improved Water Quality</span>
          </div>

          <div class="hero-feature-pill">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              <polyline points="9 12 11 14 15 10"></polyline>
            </svg>
            <span>Hygienic Cleaning</span>
          </div>

          <div class="hero-feature-pill">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7.5" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
            <span>Reliable Service</span>
          </div>

          <div class="hero-feature-pill">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            <span>Transparent Pricing</span>
          </div>
        </div>
      </div>

      <!-- Right Column: Visual Tank Showcase -->
      <div class="hero-visual-col">
        <div class="hero-visual-card">
          <img src="{{% static 'images/hero_tank_splash.jpg' %}}" alt="DRTC Professional Water Tank Cleaning Hero" class="hero-visual-img">
        </div>
      </div>
    </div>

    <!-- Mouse Scroll Down Indicator -->
    <a href="#services" class="scroll-down-wrap">
      <div class="mouse-pill">
        <div class="mouse-dot"></div>
      </div>
      <span class="scroll-label">SCROLL DOWN</span>
    </a>
  </div>
</section>

<!-- =================================================================
     PANEL 2: OUR SERVICES - PROFESSIONAL TANK CLEANING SERVICES (6 CARDS)
     ================================================================= -->
<section class="services-clean-section" id="services">
  <div class="section-watermark">OUR SERVICES</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">OUR SERVICES</span>
      <h2 class="section-title-clean">PROFESSIONAL TANK CLEANING SERVICES</h2>
      <p class="section-desc-clean">
        Comprehensive cleaning solutions for all types of water tanks.
      </p>
    </div>

    <!-- 6 Service Cards Grid (3x2) -->
    <div class="service-cards-grid">
      <!-- 1. Tank Cleaning Service -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/gallery_1.jpg' %}}" alt="Tank Cleaning Service" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Tank Cleaning Service</h3>
          <p class="service-card-desc">Complete cleaning and disinfection of water tanks.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="1000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- 2. Deep Cleaning -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/gallery_2.jpg' %}}" alt="Deep Cleaning" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Deep Cleaning</h3>
          <p class="service-card-desc">Removal of dirt, sludge and harmful deposits.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="1000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- 3. Maintenance Service -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/gallery_3.jpg' %}}" alt="Maintenance Service" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Maintenance Service</h3>
          <p class="service-card-desc">Regular cleaning to maintain water quality.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="1000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- 4. Residential Tank Cleaning -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/svc_residential.jpg' %}}" alt="Residential Tank Cleaning" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Residential Tank Cleaning</h3>
          <p class="service-card-desc">Safe and hygienic cleaning for homes and apartments.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="1000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- 5. Commercial Tank Cleaning -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/svc_commercial.jpg' %}}" alt="Commercial Tank Cleaning" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Commercial Tank Cleaning</h3>
          <p class="service-card-desc">Professional cleaning for offices, shops and buildings.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="2000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- 6. Industrial Tank Cleaning -->
      <div class="service-card-clean">
        <div class="service-card-img-wrap">
          <img src="{{% static 'images/svc_industrial.jpg' %}}" alt="Industrial Tank Cleaning" class="service-card-img">
        </div>
        <div class="service-card-content">
          <h3 class="service-card-title">Industrial Tank Cleaning</h3>
          <p class="service-card-desc">High-capacity tank cleaning with advanced methods.</p>
          <a href="#booking" class="btn btn-cyan-pill service-card-btn open-booking-modal-btn" data-capacity="5000 L">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     PANEL 3: SERVICE PRICING - CHOOSE YOUR TANK CAPACITY (3 TOP + 2 BOTTOM + BANNER)
     ================================================================= -->
<section class="services-clean-section" id="pricing" style="background: #03080e;">
  <div class="section-watermark">SERVICE PRICING</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">SERVICE PRICING</span>
      <h2 class="section-title-clean">CHOOSE YOUR TANK CAPACITY</h2>
    </div>

    <div class="pricing-split-layout">
      <!-- Top Row of 3 Cards (500L, 1000L, 2000L) -->
      <div class="pricing-top-3">
        <!-- 500 L -->
        <div class="capacity-card">
          <div class="capacity-card-img-wrap">
            <img src="{{% static 'images/tanks/tank_500.png' %}}" alt="500 L Tank Cleaning" class="capacity-card-img">
          </div>
          <div class="capacity-card-size">500 L</div>
          <div class="capacity-card-label">TANK CAPACITY</div>
          <div class="capacity-card-price">₹250</div>
          <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="500 L" data-package-id="1">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>

        <!-- 1000 L (Featured) -->
        <div class="capacity-card" style="border-color: rgba(0, 240, 255, 0.55); box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 30px rgba(0, 210, 255, 0.25);">
          <div class="capacity-card-img-wrap">
            <img src="{{% static 'images/tanks/tank_1000.png' %}}" alt="1000 L Tank Cleaning" class="capacity-card-img">
          </div>
          <div class="capacity-card-size">1000 L</div>
          <div class="capacity-card-label">TANK CAPACITY</div>
          <div class="capacity-card-price">₹400</div>
          <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="1000 L" data-package-id="2">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>

        <!-- 2000 L -->
        <div class="capacity-card">
          <div class="capacity-card-img-wrap">
            <img src="{{% static 'images/tanks/tank_2000.png' %}}" alt="2000 L Tank Cleaning" class="capacity-card-img">
          </div>
          <div class="capacity-card-size">2000 L</div>
          <div class="capacity-card-label">TANK CAPACITY</div>
          <div class="capacity-card-price">₹650</div>
          <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="2000 L" data-package-id="3">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- Bottom Row of 2 Cards (3000L, 5000L) -->
      <div class="pricing-bottom-2">
        <!-- 3000 L -->
        <div class="capacity-card">
          <div class="capacity-card-img-wrap">
            <img src="{{% static 'images/tanks/tank_3000.png' %}}" alt="3000 L Tank Cleaning" class="capacity-card-img">
          </div>
          <div class="capacity-card-size">3000 L</div>
          <div class="capacity-card-label">TANK CAPACITY</div>
          <div class="capacity-card-price">₹900</div>
          <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="3000 L" data-package-id="4">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>

        <!-- 5000 L -->
        <div class="capacity-card">
          <div class="capacity-card-img-wrap">
            <img src="{{% static 'images/tanks/tank_5000.png' %}}" alt="5000 L Tank Cleaning" class="capacity-card-img">
          </div>
          <div class="capacity-card-size">5000 L</div>
          <div class="capacity-card-label">TANK CAPACITY</div>
          <div class="capacity-card-price">₹1100</div>
          <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="5000 L" data-package-id="5">
            <span>BOOK NOW &rarr;</span>
          </a>
        </div>
      </div>

      <!-- Transparent & Fair Pricing Banner -->
      <div class="pricing-fair-banner">
        <div class="fair-banner-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
        </div>
        <div>
          <div class="fair-banner-title">Transparent &amp; Fair Pricing</div>
          <div class="fair-banner-sub">No hidden charges, high-quality cleaning at the best price.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     WHY CHOOSE DRTC SERVICE SECTION
     ================================================================= -->
<section class="why-clean-section" id="why-us">
  <div class="section-watermark">WHY CHOOSE US</div>

  <div class="container">
    <div class="section-header-center">
      <h2 class="section-title-clean">
        WHY CHOOSE <span class="text-cyan-neon">DRTC SERVICE?</span>
      </h2>
      <p class="section-desc-clean">
        Reliable, hygienic and professional tank cleaning services you can trust.
      </p>
    </div>

    <!-- 6 Cards Grid -->
    <div class="why-clean-grid">
      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
          </svg>
        </div>
        <h3 class="why-title">Professional Tank Cleaning</h3>
        <p class="why-desc">Thorough and effective cleaning for cleaner tanks.</p>
      </div>

      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <circle cx="12" cy="12" r="9"></circle>
            <path d="M12 6v6l4 2"></path>
            <path d="M12 3a9 9 0 0 1 9 9"></path>
          </svg>
        </div>
        <h3 class="why-title">Focus on Hygiene</h3>
        <p class="why-desc">Helps maintain safe and clean water storage.</p>
      </div>

      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <polyline points="9 12 11 14 15 10"></polyline>
          </svg>
        </div>
        <h3 class="why-title">Reliable Service</h3>
        <p class="why-desc">On-time and dependable service experience.</p>
      </div>

      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
        </div>
        <h3 class="why-title">Transparent Pricing</h3>
        <p class="why-desc">Clear tank capacity and service price with no hidden cost.</p>
      </div>

      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
        </div>
        <h3 class="why-title">Customer Convenience</h3>
        <p class="why-desc">Easy and quick booking process online.</p>
      </div>

      <div class="why-card">
        <div class="why-icon-box">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
            <path d="M12 12a3 3 0 0 0 3 3"></path>
          </svg>
        </div>
        <h3 class="why-title">Cleaner Water Storage</h3>
        <p class="why-desc">Supports healthier water for your daily needs.</p>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     PANEL 5: ABOUT DRTC SERVICE (CLEANER TANKS. SAFER TOMORROW.)
     ================================================================= -->
<section class="about-clean-section" id="about">
  <div class="section-watermark">ABOUT DRTC</div>

  <div class="container">
    <div class="about-split-grid">
      <!-- Left: Big Tank Image -->
      <div class="about-tank-card">
        <img src="{{% static 'images/hero_tank_splash.jpg' %}}" alt="DRTC Service Black Water Tank" class="about-tank-img">
      </div>

      <!-- Right: Story & Values -->
      <div class="about-content-col">
        <span class="section-tag-cyan">ABOUT DRTC SERVICE</span>
        <h2 class="section-title-clean" style="text-align: left; margin-bottom: 1.5rem;">
          CLEANER TANKS.<br><span class="text-cyan-neon">SAFER TOMORROW.</span>
        </h2>

        <div class="about-story-box">
          <h3 class="about-section-heading">Our Story</h3>
          <p class="about-story-text">
            DRTC SERVICE (Dinesh Rakesh Tank Cleaning Service) provides professional water tank cleaning solutions for homes, commercial and industrial needs.
          </p>
        </div>

        <div class="about-values-box">
          <h3 class="about-section-heading">Our Values</h3>
          <div class="about-values-grid">
            <div class="about-value-badge">
              <div class="about-value-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                  <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                </svg>
              </div>
              <span class="about-value-name">Hygiene</span>
            </div>

            <div class="about-value-badge">
              <div class="about-value-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  <polyline points="9 12 11 14 15 10"></polyline>
                </svg>
              </div>
              <span class="about-value-name">Reliability</span>
            </div>

            <div class="about-value-badge">
              <div class="about-value-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                </svg>
              </div>
              <span class="about-value-name">Customer First</span>
            </div>

            <div class="about-value-badge">
              <div class="about-value-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                  <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                  <polyline points="2 17 12 22 22 17"></polyline>
                  <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
              </div>
              <span class="about-value-name">Transparent Service</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     PANEL 4: BOOKING SECTION (WITH BOTTOM 4 FEATURE BADGES)
     ================================================================= -->
<section class="booking-clean-section" id="booking">
  <div class="section-watermark">BOOKING</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">BOOK A SERVICE</span>
      <h2 class="section-title-clean">BOOK YOUR TANK CLEANING</h2>
      <p class="section-desc-clean">
        Fill in the details below to request a tank cleaning service.
      </p>
    </div>

    <div class="booking-split-grid">
      <!-- Left: Form Card -->
      <div class="booking-form-card">
        <form id="inlineBookingForm" method="POST" action="{{% url 'api_create_booking' %}}">
          {{% csrf_token %}}
          <input type="hidden" id="inline-package-id" name="package_id" value="">

          <div class="form-row-2col">
            <div class="form-group-custom">
              <label class="form-label-clean" for="inline-customer-name">Full Name <span style="color: #ef4444;">*</span></label>
              <div class="input-with-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                <input type="text" id="inline-customer-name" name="customer_name" class="clean-input" placeholder="Enter your name" required>
              </div>
            </div>

            <div class="form-group-custom">
              <label class="form-label-clean" for="inline-customer-phone">Phone Number <span style="color: #ef4444;">*</span></label>
              <div class="input-with-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
                <input type="tel" id="inline-customer-phone" name="customer_phone" class="clean-input" placeholder="Enter mobile number" required>
              </div>
            </div>
          </div>

          <div class="form-group-custom">
            <label class="form-label-clean" for="inline-capacity-select">Tank Capacity <span style="color: #ef4444;">*</span></label>
            <div class="select-with-icon">
              <select name="custom_capacity" id="inline-capacity-select" class="clean-select" required>
                <option value="" disabled>Select tank capacity</option>
                <option value="500 L">500 L (₹250)</option>
                <option value="1000 L" selected>1000 L (₹400) ★ Most Popular</option>
                <option value="2000 L">2000 L (₹650)</option>
                <option value="3000 L">3000 L (₹900)</option>
                <option value="5000 L">5000 L (₹1100)</option>
                <option value="8000 L">8000 L (₹1680)</option>
                <option value="10,000 L">10,000 L (₹2200)</option>
                <option value="15,000 L">15,000 L (₹3080)</option>
                <option value="20,000 L">20,000 L (₹3820)</option>
                <option value="25,000 L">25,000 L (₹4740)</option>
                <option value="30,000 L">30,000 L (₹5490)</option>
                <option value="40,000 L">40,000 L (₹6390)</option>
                <option value="50,000 L">50,000 L (₹7600)</option>
                <option value="1,00,000 L">1,00,000 L (₹18780)</option>
              </select>
            </div>
          </div>

          <div class="form-group-custom">
            <label class="form-label-clean" for="inline-address">Address <span style="color: #ef4444;">*</span></label>
            <textarea id="inline-address" name="address" class="clean-textarea" placeholder="Enter your complete address" rows="3" required></textarea>
          </div>

          <button type="submit" class="btn btn-cyan-pill" style="width: 100%; padding: 0.95rem; font-size: 0.95rem;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>CONFIRM BOOKING</span>
          </button>
        </form>
      </div>

      <!-- Right: Pricing Sidebar Card -->
      <div class="pricing-summary-card">
        <div class="pricing-summary-header">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
          </svg>
          <span>SERVICE PRICING</span>
        </div>

        <div class="pricing-summary-list">
          <div class="pricing-row-item">
            <span class="pricing-item-cap">500 L</span>
            <span class="pricing-item-rate">₹250</span>
          </div>
          <div class="pricing-row-item">
            <span class="pricing-item-cap">1000 L</span>
            <span class="pricing-item-rate">₹400</span>
          </div>
          <div class="pricing-row-item">
            <span class="pricing-item-cap">2000 L</span>
            <span class="pricing-item-rate">₹650</span>
          </div>
          <div class="pricing-row-item">
            <span class="pricing-item-cap">3000 L</span>
            <span class="pricing-item-rate">₹900</span>
          </div>
          <div class="pricing-row-item">
            <span class="pricing-item-cap">5000 L</span>
            <span class="pricing-item-rate">₹1100</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom 4 Feature Badges (Exact from Mockup) -->
    <div class="booking-bottom-badges">
      <div class="booking-badge-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          <polyline points="9 12 11 14 15 10"></polyline>
        </svg>
        <span>Safe &amp; Hygienic</span>
      </div>

      <div class="booking-badge-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
        <span>Professional Team</span>
      </div>

      <div class="booking-badge-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        <span>On-time Service</span>
      </div>

      <div class="booking-badge-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00d2d3" stroke-width="2.2">
          <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
          <polyline points="9 12 11 14 15 10"></polyline>
        </svg>
        <span>Quality Cleaning</span>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     GALLERY SECTION (4 PHOTOS)
     ================================================================= -->
<section class="gallery-clean-section" id="gallery">
  <div class="section-watermark">OUR GALLERY</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">OUR WORK</span>
      <h2 class="section-title-clean">GALLERY</h2>
      <p class="section-desc-clean">
        A look at our tank cleaning work.
      </p>
    </div>

    <!-- 4 High-Resolution Photo Cards Grid -->
    <div class="gallery-photo-grid">
      <div class="gallery-photo-card">
        <img src="{{% static 'images/gallery_1.jpg' %}}" alt="DRTC Technician Cleaning Muddy Tank" class="gallery-img">
      </div>
      <div class="gallery-photo-card">
        <img src="{{% static 'images/gallery_2.jpg' %}}" alt="Deep Clean Water Tank With Turquoise Water" class="gallery-img">
      </div>
      <div class="gallery-photo-card">
        <img src="{{% static 'images/gallery_3.jpg' %}}" alt="DRTC Service Black Water Tank on Rooftop" class="gallery-img">
      </div>
      <div class="gallery-photo-card">
        <img src="{{% static 'images/gallery_4.jpg' %}}" alt="Sanitized Clean Tank Floor Squeegee Cleaned" class="gallery-img">
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     PANEL 6: CONTACT US - DIRECT CONTACTS & ENQUIRY FORM
     ================================================================= -->
<section class="contact-clean-section" id="contact">
  <div class="section-watermark">CONTACT US</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">CONTACT US</span>
      <h2 class="section-title-clean">GET IN TOUCH FOR BOOKING OR ANY ENQUIRY</h2>
    </div>

    <div class="contact-split-grid">
      <!-- Left: Direct Contacts Card -->
      <div class="contact-details-card">
        <!-- Call -->
        <div class="contact-row-entry">
          <div class="contact-entry-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
          </div>
          <div>
            <div class="contact-entry-label">Call Us</div>
            <div class="contact-entry-val"><a href="tel:7808611636">+91 7808611636</a> / <a href="tel:6352561343">6352561343</a></div>
          </div>
        </div>

        <!-- WhatsApp -->
        <div class="contact-row-entry">
          <div class="contact-entry-icon" style="color: #25d366; border-color: rgba(37, 211, 102, 0.3); background: rgba(37, 211, 102, 0.08);">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.664-.698c.993.541 1.956.818 2.801.819 3.178 0 5.767-2.587 5.767-5.766.002-3.181-2.584-5.766-5.772-5.766zm9.969 5.768c0 5.485-4.467 9.953-9.969 9.953-1.748 0-3.376-.452-4.79-1.242l-5.241 1.373 1.4-5.109c-.89-1.488-1.398-3.235-1.398-5.093 0-5.486 4.469-9.953 9.969-9.953 5.486 0 10.029 4.467 10.029 9.953z" />
            </svg>
          </div>
          <div>
            <div class="contact-entry-label">WhatsApp</div>
            <div class="contact-entry-val"><a href="https://wa.me/917808611636" target="_blank">+91 7808611636</a></div>
          </div>
        </div>

        <!-- Email -->
        <div class="contact-row-entry">
          <div class="contact-entry-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </div>
          <div>
            <div class="contact-entry-label">Email Us</div>
            <div class="contact-entry-val"><a href="mailto:drtcservice@gmail.com">drtcservice@gmail.com</a></div>
          </div>
        </div>

        <!-- Service Area -->
        <div class="contact-row-entry">
          <div class="contact-entry-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
          </div>
          <div>
            <div class="contact-entry-label">Service Area</div>
            <div class="contact-entry-val">Gamharia, Jamshedpur &amp; Adityapur, Jharkhand</div>
          </div>
        </div>
      </div>

      <!-- Right: Send an Enquiry Card -->
      <div class="contact-enquiry-card">
        <h3 class="enquiry-card-title">Send an Enquiry</h3>

        <form id="contactForm">
          {{% csrf_token %}}
          <div class="form-group-custom">
            <input type="text" id="inq-name" name="name" class="clean-input" placeholder="Your Name" style="padding-left: 1rem;" required>
          </div>

          <div class="form-group-custom">
            <input type="tel" id="inq-phone" name="phone" class="clean-input" placeholder="Phone Number" style="padding-left: 1rem;" required>
          </div>

          <div class="form-group-custom">
            <textarea id="inq-msg" name="message" class="clean-textarea" placeholder="Your Message" rows="3" required></textarea>
          </div>

          <button type="submit" class="btn btn-cyan-pill" style="width: 100%; padding: 0.85rem; justify-content: center;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            <span>SEND ENQUIRY</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</section>

<!-- =================================================================
     ADVANCED MULTI-TANK ESTIMATOR & CALCULATOR (EXPANDABLE)
     ================================================================= -->
<section class="section" style="padding-top: 3.5rem; background: #03080e;">
  <div class="container">
    {calc_block}
  </div>
</section>

{middle_legacy}

{{% endblock %}}

{extra_js_block}
'''

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(complete_index)

print('Updated index.html with all sections matching the full mockup board!')

