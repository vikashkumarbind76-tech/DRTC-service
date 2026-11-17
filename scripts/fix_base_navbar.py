with open('templates/base.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate from '<!-- ==========================================================================\n     SECTION 1 — TOP INFORMATION BAR'
# up to '</nav>'
start_marker = '<!-- ==========================================================================\n     SECTION 1 — TOP INFORMATION BAR'
if start_marker not in text:
    start_marker = '<div class="top-info-bar">'

start_pos = text.find(start_marker)
end_marker = '</nav>'
end_pos = text.find(end_marker, start_pos) + len(end_marker)

print(f"Replacing from index {start_pos} to {end_pos}")

new_navbar = """<!-- ==========================================================================
     MAIN NAVIGATION (Exact Match to Figma Mockup)
     ========================================================================== -->
<header class="navbar" id="mainNavbar">
  <div class="container nav-inner">
    <a href="{% url 'home' %}" class="brand-wordmark" title="DRTC Service Home">
      <div class="brand-text-block">
        <div class="brand-title">
          <span style="color: #ffffff; font-weight: 800; font-size: 1.35rem; letter-spacing: 0.04em;">DRTC SERVICE</span>
        </div>
        <span style="color: #00d2d3; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;">DINESH RAKESH TANK CLEANING SERVICE</span>
      </div>
    </a>

    <!-- Desktop Navigation Links (Exact from Mockup) -->
    <ul class="nav-links">
      <li><a href="{% url 'home' %}#home" class="nav-link active">Home</a></li>
      <li><a href="{% url 'home' %}#services" class="nav-link">Services</a></li>
      <li><a href="{% url 'home' %}#pricing" class="nav-link">Pricing</a></li>
      <li><a href="{% url 'home' %}#gallery" class="nav-link">Gallery</a></li>
      <li><a href="{% url 'home' %}#about" class="nav-link">About</a></li>
      <li><a href="{% url 'home' %}#contact" class="nav-link">Contact</a></li>
    </ul>

    <!-- Action CTA button in navbar -->
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <a href="{% url 'home' %}#booking" class="btn btn-cyan-pill open-booking-modal-btn" data-capacity="1000 L" style="padding: 0.52rem 1.35rem; font-size: 0.82rem;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        <span>BOOK NOW</span>
      </a>

      <button class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Toggle navigation menu" style="display: none; background: transparent; border: none; color: #00d2d3; cursor: pointer;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
</header>"""

updated_text = text[:start_pos] + new_navbar + text[end_pos:]

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(updated_text)

print("templates/base.html updated successfully!")
