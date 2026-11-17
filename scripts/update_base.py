import re

# Update base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace brand
old_brand_pat = re.compile(r'<!-- Two-Tone Wordmark Brand Identity with Official Logo -->.*?</a>', re.DOTALL)
new_brand = '''<!-- Brand Identity (Exact from Mockup) -->
      <a href="{% url 'home' %}" class="brand-wordmark" title="DRTC Service Home">
        <div class="brand-text-block">
          <div class="brand-title">
            <span class="brand-drtc-exact">DRTC SERVICE</span>
          </div>
          <span class="brand-subtext-cyan">DINESH RAKESH TANK CLEANING SERVICE</span>
        </div>
      </a>'''
content = old_brand_pat.sub(new_brand, content, count=1)

# Replace nav links
old_links_pat = re.compile(r'<!-- Desktop Nav Links -->\s*<ul class="nav-links">.*?</ul>', re.DOTALL)
new_links = '''<!-- Desktop Nav Links (Exact from Mockup) -->
      <ul class="nav-links">
        <li><a href="{% url 'home' %}#home"
            class="nav-link {% if request.resolver_match.url_name == 'home' %}active{% endif %}">Home</a></li>
        <li><a href="{% url 'home' %}#services" class="nav-link">Services</a></li>
        <li><a href="{% url 'home' %}#pricing" class="nav-link">Pricing</a></li>
        <li><a href="{% url 'home' %}#gallery" class="nav-link">Gallery</a></li>
        <li><a href="{% url 'home' %}#about" class="nav-link">About</a></li>
        <li><a href="{% url 'home' %}#contact" class="nav-link">Contact</a></li>
        <li><a href="{% url 'booking_track' %}"
            class="nav-link {% if request.resolver_match.url_name == 'booking_track' %}active{% endif %}">Track</a></li>
      </ul>'''
content = old_links_pat.sub(new_links, content, count=1)

# Replace action CTA button in navbar
old_btn_pat = re.compile(r'<button class="btn btn-primary btn-sm open-booking-modal-btn"[^>]*>.*?</button>', re.DOTALL)
new_btn = '''<a href="#booking" class="btn btn-cyan-pill open-booking-modal-btn" data-capacity="1000 L" style="padding: 0.5rem 1.25rem; font-size: 0.82rem;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>BOOK NOW</span>
        </a>'''
content = old_btn_pat.sub(new_btn, content, count=1)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('base.html updated successfully!')
