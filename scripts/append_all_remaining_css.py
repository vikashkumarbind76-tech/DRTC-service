css_all = '''
/* ==========================================================================
   OFFICIAL DRTC REMAINING PANELS STYLES (MATCHING FULL DESIGN BOARD)
   ========================================================================== */

/* ----------------------------------------------------
   PANEL 2: 6 SERVICES CARDS GRID (3x2)
   ---------------------------------------------------- */
.service-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 992px) {
  .service-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .service-cards-grid {
    grid-template-columns: 1fr;
    max-width: 380px;
    margin: 0 auto;
  }
}

.service-card-clean {
  background: linear-gradient(180deg, rgba(8, 24, 38, 0.75) 0%, rgba(4, 12, 22, 0.92) 100%);
  border: 1px solid rgba(0, 240, 255, 0.22);
  border-radius: 18px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(14px);
  transition: all var(--transition-smooth);
}

.service-card-clean:hover {
  border-color: rgba(0, 240, 255, 0.55);
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.85), 0 0 30px rgba(0, 210, 255, 0.25);
  transform: translateY(-6px);
}

.service-card-img-wrap {
  width: 100%;
  height: 160px;
  overflow: hidden;
  position: relative;
}

.service-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-smooth);
}

.service-card-clean:hover .service-card-img {
  transform: scale(1.06);
}

.service-card-content {
  padding: 1.35rem 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
  text-align: center;
  align-items: center;
}

.service-card-title {
  font-family: var(--font-body);
  font-size: 1.15rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.5rem;
  line-height: 1.25;
}

.service-card-desc {
  font-size: 0.84rem;
  color: #94a3b8;
  line-height: 1.5;
  margin-bottom: 1.25rem;
  flex: 1;
}

.service-card-btn {
  width: 100%;
  padding: 0.65rem 1rem;
  font-size: 0.78rem;
}

/* ----------------------------------------------------
   PANEL 3: PRICING 3 TOP + 2 BOTTOM + BANNER
   ---------------------------------------------------- */
.pricing-split-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  z-index: 1;
}

.pricing-top-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.35rem;
}

.pricing-bottom-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.35rem;
  max-width: 66.66%;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 900px) {
  .pricing-top-3, .pricing-bottom-2 {
    grid-template-columns: 1fr;
    max-width: 380px;
    margin: 0 auto;
  }
}

.pricing-fair-banner {
  margin-top: 1.75rem;
  background: linear-gradient(135deg, rgba(8, 28, 44, 0.75) 0%, rgba(4, 16, 26, 0.9) 100%);
  border: 1px solid rgba(0, 240, 255, 0.25);
  border-radius: 16px;
  padding: 1.25rem 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
}

.fair-banner-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid rgba(0, 240, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neon-cyan);
  flex-shrink: 0;
}

.fair-banner-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: #ffffff;
}

.fair-banner-sub {
  font-size: 0.84rem;
  color: #94a3b8;
  margin-top: 2px;
}

/* ----------------------------------------------------
   PANEL 4: BOOKING BOTTOM 4 PILLS
   ---------------------------------------------------- */
.booking-bottom-badges {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
  margin-top: 2.5rem;
  position: relative;
  z-index: 1;
}

.booking-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 1.25rem;
  background: rgba(8, 24, 38, 0.7);
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 9999px;
  font-size: 0.84rem;
  font-weight: 600;
  color: #f1f5f9;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

/* ----------------------------------------------------
   PANEL 5: ABOUT DRTC SERVICE
   ---------------------------------------------------- */
.about-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: #03080e;
  overflow: hidden;
}

.about-split-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  align-items: center;
  gap: 3.5rem;
  position: relative;
  z-index: 1;
}

@media (max-width: 900px) {
  .about-split-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

.about-tank-card {
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(0, 240, 255, 0.22);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 35px rgba(0, 210, 255, 0.15);
  background: #050d16;
  aspect-ratio: 4 / 3.3;
}

.about-tank-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.about-content-col {
  display: flex;
  flex-direction: column;
}

.about-story-box {
  margin-bottom: 2rem;
}

.about-section-heading {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.65rem;
}

.about-story-text {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.65;
}

.about-values-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 480px) {
  .about-values-grid {
    grid-template-columns: 1fr;
  }
}

.about-value-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem 1.15rem;
  background: rgba(8, 24, 38, 0.65);
  border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 14px;
  transition: all var(--transition-fast);
}

.about-value-badge:hover {
  background: rgba(12, 32, 50, 0.85);
  border-color: rgba(0, 240, 255, 0.45);
  transform: translateY(-2px);
}

.about-value-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid rgba(0, 240, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neon-cyan);
  flex-shrink: 0;
}

.about-value-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #ffffff;
}

/* ----------------------------------------------------
   PANEL 6: CONTACT US
   ---------------------------------------------------- */
.contact-clean-section {
  position: relative;
  padding: 6.5rem 0;
  background: #04090e;
  overflow: hidden;
}

.contact-split-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  max-width: 1040px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

@media (max-width: 868px) {
  .contact-split-grid {
    grid-template-columns: 1fr;
  }
}

.contact-details-card {
  background: linear-gradient(180deg, rgba(8, 22, 34, 0.82) 0%, rgba(4, 12, 22, 0.95) 100%);
  border: 1px solid rgba(0, 240, 255, 0.22);
  border-radius: 20px;
  padding: 2.25rem;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(16px);
  display: flex;
  flex-direction: column;
  gap: 1.35rem;
}

.contact-row-entry {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.contact-entry-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(0, 240, 255, 0.08);
  border: 1px solid rgba(0, 240, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neon-cyan);
  flex-shrink: 0;
  margin-top: 2px;
}

.contact-entry-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--neon-cyan);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 2px;
}

.contact-entry-val {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.4;
}

.contact-entry-val a {
  color: #ffffff;
  text-decoration: none;
  transition: color 0.2s ease;
}

.contact-entry-val a:hover {
  color: var(--neon-cyan);
}

.contact-enquiry-card {
  background: linear-gradient(180deg, rgba(8, 22, 34, 0.82) 0%, rgba(4, 12, 22, 0.95) 100%);
  border: 1px solid rgba(0, 240, 255, 0.22);
  border-radius: 20px;
  padding: 2.25rem;
  box-shadow: 0 16px 45px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(16px);
}

.enquiry-card-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 1.35rem;
}

/* ----------------------------------------------------
   PANEL 7: BOOKING SUCCESS CARD (MATCHING MOCKUP)
   ---------------------------------------------------- */
.success-card-mockup {
  background: linear-gradient(180deg, rgba(8, 24, 38, 0.85) 0%, rgba(4, 12, 22, 0.95) 100%);
  border: 1px solid rgba(0, 240, 255, 0.25);
  border-radius: 24px;
  padding: 2.75rem 2.25rem;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 35px rgba(0, 210, 255, 0.15);
  backdrop-filter: blur(16px);
  position: relative;
  overflow: hidden;
}

.success-circle-check {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(16, 185, 129, 0.12);
  border: 3px solid #10b981;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
  box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
}

.success-title-mockup {
  font-family: var(--font-body);
  font-size: clamp(1.6rem, 3.5vw, 2.2rem);
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.01em;
  margin-bottom: 0.65rem;
}

.success-desc-mockup {
  font-size: 0.95rem;
  color: #94a3b8;
  max-width: 520px;
  margin: 0 auto 1.75rem auto;
  line-height: 1.6;
}

.reference-badge-box {
  display: inline-flex;
  align-items: center;
  gap: 1.25rem;
  background: rgba(5, 16, 26, 0.8);
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 12px;
  padding: 0.75rem 1.75rem;
  margin-bottom: 2rem;
}

.ref-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #94a3b8;
}

.ref-val {
  font-family: monospace;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--neon-cyan-bright);
}

.success-actions-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.75rem;
  flex-wrap: wrap;
}

.success-specs-box {
  background: rgba(5, 12, 20, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 1.15rem 1.35rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  font-size: 0.88rem;
}

.success-spec-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #cbd5e1;
}
'''

with open('static/css/styles.css', 'a', encoding='utf-8') as f:
    f.write('\n' + css_all + '\n')

print('Appended all remaining CSS styles to static/css/styles.css successfully!')

