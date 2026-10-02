/**
 * DRTC SERVICE - Dinesh Rakesh Tank Cleaning Service
 * Interactive Frontend Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
  initScrollSpy();
  initCalculator();
  initBookingModal();
  initLightbox();
  initContactForm();
  init3DTilt();
  initHeroBubbles();
  initCardSpotlight();
  initBeforeAfterSlider();
  initCounters();
  initButtonRipples();
  initScrollReveal();
});

/* ----------------------------------------------------
   1. Navbar Scroll Effect & Mobile Nav
   ---------------------------------------------------- */
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar');
  const toggleBtn = document.querySelector('.mobile-menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  });

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isActive = navLinks.classList.toggle('active');
      toggleBtn.classList.toggle('active');
      toggleBtn.setAttribute('aria-expanded', isActive ? 'true' : 'false');
      toggleBtn.innerHTML = isActive 
        ? `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`
        : `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
    });

    // Close on link click
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        toggleBtn.classList.remove('active');
        toggleBtn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
      });
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!navLinks.contains(e.target) && !toggleBtn.contains(e.target) && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        toggleBtn.classList.remove('active');
        toggleBtn.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
      }
    });
  }
}

/* ----------------------------------------------------
   1b. Dynamic Navbar ScrollSpy & Sliding Active Indicator
   ---------------------------------------------------- */
function initScrollSpy() {
  const navLinksContainer = document.querySelector('.nav-links');
  if (!navLinksContainer) return;

  const navLinks = Array.from(navLinksContainer.querySelectorAll('.nav-link'));
  if (navLinks.length === 0) return;

  // Create sliding yellow indicator if not already present
  let indicator = navLinksContainer.querySelector('.nav-indicator');
  if (!indicator) {
    indicator = document.createElement('span');
    indicator.className = 'nav-indicator';
    navLinksContainer.appendChild(indicator);
  }
  navLinksContainer.classList.add('has-indicator');

  // Update position and width of the sliding indicator
  function updateIndicator(targetLink) {
    if (!targetLink || window.innerWidth <= 900) {
      if (indicator) indicator.style.opacity = '0';
      return;
    }

    const containerRect = navLinksContainer.getBoundingClientRect();
    const linkRect = targetLink.getBoundingClientRect();

    if (linkRect.width === 0) return;

    const left = linkRect.left - containerRect.left;
    const width = linkRect.width;

    indicator.style.transform = `translateX(${left}px)`;
    indicator.style.width = `${width}px`;
    indicator.style.opacity = '1';
  }

  // Get current active link
  function getActiveLink() {
    return navLinksContainer.querySelector('.nav-link.active') || navLinks[0];
  }

  // Set active class on target link and smoothly move indicator
  function setActiveLink(activeEl) {
    if (!activeEl) return;
    navLinks.forEach(link => {
      if (link === activeEl) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
    updateIndicator(activeEl);
  }

  // Hover preview: indicator smoothly glides to hovered link, returns to active on leave
  navLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
      if (window.innerWidth > 900) {
        updateIndicator(link);
      }
    });
  });

  navLinksContainer.addEventListener('mouseleave', () => {
    if (window.innerWidth > 900) {
      updateIndicator(getActiveLink());
    }
  });

  // Re-align on resize
  window.addEventListener('resize', () => {
    updateIndicator(getActiveLink());
  }, { passive: true });

  // Re-align after font load
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => {
      updateIndicator(getActiveLink());
    });
  }

  // Map homepage sections
  const sectionIds = ['home', 'pricing', 'reviews', 'contact'];
  const sections = sectionIds
    .map(id => document.getElementById(id))
    .filter(Boolean);

  // If no sections on current page (e.g. /booking/track/), position indicator on active link and stop
  if (sections.length === 0) {
    updateIndicator(getActiveLink());
    return;
  }

  let isManualScrolling = false;
  let manualScrollTimer = null;

  function onScroll() {
    if (isManualScrolling) return;

    const scrollY = window.scrollY || window.pageYOffset;
    const windowHeight = window.innerHeight;
    const docHeight = document.documentElement.scrollHeight;

    // Bottom of the page: activate Contact
    if (scrollY + windowHeight >= docHeight - 70) {
      const contactLink = navLinks.find(link => (link.getAttribute('href') || '').endsWith('#contact'));
      if (contactLink) setActiveLink(contactLink);
      return;
    }

    // ScrollSpy trigger threshold
    const navbarOffset = 130;
    let currentSectionId = sections[0].id;

    for (let i = 0; i < sections.length; i++) {
      const sec = sections[i];
      if (scrollY + navbarOffset >= sec.offsetTop) {
        currentSectionId = sec.id;
      }
    }

    const currentLink = navLinks.find(link => (link.getAttribute('href') || '').endsWith('#' + currentSectionId));
    if (currentLink && !currentLink.classList.contains('active')) {
      setActiveLink(currentLink);
    }
  }

  // Smooth scroll and immediate active state transfer on nav link clicks
  navLinks.forEach(link => {
    const href = link.getAttribute('href') || '';
    const hashIndex = href.indexOf('#');
    if (hashIndex !== -1) {
      const targetId = href.substring(hashIndex + 1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        link.addEventListener('click', (e) => {
          const currentPath = window.location.pathname.replace(/\/$/, '');
          const linkPath = href.substring(0, hashIndex).replace(/\/$/, '');

          if (!linkPath || linkPath === currentPath) {
            e.preventDefault();

            setActiveLink(link);

            isManualScrolling = true;
            clearTimeout(manualScrollTimer);

            const navbarHeight = 75;
            const targetTop = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

            window.scrollTo({
              top: Math.max(0, targetTop),
              behavior: 'smooth'
            });

            if (history.pushState) {
              history.pushState(null, '', '#' + targetId);
            }

            manualScrollTimer = setTimeout(() => {
              isManualScrolling = false;
              onScroll();
            }, 800);
          }
        });
      }
    }
  });

  // Passive throttled scroll listener
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        onScroll();
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // Initial sync
  const hash = window.location.hash.replace('#', '');
  if (hash && document.getElementById(hash)) {
    const matchedLink = navLinks.find(link => (link.getAttribute('href') || '').endsWith('#' + hash));
    if (matchedLink) {
      setActiveLink(matchedLink);
    } else {
      updateIndicator(getActiveLink());
    }
  } else {
    onScroll();
    updateIndicator(getActiveLink());
  }

  setTimeout(() => {
    updateIndicator(getActiveLink());
  }, 100);
  setTimeout(() => {
    updateIndicator(getActiveLink());
  }, 400);
}

/* ----------------------------------------------------
   2. Interactive Dynamic Calculator
   ---------------------------------------------------- */
function initCalculator() {
  const pills = document.querySelectorAll('.capacity-pill');
  const countSelect = document.getElementById('calc-count');
  
  const totalDisplay = document.getElementById('calc-total-display');
  const mrpDisplay = document.getElementById('calc-mrp-display');
  const savingsDisplay = document.getElementById('calc-savings-display');
  const durationDisplay = document.getElementById('calc-duration-display');
  const perTankDisplay = document.getElementById('calc-per-tank-display');
  const calcBookBtn = document.getElementById('calc-book-btn');
  const calcWhatsAppBtn = document.getElementById('calc-whatsapp-btn');

  let currentCapacity = 1000;

  function updateCalculator() {
    const count = parseInt(countSelect?.value || '1', 10);
    const tankType = 'OVERHEAD_PVC';

    // Official DRTC rates:
    // 500L: 250, 1000L: 400, 2000L: 650, 3000L: 900, 5000L: 1100
    let baseRate = 400;
    let baseDuration = 60;

    if (currentCapacity <= 500) {
      baseRate = 250;
      baseDuration = 45;
    } else if (currentCapacity <= 1000) {
      baseRate = 400;
      baseDuration = 60;
    } else if (currentCapacity <= 2000) {
      baseRate = 650;
      baseDuration = 90;
    } else if (currentCapacity <= 3000) {
      baseRate = 900;
      baseDuration = 120;
    } else {
      baseRate = 1100 + Math.floor((currentCapacity - 5000) / 1000) * 200;
      baseDuration = 180;
    }

    const finalPerTank = baseRate;
    const finalTotal = finalPerTank * count;
    const originalMrp = Math.round(finalTotal * 1.45);
    const savings = originalMrp - finalTotal;
    const totalDuration = baseDuration * count;

    if (totalDisplay) totalDisplay.textContent = `₹${finalTotal}`;
    if (mrpDisplay) mrpDisplay.textContent = `₹${originalMrp}`;
    if (savingsDisplay) savingsDisplay.textContent = `You Save ₹${savings} (31% OFF)`;
    if (durationDisplay) durationDisplay.textContent = `${totalDuration} Minutes`;
    if (perTankDisplay) perTankDisplay.textContent = `₹${finalPerTank} / tank`;

    // Update WhatsApp link
    if (calcWhatsAppBtn) {
      const msg = `Hello Dinesh & Rakesh (DRTC Service), I want to clean ${count} plastic tank(s) of ${currentCapacity}L. Estimated Quote: ₹${finalTotal}. Please contact me to confirm a slot.`;
      calcWhatsAppBtn.href = `https://wa.me/917808611636?text=${encodeURIComponent(msg)}`;
    }

    // Pass data to booking modal trigger
    if (calcBookBtn) {
      calcBookBtn.setAttribute('data-capacity', `${currentCapacity} L`);
      calcBookBtn.setAttribute('data-count', count);
      calcBookBtn.setAttribute('data-type', tankType);
      calcBookBtn.setAttribute('data-total', finalTotal);
    }
  }

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentCapacity = parseInt(pill.getAttribute('data-liters') || '1000', 10);
      updateCalculator();
    });
  });

  countSelect?.addEventListener('change', updateCalculator);

  // Initial calculation
  updateCalculator();
}

/* ----------------------------------------------------
   3. Booking Modal & Flow
   ---------------------------------------------------- */
function initBookingModal() {
  const modal = document.getElementById('bookingModal');
  const closeBtn = document.getElementById('closeBookingModal');
  const form = document.getElementById('bookingForm');
  const openButtons = document.querySelectorAll('.open-booking-modal-btn');

  const capInput = document.getElementById('modal-package-cap');
  const pkgIdInput = document.getElementById('modal-package-id');
  const typeSelect = document.getElementById('modal-tank-type');
  const countInput = document.getElementById('modal-tank-count');

  function openModal(data = {}) {
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';

      if (data.capacity && capInput) capInput.value = data.capacity;
      if (data.packageId && pkgIdInput) pkgIdInput.value = data.packageId;
      if (data.type && typeSelect) typeSelect.value = data.type;
      if (data.count && countInput) countInput.value = data.count;
    }
  }

  function closeModal() {
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const capacity = btn.getAttribute('data-capacity') || '1000 L';
      const packageId = btn.getAttribute('data-package-id') || '';
      const type = btn.getAttribute('data-type') || 'OVERHEAD_PVC';
      const count = btn.getAttribute('data-count') || '1';
      openModal({ capacity, packageId, type, count });
    });
  });

  closeBtn?.addEventListener('click', closeModal);
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // AJAX Booking Form Submission
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = `<span>Booking Appointment...</span>`;
    submitBtn.disabled = true;

    const formData = new FormData(form);

    try {
      const response = await fetch('/api/booking/create/', {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      const result = await response.json();

      if (response.ok && result.status === 'success') {
        closeModal();
        showBookingSuccessModal(result);
        form.reset();
      } else {
        showToast(result.message || 'Error creating booking. Please try again.', 'error');
      }
    } catch (err) {
      console.error(err);
      showToast('Network error. Please call Dinesh at 7808611636 directly.', 'error');
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
}

/* ----------------------------------------------------
   4. Booking Success Modal Card
   ---------------------------------------------------- */
function showBookingSuccessModal(data) {
  const successModal = document.getElementById('bookingSuccessModal');
  const idEl = document.getElementById('success-booking-id');
  const nameEl = document.getElementById('success-customer-name');
  const totalEl = document.getElementById('success-total-amount');
  const waBtn = document.getElementById('success-whatsapp-btn');
  const closeBtn = document.getElementById('closeSuccessModal');

  if (idEl) idEl.textContent = data.booking_id;
  if (nameEl) nameEl.textContent = data.customer_name;
  if (totalEl) totalEl.textContent = `₹${data.total_amount}`;
  if (waBtn) waBtn.href = data.whatsapp_url;

  if (successModal) {
    successModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  closeBtn?.addEventListener('click', () => {
    successModal?.classList.remove('active');
    document.body.style.overflow = '';
  });
}

/* ----------------------------------------------------
   5. Official Media Proof Lightbox
   ---------------------------------------------------- */
function initLightbox() {
  const lightbox = document.getElementById('imageLightboxModal');
  const lightboxImg = document.getElementById('lightbox-preview-img');
  const closeBtn = document.getElementById('closeLightboxModal');
  const triggers = document.querySelectorAll('.proof-image-container');

  triggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const img = trigger.querySelector('.proof-img');
      if (img && lightbox && lightboxImg) {
        lightboxImg.src = img.src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  function closeLightbox() {
    lightbox?.classList.remove('active');
    document.body.style.overflow = '';
  }

  closeBtn?.addEventListener('click', closeLightbox);
  lightbox?.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });
}

/* ----------------------------------------------------
   6. Contact Inquiry Form
   ---------------------------------------------------- */
function initContactForm() {
  const form = document.getElementById('contactForm');
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const orig = btn.innerHTML;
    btn.innerHTML = 'Sending Message...';
    btn.disabled = true;

    const formData = new FormData(form);

    try {
      const res = await fetch('/api/contact/', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      const data = await res.json();
      if (res.ok && data.status === 'success') {
        showToast(data.message, 'success');
        form.reset();
      } else {
        showToast(data.message || 'Failed to submit inquiry.', 'error');
      }
    } catch (err) {
      showToast('Network error. You can directly call Dinesh at 7808611636.', 'error');
    } finally {
      btn.innerHTML = orig;
      btn.disabled = false;
    }
  });
}

/* ----------------------------------------------------
   7. 3D Tilt Effect on Desktop Pointer Hover
   ---------------------------------------------------- */
function init3DTilt() {
  if (window.matchMedia('(pointer: coarse)').matches) return; // Touch devices skip

  const cards = document.querySelectorAll('.hero-image-card');

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = ((y - centerY) / centerY) * -7;
      const rotateY = ((x - centerX) / centerX) * 7;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  });
}

/* ----------------------------------------------------
   8. Toast Notification Utility
   ---------------------------------------------------- */
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <div style="flex-grow: 1;">${message}</div>
    <button style="background:none; border:none; color:#94a3b8; cursor:pointer;" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s';
    setTimeout(() => toast.remove(), 400);
  }, 4500);
}

/* ----------------------------------------------------
   9. Floating Water Droplets & Bubbles Particle Canvas
   ---------------------------------------------------- */
function initHeroBubbles() {
  const canvas = document.getElementById('heroBubbleCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = canvas.parentElement.offsetWidth);
  let height = (canvas.height = canvas.parentElement.offsetHeight);

  window.addEventListener('resize', () => {
    if (!canvas.parentElement) return;
    width = canvas.width = canvas.parentElement.offsetWidth;
    height = canvas.height = canvas.parentElement.offsetHeight;
  });

  const mouse = { x: -1000, y: -1000 };
  window.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });

  const bubbles = [];
  const bubbleCount = Math.min(38, Math.floor(width / 32));

  for (let i = 0; i < bubbleCount; i++) {
    bubbles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 4.5 + 1.5,
      speedY: Math.random() * 0.7 + 0.35,
      speedX: (Math.random() - 0.5) * 0.4,
      opacity: Math.random() * 0.35 + 0.15,
      hue: Math.random() > 0.4 ? '195' : '210', // electric cyan or deep azure blue
      pulse: Math.random() * Math.PI,
      pulseSpeed: Math.random() * 0.03 + 0.015,
    });
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < bubbles.length; i++) {
      const b = bubbles[i];
      b.y -= b.speedY;
      b.x += Math.sin(b.pulse) * 0.45;
      b.pulse += b.pulseSpeed;

      // Soft mouse repel
      const dx = b.x - mouse.x;
      const dy = b.y - mouse.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 120) {
        const force = (120 - dist) / 120;
        b.x += (dx / dist) * force * 2.2;
        b.y += (dy / dist) * force * 2.2;
      }

      // Reset when top reached
      if (b.y < -10) {
        b.y = height + 10;
        b.x = Math.random() * width;
      }
      if (b.x < -10) b.x = width + 10;
      if (b.x > width + 10) b.x = -10;

      // Draw glowing water bubble
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
      if (b.hue === '195') {
        ctx.fillStyle = `rgba(0, 210, 255, ${b.opacity})`;
        ctx.shadowColor = 'rgba(0, 210, 255, 0.45)';
      } else {
        ctx.fillStyle = `rgba(2, 132, 199, ${b.opacity * 0.9})`;
        ctx.shadowColor = 'rgba(2, 132, 199, 0.4)';
      }
      ctx.shadowBlur = 8;
      ctx.fill();

      // Specular highlight on bubble
      ctx.beginPath();
      ctx.arc(b.x - b.radius * 0.3, b.y - b.radius * 0.3, b.radius * 0.35, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${b.opacity + 0.25})`;
      ctx.shadowBlur = 0;
      ctx.fill();
    }

    requestAnimationFrame(animate);
  }

  animate();
}

/* ----------------------------------------------------
   10. Interactive Card Spotlight & Specular Light Follow
   ---------------------------------------------------- */
function initCardSpotlight() {
  const spotlightTargets = document.querySelectorAll(
    '.package-card, .hero-image-card, .calculator-box, .calc-result-card, .stage-card, .faq-item, .contact-info-card, .contact-form, .proof-card'
  );

  spotlightTargets.forEach((card) => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

/* ----------------------------------------------------
   11. Interactive Before & After Drag Comparison Slider
   ---------------------------------------------------- */
function initBeforeAfterSlider() {
  const container = document.getElementById('beforeAfterSlider');
  const beforeWrapper = document.getElementById('baBeforeWrapper');
  const handle = document.getElementById('baHandle');

  if (!container || !beforeWrapper || !handle) return;

  let isDragging = false;

  function updateSlider(clientX) {
    const rect = container.getBoundingClientRect();
    let x = clientX - rect.left;
    // Clamp within 5% to 95%
    const min = rect.width * 0.05;
    const max = rect.width * 0.95;
    if (x < min) x = min;
    if (x > max) x = max;

    const percent = (x / rect.width) * 100;
    beforeWrapper.style.width = `${percent}%`;
    handle.style.left = `${percent}%`;
  }

  // Pointer & Mouse Drag Events
  handle.addEventListener('mousedown', (e) => {
    isDragging = true;
    handle.classList.add('active');
    e.preventDefault();
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      handle.classList.remove('active');
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updateSlider(e.clientX);
  });

  // Touch Support for Mobile
  handle.addEventListener('touchstart', (e) => {
    isDragging = true;
    handle.classList.add('active');
  }, { passive: true });

  window.addEventListener('touchend', () => {
    isDragging = false;
    handle.classList.remove('active');
  });

  window.addEventListener('touchmove', (e) => {
    if (!isDragging || !e.touches[0]) return;
    updateSlider(e.touches[0].clientX);
  }, { passive: true });

  // Click or drag anywhere on container to move slider
  container.addEventListener('click', (e) => {
    updateSlider(e.clientX);
  });
}

/* ----------------------------------------------------
   12. Animated Numerical Counters & Real-Time Booking Sync
   ---------------------------------------------------- */
function animateCounterNumber(el, start, end, duration = 1200, prefix = '', suffix = '', decimals = 0) {
  if (!el) return;
  const startTime = performance.now();
  const diff = end - start;

  function step(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    const currentVal = start + diff * ease;

    const formatted = decimals > 0 
      ? currentVal.toFixed(decimals) 
      : Math.round(currentVal).toLocaleString();

    el.textContent = `${prefix}${formatted}${suffix}`;

    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      const finalFormatted = decimals > 0 ? end.toFixed(decimals) : end.toLocaleString();
      el.textContent = `${prefix}${finalFormatted}${suffix}`;
    }
  }

  requestAnimationFrame(step);
}

function showLiveToast(message) {
  let container = document.querySelector('.live-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'live-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'live-toast';
  toast.innerHTML = `
    <div class="live-toast-icon">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
    </div>
    <div>
      <div style="font-weight: 700; color: #34d399; font-size: 0.74rem; letter-spacing: 0.5px; text-transform: uppercase;">Real-Time Booking Update</div>
      <div style="font-size: 0.82rem; color: #ffffff;">${message}</div>
    </div>
  `;

  container.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add('show'));

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 5000);
}

function initCounters() {
  const counters = document.querySelectorAll('.counter-value');
  if (!counters.length) return;

  const observed = new Set();
  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !observed.has(entry.target)) {
          observed.add(entry.target);
          const el = entry.target;
          const target = parseFloat(el.getAttribute('data-target') || '0');
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
          animateCounterNumber(el, 0, target, 1600, prefix, suffix, decimals);
        }
      });
    },
    { threshold: 0.2 }
  );

  counters.forEach((c) => observer.observe(c));

  // Initialize live background sync with server
  initRealtimeBookingSync();
}

function initRealtimeBookingSync() {
  let lastTotalBookings = null;
  let lastDeliveredTanks = null;
  let broadcastChannel = null;

  try {
    broadcastChannel = new BroadcastChannel('drtc_booking_sync');
    broadcastChannel.onmessage = (event) => {
      if (event.data && event.data.type === 'BOOKING_CREATED') {
        fetchLiveStats(true);
      }
    };
  } catch (e) {
    // Graceful fallback for older browsers
  }

  async function fetchLiveStats(isManualTrigger = false) {
    try {
      const res = await fetch('/api/live-stats/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      });
      if (!res.ok) return;
      const data = await res.json();
      if (data.status !== 'success') return;

      const currentTotal = data.total_bookings;
      const currentDelivered = data.clean_tanks_delivered;

      const totalBookingsEl = document.getElementById('stat-live-bookings');
      const deliveredEl = document.getElementById('stat-clean-tanks');
      const heroCountEl = document.getElementById('heroLiveBookings');

      if (lastTotalBookings !== null && currentTotal > lastTotalBookings) {
        // Real-time booking increment detected!
        if (totalBookingsEl) {
          totalBookingsEl.classList.add('stat-updated');
          animateCounterNumber(totalBookingsEl, lastTotalBookings, currentTotal, 900, '', '');
          setTimeout(() => totalBookingsEl.classList.remove('stat-updated'), 1200);
        }
        if (deliveredEl) {
          deliveredEl.classList.add('stat-updated');
          animateCounterNumber(deliveredEl, lastDeliveredTanks, currentDelivered, 900, '', '+');
          setTimeout(() => deliveredEl.classList.remove('stat-updated'), 1200);
        }
        if (heroCountEl) {
          heroCountEl.textContent = currentTotal;
          heroCountEl.classList.add('stat-updated');
          setTimeout(() => heroCountEl.classList.remove('stat-updated'), 1200);
        }

        const latest = data.latest_booking;
        if (latest) {
          showLiveToast(`New Booking #${latest.booking_id} for ${latest.capacity} in ${latest.locality}!`);
        } else {
          showLiveToast(`A new tank cleaning appointment was scheduled live!`);
        }
      } else if (lastTotalBookings === null) {
        // Initial populate if not yet animated
        if (totalBookingsEl && !totalBookingsEl.textContent.trim()) {
          totalBookingsEl.textContent = currentTotal;
        }
        if (deliveredEl && !deliveredEl.textContent.trim()) {
          deliveredEl.textContent = `${currentDelivered}+`;
        }
        if (heroCountEl) {
          heroCountEl.textContent = currentTotal;
        }
      }

      lastTotalBookings = currentTotal;
      lastDeliveredTanks = currentDelivered;
    } catch (err) {
      // Quiet background polling catch
    }
  }

  // Poll live every 4 seconds
  setInterval(() => fetchLiveStats(false), 4000);
  fetchLiveStats(false);

  // Broadcast when user books locally
  window.addEventListener('drtc:booking_created', () => {
    fetchLiveStats(true);
    if (broadcastChannel) {
      broadcastChannel.postMessage({ type: 'BOOKING_CREATED', timestamp: Date.now() });
    }
  });
}

/* ----------------------------------------------------
   13. Button Click Water Ripple Effect
   ---------------------------------------------------- */
function initButtonRipples() {
  document.querySelectorAll('.btn').forEach((btn) => {
    btn.addEventListener('click', function (e) {
      const rect = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const diameter = Math.max(rect.width, rect.height);
      const radius = diameter / 2;

      circle.style.width = circle.style.height = `${diameter}px`;
      circle.style.left = `${e.clientX - rect.left - radius}px`;
      circle.style.top = `${e.clientY - rect.top - radius}px`;
      circle.classList.add('click-ripple');

      const existing = this.querySelector('.click-ripple');
      if (existing) existing.remove();

      this.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  });
}

/* ----------------------------------------------------
   14. Scroll Reveal Staggered Animations
   ---------------------------------------------------- */
function initScrollReveal() {
  const elements = document.querySelectorAll(
    '.package-card, .stage-card, .proof-card, .review-card, .calc-grid, .before-after-container'
  );

  elements.forEach((el) => el.classList.add('reveal-fade-up'));

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  elements.forEach((el) => observer.observe(el));
}

