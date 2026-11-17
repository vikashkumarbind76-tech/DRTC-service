/**
 * Interactive 3D Tilt & Magnetic Micro-interactions
 * Uses gsap.quickTo() for 60fps buttery-smooth tracking with zero garbage collection lag.
 */
function initInteractiveCards() {
  if (typeof gsap === "undefined") return;

  const cards = document.querySelectorAll(".tilt-card, [data-interactive-card]");

  cards.forEach((card) => {
    // QuickTo setters for high-frequency transforms
    const xTo = gsap.quickTo(card, "rotationY", { duration: 0.35, ease: "power2.out" });
    const yTo = gsap.quickTo(card, "rotationX", { duration: 0.35, ease: "power2.out" });
    const scaleTo = gsap.quickTo(card, "scale", { duration: 0.3, ease: "power2.out" });

    // Set 3D perspective on parent if not already set in CSS
    if (!card.parentElement.style.perspective) {
      card.parentElement.style.perspective = "1000px";
    }

    card.addEventListener("mouseenter", () => {
      scaleTo(1.025);
    });

    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const xPercent = (e.clientX - rect.left) / rect.width - 0.5;
      const yPercent = (e.clientY - rect.top) / rect.height - 0.5;

      // Rotate card: max 12 degrees
      xTo(xPercent * 14);
      yTo(-yPercent * 14);
    });

    card.addEventListener("mouseleave", () => {
      xTo(0);
      yTo(0);
      scaleTo(1);
    });
  });
}

document.addEventListener("DOMContentLoaded", initInteractiveCards);

