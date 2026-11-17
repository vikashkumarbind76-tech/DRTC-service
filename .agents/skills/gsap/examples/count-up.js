/**
 * Animated Numeric Counters with ScrollTrigger
 * Smoothly animates numbers from 0 to target value on scroll into viewport.
 */
function initAnimatedCounters() {
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;

  gsap.registerPlugin(ScrollTrigger);

  const counters = document.querySelectorAll(".stat-counter, [data-counter-target]");

  counters.forEach((el) => {
    const target = parseFloat(el.getAttribute("data-counter-target") || el.textContent.replace(/[^0-9.]/g, "")) || 0;
    const prefix = el.getAttribute("data-counter-prefix") || "";
    const suffix = el.getAttribute("data-counter-suffix") || "";
    const decimals = parseInt(el.getAttribute("data-counter-decimals") || "0", 10);

    const state = { count: 0 };

    gsap.to(state, {
      count: target,
      duration: 1.8,
      ease: "power2.out",
      scrollTrigger: {
        trigger: el,
        start: "top 85%",
        once: true
      },
      onUpdate: () => {
        const formatted = decimals > 0 
          ? state.count.toFixed(decimals) 
          : Math.floor(state.count).toLocaleString();
        el.textContent = `${prefix}${formatted}${suffix}`;
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", initAnimatedCounters);

