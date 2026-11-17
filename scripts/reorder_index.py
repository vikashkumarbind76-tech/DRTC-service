import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Define the 5-card row section for Panel 1 Part B
panel1_part_b = """
<!-- =================================================================
     PANEL 1 (Part B): OUR SERVICES & PRICING - TANK CLEANING SERVICES (5 CARDS ROW)
     ================================================================= -->
<section class="services-clean-section" id="quick-pricing" style="padding-top: 4rem; padding-bottom: 4rem; border-top: 1px solid rgba(0, 240, 255, 0.12); border-bottom: 1px solid rgba(0, 240, 255, 0.12); background: #03080e;">
  <div class="section-watermark">OUR SERVICES</div>

  <div class="container">
    <div class="section-header-center">
      <span class="section-tag-cyan">OUR SERVICES &amp; PRICING</span>
      <h2 class="section-title-clean">TANK CLEANING SERVICES</h2>
      <p class="section-desc-clean">
        Choose your tank capacity and book a professional cleaning service at a transparent price.
      </p>
    </div>

    <!-- 5 Tank Capacity Cards in one 5-column row -->
    <div class="capacity-cards-row">
      <!-- 500 L -->
      <div class="capacity-card">
        <div class="capacity-card-img-wrap">
          <img src="{% static 'images/tanks/tank_500.png' %}" alt="500 L Tank Cleaning" class="capacity-card-img">
        </div>
        <div class="capacity-card-size">500 L</div>
        <div class="capacity-card-label">TANK CAPACITY</div>
        <div class="capacity-card-price">&#8377;250</div>
        <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="500 L" data-package-id="1">
          <span>BOOK NOW &rarr;</span>
        </a>
      </div>

      <!-- 1000 L (Featured) -->
      <div class="capacity-card" style="border-color: rgba(0, 240, 255, 0.55); box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 30px rgba(0, 210, 255, 0.25);">
        <div class="capacity-card-img-wrap">
          <img src="{% static 'images/tanks/tank_1000.png' %}" alt="1000 L Tank Cleaning" class="capacity-card-img">
        </div>
        <div class="capacity-card-size">1000 L</div>
        <div class="capacity-card-label">TANK CAPACITY</div>
        <div class="capacity-card-price">&#8377;400</div>
        <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="1000 L" data-package-id="2">
          <span>BOOK NOW &rarr;</span>
        </a>
      </div>

      <!-- 2000 L -->
      <div class="capacity-card">
        <div class="capacity-card-img-wrap">
          <img src="{% static 'images/tanks/tank_2000.png' %}" alt="2000 L Tank Cleaning" class="capacity-card-img">
        </div>
        <div class="capacity-card-size">2000 L</div>
        <div class="capacity-card-label">TANK CAPACITY</div>
        <div class="capacity-card-price">&#8377;650</div>
        <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="2000 L" data-package-id="3">
          <span>BOOK NOW &rarr;</span>
        </a>
      </div>

      <!-- 3000 L -->
      <div class="capacity-card">
        <div class="capacity-card-img-wrap">
          <img src="{% static 'images/tanks/tank_3000.png' %}" alt="3000 L Tank Cleaning" class="capacity-card-img">
        </div>
        <div class="capacity-card-size">3000 L</div>
        <div class="capacity-card-label">TANK CAPACITY</div>
        <div class="capacity-card-price">&#8377;900</div>
        <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="3000 L" data-package-id="4">
          <span>BOOK NOW &rarr;</span>
        </a>
      </div>

      <!-- 5000 L -->
      <div class="capacity-card">
        <div class="capacity-card-img-wrap">
          <img src="{% static 'images/tanks/tank_5000.png' %}" alt="5000 L Tank Cleaning" class="capacity-card-img">
        </div>
        <div class="capacity-card-size">5000 L</div>
        <div class="capacity-card-label">TANK CAPACITY</div>
        <div class="capacity-card-price">&#8377;1100</div>
        <a href="#booking" class="btn btn-cyan-pill card-btn open-booking-modal-btn" data-capacity="5000 L" data-package-id="5">
          <span>BOOK NOW &rarr;</span>
        </a>
      </div>
    </div>
  </div>
</section>
"""

# Let's extract sections cleanly:
# 1. Everything up to end of hero-clean-section (closing </section>)
hero_end_marker = '</section>'
hero_pos = text.find('class="hero-clean-section"')
if hero_pos != -1:
    hero_section_end = text.find('</section>', hero_pos) + len('</section>')
    header_and_hero = text[:hero_section_end]
    rest = text[hero_section_end:]
    print("Found hero section end at", hero_section_end)

# Let's find why-clean-section
why_pos = text.find('<section class="why-clean-section"')
why_end = text.find('</section>', why_pos) + len('</section>')
why_section = text[why_pos:why_end]

# Let's find services-clean-section id="services" (Panel 2)
services_pos = text.find('<section class="services-clean-section" id="services">')
services_end = text.find('</section>', services_pos) + len('</section>')
services_section = text[services_pos:services_end]

# Let's find pricing section id="pricing" (Panel 3)
pricing_pos = text.find('<section class="services-clean-section" id="pricing"')
pricing_end = text.find('</section>', pricing_pos) + len('</section>')
pricing_section = text[pricing_pos:pricing_end]

# Let's find about section id="about" (Panel 5)
about_pos = text.find('<section class="about-clean-section" id="about">')
about_end = text.find('</section>', about_pos) + len('</section>')
about_section = text[about_pos:about_end]

# Let's find booking section id="booking" (Panel 4)
booking_pos = text.find('<section class="booking-clean-section" id="booking">')
booking_end = text.find('</section>', booking_pos) + len('</section>')
booking_section = text[booking_pos:booking_end]

# Let's find gallery section id="gallery"
gallery_pos = text.find('<section class="gallery-clean-section" id="gallery">')
gallery_end = text.find('</section>', gallery_pos) + len('</section>')
gallery_section = text[gallery_pos:gallery_end]

# Let's find contact section id="contact" (Panel 6)
contact_pos = text.find('<section class="contact-clean-section" id="contact">')
contact_end = text.find('</section>', contact_pos) + len('</section>')
contact_section = text[contact_pos:contact_end]

# Remainder of the template from after contact section
remainder = text[contact_end:]

# Now assemble in the exact order:
# 1. header_and_hero (Panel 1 Part A)
# 2. panel1_part_b (Panel 1 Part B - 5 capacity cards row)
# 3. why_section (Panel 1 Part C - 6 why choose us cards)
# 4. services_section (Panel 2 - 6 service category cards)
# 5. pricing_section (Panel 3 - 3+2 cards + fair pricing banner)
# 6. about_section (Panel 5 - About DRTC)
# 7. booking_section (Panel 4 - Booking form + pricing sidebar + 4 badges)
# 8. gallery_section (Gallery 4 photos)
# 9. contact_section (Panel 6 - Contact details + enquiry form)
# 10. remainder (Calculator, Reviews, FAQ, Modals, Footer, Scripts)

new_text = (
    header_and_hero + "\n\n" +
    panel1_part_b + "\n\n" +
    why_section + "\n\n" +
    services_section + "\n\n" +
    pricing_section + "\n\n" +
    about_section + "\n\n" +
    booking_section + "\n\n" +
    gallery_section + "\n\n" +
    contact_section + "\n\n" +
    remainder
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Successfully reassembled templates/index.html with exact 9-panel flow!")
