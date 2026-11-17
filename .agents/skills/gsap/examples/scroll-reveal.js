/**
 * Staggered Scroll Reveal Pattern with ScrollTrigger
 * Ideal for feature grids, service cards, and review lists.
 */
function initScrollReveal() {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
    console.warn("GSAP or ScrollTrigger not loaded");
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // Group reveal for grids
  const sections = document.querySelectorAll("[data-scroll-section]");

  sections.forEach((section) => {
    const cards = section.querySelectorAll("[data-scroll-item]");
    if (!cards.length) return;

    gsap.from(cards, {
      scrollTrigger: {
        trigger: section,
        start: "top 85%",
        toggleActions: "play none none reverse",
      },
      opacity: 0,
      y: 35,
      duration: 0.65,
      stagger: 0.12,
      ease: "power2.out",
      clearProps: "transform,opacity"
    });
  });
}

document.addEventListener("DOMContentLoaded", initScrollReveal);

