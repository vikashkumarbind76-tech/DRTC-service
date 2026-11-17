css_additions = '''
/* ==========================================================================
   OFFICIAL DRTC SERVICE DESIGN SYSTEM (EXACT FIGMA MOCKUP REPLICA)
   Pure Aquatic Dark Neon Cyan Theme
   ========================================================================== */

:root {
  --neon-cyan: #00d2d3;
  --neon-cyan-bright: #00f0ff;
  --neon-cyan-glow: rgba(0, 240, 255, 0.35);
  --neon-cyan-subtle: rgba(0, 210, 211, 0.12);
  --dark-teal-bg: #04090e;
  --dark-teal-card: rgba(8, 22, 34, 0.78);
  --dark-teal-card-hover: rgba(12, 30, 46, 0.9);
  --dark-teal-border: rgba(0, 240, 255, 0.22);
}

/* Navbar Brand typography matching mockup */
.brand-drtc-exact {
  font-family: var(--font-body);
  font-size: 1.4rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.5px;
  line-height: 1;
  text-transform: uppercase;
}

.brand-subtext-cyan {
  font-family: var(--font-body);
  font-size: 0.62rem;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-top: 3px;
  line-height: 1;
}

/* Watermark typography */
.section-watermark {
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-body);
  font-size: clamp(3.2rem, 7.5vw, 6.5rem);
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: transparent;
  -webkit-text-stroke: 1.5px rgba(0, 240, 255, 0.08);
  white-space: nowrap;
  pointer-events: none;
  user-select: none;
  z-index: 0;
}

/* Cyan neon text */
.text-cyan-neon {
  color: var(--neon-cyan-bright) !important;
  text-shadow: 0 0 16px rgba(0, 240, 255, 0.45);
}

/* Section Centered Headers */
.section-header-center {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 720px;
  margin: 0 auto 3rem auto;
}

.section-tag-cyan {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 0.65rem;
}

.section-title-clean {
  font-family: var(--font-body);
  font-size: clamp(1.85rem, 4vw, 2.75rem);
  font-weight: 800;
  color: #ffffff;
  line-height: 1.2;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.section-desc-clean {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.6;
  max-width: 620px;
  margin: 0 auto;
}

/* Buttons Pill */
.btn-cyan-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  padding: 0.8rem 1.85rem;
  background: linear-gradient(135deg, #00d2d3 0%, #00f0ff 100%);
  color: #030a10 !important;
  font-family: var(--font-body);
  font-size: 0.86rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: none;
  border-radius: 9999px;
  box-shadow: 0 4px 20px rgba(0, 210, 255, 0.35);
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.btn-cyan-pill:hover {
  background: linear-gradient(135deg, #00f0ff 0%, #38bdf8 100%);
  box-shadow: 0 6px 28px rgba(0, 240, 255, 0.6);
  transform: translateY(-2px);
  color: #000000 !important;
}

.btn-outline-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  padding: 0.8rem 1.85rem;
  background: rgba(0, 240, 255, 0.04);
  color: #ffffff !important;
  font-family: var(--font-body);
  font-size: 0.86rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 9999px;
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.btn-outline-pill:hover {
  background: rgba(0, 240, 255, 0.12);
  border-color: var(--neon-cyan);
  color: var(--neon-cyan-bright) !important;
  box-shadow: 0 4px 20px rgba(0, 210, 255, 0.2);
  transform: translateY(-2px);
}

/* ==========================================================================
   HERO SECTION (MOCKUP REPLICA)
   ========================================================================== */
.hero-clean-section {
  position: relative;
  min-height: 100vh;
  padding: 8.5rem 0 3.5rem 0;
  background: radial-gradient(circle at 80% 20%, rgba(0, 210, 255, 0.08) 0%, transparent 50%),
              radial-gradient(circle at 20% 70%, rgba(0, 168, 204, 0.06) 0%, transparent 40%),
              #04090e;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-clean-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.95fr;
  align-items: center;
  gap: 3.5rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 992px) {
  .hero-clean-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

.hero-tagline {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.hero-headline-clean {
  font-family: var(--font-body);
  font-size: clamp(2.3rem, 4.5vw, 3.6rem);
  font-weight: 900;
  color: #ffffff;
  line-height: 1.15;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  margin-bottom: 1.35rem;
}

.hero-desc-clean {
  font-size: 1.05rem;
  color: #94a3b8;
  line-height: 1.65;
  max-width: 540px;
  margin-bottom: 2.25rem;
}

.hero-actions-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
  margin-bottom: 2.75rem;
}

.hero-feature-pills {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.hero-feature-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.55rem 1.1rem;
  background: rgba(8, 24, 38, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #f1f5f9;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  transition: all var(--transition-fast);
}

.hero-feature-pill:hover {
  border-color: rgba(0, 240, 255, 0.5);
  background: rgba(12, 32, 50, 0.9);
  box-shadow: 0 4px 20px rgba(0, 210, 255, 0.2);
  transform: translateY(-2px);
}

.hero-visual-card {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 50px rgba(0, 210, 255, 0.18);
  border: 1px solid rgba(0, 240, 255, 0.25);
  background: #050d16;
  aspect-ratio: 4 / 3.4;
  transition: transform var(--transition-smooth);
}

.hero-visual-card:hover {
  transform: scale(1.015);
  border-color: rgba(0, 240, 255, 0.45);
}

.hero-visual-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Mouse Scroll Down Indicator */
.scroll-down-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  margin-top: 3.5rem;
  text-decoration: none;
  position: relative;
  z-index: 1;
}

.mouse-pill {
  width: 22px;
  height: 36px;
  border: 2px solid rgba(0, 240, 255, 0.55);
  border-radius: 12px;
  display: flex;
  justify-content: center;
  padding-top: 6px;
}

.mouse-dot {
  width: 3.5px;
  height: 7px;
  background: var(--neon-cyan-bright);
  border-radius: 2px;
  animation: mouseAnim 1.7s infinite;
}

@keyframes mouseAnim {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(14px); opacity: 0; }
}

.scroll-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

/* ==========================================================================
   SERVICES & PRICING SECTION (MOCKUP REPLICA)
   ========================================================================== */
.services-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: #04090e;
  overflow: hidden;
}

.capacity-cards-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 1100px) {
  .capacity-cards-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 680px) {
  .capacity-cards-row {
    grid-template-columns: 1fr;
    max-width: 380px;
    margin-left: auto;
    margin-right: auto;
  }
}

.capacity-card {
  position: relative;
  background: linear-gradient(180deg, rgba(8, 24, 38, 0.75) 0%, rgba(4, 12, 22, 0.92) 100%);
  border: 1px solid rgba(0, 240, 255, 0.22);
  border-radius: 18px;
  padding: 1.75rem 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(14px);
  transition: all var(--transition-smooth);
  overflow: hidden;
}

.capacity-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 20%;
  right: 20%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #00f0ff, transparent);
  opacity: 0.8;
}

.capacity-card:hover {
  border-color: rgba(0, 240, 255, 0.55);
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 30px rgba(0, 210, 255, 0.25);
  transform: translateY(-6px);
}

.capacity-card-img-wrap {
  width: 100%;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.85rem;
}

.capacity-card-img {
  max-width: 95px;
  max-height: 85px;
  object-fit: contain;
  filter: drop-shadow(0 4px 14px rgba(0, 210, 255, 0.35));
}

.capacity-card-size {
  font-family: var(--font-body);
  font-size: 1.6rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.1;
  margin-bottom: 0.2rem;
}

.capacity-card-label {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--neon-cyan);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.capacity-card-price {
  font-family: var(--font-body);
  font-size: 1.85rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1.25rem;
}

.capacity-card .card-btn {
  width: 100%;
  padding: 0.65rem 0.95rem;
  font-size: 0.78rem;
}

/* ==========================================================================
   WHY CHOOSE US SECTION (MOCKUP REPLICA)
   ========================================================================== */
.why-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: radial-gradient(circle at 50% 50%, rgba(0, 210, 255, 0.05) 0%, transparent 60%), #03080e;
  overflow: hidden;
}

.why-clean-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1.15rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 1200px) {
  .why-clean-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .why-clean-grid {
    grid-template-columns: 1fr;
    max-width: 380px;
    margin-left: auto;
    margin-right: auto;
  }
}

.why-card {
  background: linear-gradient(180deg, rgba(8, 22, 34, 0.65) 0%, rgba(4, 12, 20, 0.88) 100%);
  border: 1px solid rgba(0, 240, 255, 0.18);
  border-radius: 16px;
  padding: 1.75rem 1.15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  transition: all var(--transition-smooth);
}

.why-card:hover {
  border-color: rgba(0, 240, 255, 0.45);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.75), 0 0 25px rgba(0, 210, 255, 0.22);
  transform: translateY(-4px);
}

.why-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(0, 240, 255, 0.08);
  border: 1px solid rgba(0, 240, 255, 0.28);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.1rem;
  color: var(--neon-cyan);
}

.why-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
  line-height: 1.35;
}

.why-desc {
  font-size: 0.8rem;
  color: #94a3b8;
  line-height: 1.5;
}

/* ==========================================================================
   BOOKING SECTION (TOP RIGHT FRAME OF COLLAGE)
   ========================================================================== */
.booking-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: #04090e;
  overflow: hidden;
}

.booking-split-grid {
  display: grid;
  grid-template-columns: 1.65fr 1fr;
  gap: 1.85rem;
  max-width: 1040px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

@media (max-width: 868px) {
  .booking-split-grid {
    grid-template-columns: 1fr;
  }
}

.booking-form-card {
  background: linear-gradient(180deg, rgba(8, 22, 34, 0.82) 0%, rgba(4, 12, 22, 0.95) 100%);
  border: 1px solid rgba(0, 240, 255, 0.24);
  border-radius: 20px;
  padding: 2.25rem;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(16px);
}

.pricing-summary-card {
  background: linear-gradient(180deg, rgba(8, 22, 34, 0.82) 0%, rgba(4, 12, 22, 0.95) 100%);
  border: 1px solid rgba(0, 240, 255, 0.24);
  border-radius: 20px;
  padding: 2.25rem;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(16px);
  display: flex;
  flex-direction: column;
}

.pricing-summary-header {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.9rem;
  font-weight: 800;
  color: var(--neon-cyan);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 1.5rem;
}

.pricing-summary-list {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  flex: 1;
}

.pricing-row-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(0, 240, 255, 0.12);
  transition: all var(--transition-fast);
}

.pricing-row-item:hover {
  background: rgba(0, 240, 255, 0.08);
  border-color: rgba(0, 240, 255, 0.35);
  transform: translateX(4px);
}

.pricing-item-cap {
  font-size: 1.05rem;
  font-weight: 700;
  color: #f1f5f9;
}

.pricing-item-rate {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--neon-cyan-bright);
}

.form-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 600px) {
  .form-row-2col {
    grid-template-columns: 1fr;
  }
}

.form-group-custom {
  margin-bottom: 1.25rem;
}

.form-label-clean {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 0.5rem;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon svg {
  position: absolute;
  left: 1rem;
  color: #64748b;
  pointer-events: none;
}

.clean-input, .clean-select, .clean-textarea {
  width: 100%;
  background: rgba(5, 12, 20, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 0.75rem 1rem 0.75rem 2.85rem;
  color: #ffffff;
  font-family: var(--font-body);
  font-size: 0.9rem;
  outline: none;
  transition: all var(--transition-fast);
}

.clean-textarea {
  padding-left: 1rem;
  resize: vertical;
}

.clean-select {
  padding-left: 1rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2300d2d3' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
}

.clean-input:focus, .clean-select:focus, .clean-textarea:focus {
  border-color: var(--neon-cyan);
  background: rgba(8, 20, 32, 0.95);
  box-shadow: 0 0 16px rgba(0, 240, 255, 0.25);
}

/* ==========================================================================
   GALLERY SECTION (MIDDLE RIGHT FRAME OF COLLAGE)
   ========================================================================== */
.gallery-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: #03080e;
  overflow: hidden;
}

.gallery-photo-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.35rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 900px) {
  .gallery-photo-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .gallery-photo-grid {
    grid-template-columns: 1fr;
  }
}

.gallery-photo-card {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  border: 1px solid rgba(0, 240, 255, 0.22);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.65);
  background: #050d16;
  aspect-ratio: 4 / 3.2;
  transition: all var(--transition-smooth);
}

.gallery-photo-card:hover {
  border-color: rgba(0, 240, 255, 0.55);
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 30px rgba(0, 210, 255, 0.25);
  transform: translateY(-4px) scale(1.02);
}

.gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform var(--transition-smooth);
}

.gallery-photo-card:hover .gallery-img {
  transform: scale(1.05);
}
'''

with open('static/css/styles.css', 'a', encoding='utf-8') as f:
    f.write('\n' + css_additions + '\n')

print('Appended official exact mockup CSS to static/css/styles.css successfully!')
