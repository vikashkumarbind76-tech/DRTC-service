/**
 * High-Impact Landing Page Hero Entrance Timeline
 * Choreographs trust badges, headline, call-to-action buttons, and hero visual.
 */
function initHeroEntrance() {
  if (typeof gsap === "undefined") return;

  const hero = document.querySelector("#hero-section, .hero");
  if (!hero) return;

  // Check prefers-reduced-motion
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    gsap.set(hero.querySelectorAll(".hero-badge, .hero-title, .hero-desc, .hero-actions, .hero-visual"), {
      opacity: 1,
      y: 0,
      scale: 1
    });
    return;
  }

  const tl = gsap.timeline({
    defaults: { ease: "power3.out" },
    delay: 0.1
  });

  tl.from(hero.querySelector(".hero-badge"), {
    opacity: 0,
    y: -18,
    duration: 0.5
  })
  .from(hero.querySelector(".hero-title"), {
    opacity: 0,
    y: 30,
    duration: 0.8
  }, "-=0.25")
  .from(hero.querySelector(".hero-desc"), {
    opacity: 0,
    y: 20,
    duration: 0.6
  }, "-=0.4")
  .from(hero.querySelectorAll(".hero-actions .btn, .hero-actions a"), {
    opacity: 0,
    y: 15,
    scale: 0.95,
    stagger: 0.1,
    duration: 0.45
  }, "-=0.3")
  .from(hero.querySelector(".hero-visual"), {
    opacity: 0,
    scale: 0.9,
    y: 25,
    duration: 0.9,
    ease: "back.out(1.3)"
  }, "-=0.5");
}

document.addEventListener("DOMContentLoaded", initHeroEntrance);

