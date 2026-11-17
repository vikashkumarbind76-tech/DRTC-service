/**
 * Text Reveal / Headline Stagger Animation
 * Works with SplitText plugin if available, or falls back to span splitting.
 */
function initTextReveal() {
  if (typeof gsap === "undefined") return;

  const textElements = document.querySelectorAll("[data-split-reveal]");

  textElements.forEach((el) => {
    // If SplitText plugin is registered:
    if (typeof SplitText !== "undefined") {
      gsap.registerPlugin(SplitText);
      const split = new SplitText(el, { type: "words,chars" });

      gsap.from(split.chars, {
        scrollTrigger: {
          trigger: el,
          start: "top 80%",
          once: true
        },
        opacity: 0,
        y: 20,
        rotateX: -45,
        duration: 0.6,
        stagger: 0.02,
        ease: "back.out(1.4)",
        onComplete: () => split.revert() // Accessibility: restore natural DOM
      });
    } else {
      // Accessible fallback using words/spans
      const text = el.innerText.trim();
      const words = text.split(" ");
      el.innerHTML = words.map(w => `<span class="gsap-word" style="display:inline-block; opacity:0; transform:translateY(15px);">${w}&nbsp;</span>`).join("");

      gsap.to(el.querySelectorAll(".gsap-word"), {
        scrollTrigger: {
          trigger: el,
          start: "top 80%",
          once: true
        },
        opacity: 1,
        y: 0,
        duration: 0.5,
        stagger: 0.04,
        ease: "power2.out"
      });
    }
  });
}

document.addEventListener("DOMContentLoaded", initTextReveal);

