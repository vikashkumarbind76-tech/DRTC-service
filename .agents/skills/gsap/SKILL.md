---
name: gsap
description: GreenSock Animation Platform (GSAP 3) expert guidance for high-performance web animations, timelines, micro-interactions, scroll-driven effects, and SVG morphing. Use when creating, debugging, or optimizing animations with GSAP, ScrollTrigger, Flip, Draggable, SplitText, Observer, MotionPath, TextPlugin, or integrating GSAP in HTML, Django templates, React, Vue, or modern web stacks.
argument-hint: "[animation type, effect, or plugin]"
license: Standard GreenSock License
metadata:
  author: greensock
  version: "3.13+"
---

# GSAP Animation Skill (v3.13+)

Comprehensive engineering guide for crafting 60fps, GPU-accelerated web animations using the GreenSock Animation Platform (GSAP 3).

## When to Use This Skill

Activate this skill when:
- Designing or implementing hero section entrances and staggered layout transitions.
- Building scroll-driven animations, parallax effects, or sticky pin/scrub experiences with **ScrollTrigger**.
- Adding tactile micro-interactions (magnetic buttons, 3D tilt hover, click ripple, floating badges).
- Animating numeric counters, statistics, and KPI dashboards smoothly.
- Creating text reveals (character split, typewriter effect, word fades) using **SplitText** or **TextPlugin**.
- Handling complex choreography and sequencing with **GSAP Timelines**.
- Managing layout morphing with **Flip** or SVG path morphing with **MorphSVGPlugin**.
- Optimizing web animation performance, avoiding layout thrashing, and respecting `prefers-reduced-motion`.
- Integrating GSAP in Django templates (`static/js/gsap/`), React (`@gsap/react`), Vue, or Vanilla JS.

---

## Quick Reference & Progressive Disclosure

For deep dives, inspect the modular reference files:
- [API Cheatsheet](file:///c:/Users/Vikash/OneDrive/Desktop/Projects/DRTC_Service_Django_Production/.agents/skills/gsap/references/api-cheat-sheet.md): Tween syntax, timeline positioning, and easing curves.
- [ScrollTrigger Guide](file:///c:/Users/Vikash/OneDrive/Desktop/Projects/DRTC_Service_Django_Production/.agents/skills/gsap/references/scrolltrigger-guide.md): Triggers, scrub, pin, snapping, and responsive breakpoints.
- [Plugins Overview](file:///c:/Users/Vikash/OneDrive/Desktop/Projects/DRTC_Service_Django_Production/.agents/skills/gsap/references/plugins-overview.md): Flip, Draggable, Observer, SplitText, and TextPlugin.
- [Performance & Accessibility](file:///c:/Users/Vikash/OneDrive/Desktop/Projects/DRTC_Service_Django_Production/.agents/skills/gsap/references/performance-and-a11y.md): GPU layers, compositor thread, cleanup protocols, and reduced motion.

---

## Local Assets & Setup in DRTC Project

The production-ready minified files are packaged inside this skill at:
- `resources/dist/` (full bundle: core + all plugins)
- `static/js/gsap/` (ready for Django templates)

### Loading in Django Templates (`templates/base.html`):

```html
<!-- GSAP Core & Essential Plugins -->
<script src="{% static 'js/gsap/gsap.min.js' %}"></script>
<script src="{% static 'js/gsap/ScrollTrigger.min.js' %}"></script>
<script src="{% static 'js/gsap/TextPlugin.min.js' %}"></script>

<script>
  // Register plugins immediately after script load
  gsap.registerPlugin(ScrollTrigger, TextPlugin);
</script>
```

---

## Core Principles & Golden Rules

1. **Animate Transform and Opacity Only**:
   - Prefer `x`, `y`, `xPercent`, `yPercent`, `scale`, `rotation`, and `opacity`.
   - Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`) unless unavoidable (use the `Flip` plugin for layout shifts).
2. **Always Respect `prefers-reduced-motion`**:
   - Use `gsap.matchMedia()` to skip animations or render instantaneous final states for users with vestibular sensitivities.
3. **Use Timelines for Choreography**:
   - Avoid chaining individual `delay` values on isolated `gsap.to()` calls. Use `const tl = gsap.timeline()` with relative position parameters (`"<"`, `"-=0.2"`, `"+=0.1"`).
4. **Use `quickTo()` for High-Frequency Events**:
   - For mouse tracking, cursor followers, and 3D tilt, avoid instantiating new tweens every `pointermove`. Use `gsap.quickTo(el, "x", { duration: 0.3, ease: "power2" })`.
5. **Always Clean Up Resources**:
   - Always kill tweens or timelines on component unmount, page transitions, or dynamic AJAX swaps with `ctx.revert()` or `ScrollTrigger.getAll().forEach(t => t.kill())`.

---

## Essential Code Patterns

### 1. Staggered Scroll Reveal with ScrollTrigger
```javascript
gsap.registerPlugin(ScrollTrigger);

gsap.from(".feature-card", {
  scrollTrigger: {
    trigger: ".features-grid",
    start: "top 80%",
    toggleActions: "play none none reverse",
  },
  y: 30,
  opacity: 0,
  duration: 0.6,
  stagger: 0.12,
  ease: "power2.out"
});
```

### 2. Engaging Hero Entrance Timeline
```javascript
const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

heroTl
  .from(".hero-badge", { opacity: 0, y: -15, duration: 0.5 })
  .from(".hero-title", { opacity: 0, y: 25, duration: 0.7 }, "-=0.3")
  .from(".hero-lead", { opacity: 0, y: 20, duration: 0.6 }, "-=0.4")
  .from(".hero-cta-group .btn", { opacity: 0, scale: 0.95, stagger: 0.1, duration: 0.4 }, "-=0.3")
  .from(".hero-visual", { opacity: 0, scale: 0.92, duration: 0.8, ease: "back.out(1.2)" }, "-=0.5");
```

### 3. Tactile 3D Tilt Card Micro-interaction
```javascript
const card = document.querySelector(".interactive-card");
const xTo = gsap.quickTo(card, "rotateY", { duration: 0.3, ease: "power2" });
const yTo = gsap.quickTo(card, "rotateX", { duration: 0.3, ease: "power2" });

card.addEventListener("mousemove", (e) => {
  const rect = card.getBoundingClientRect();
  const px = (e.clientX - rect.left) / rect.width - 0.5;
  const py = (e.clientY - rect.top) / rect.height - 0.5;
  xTo(px * 16);  // rotateY
  yTo(-py * 16); // rotateX
});

card.addEventListener("mouseleave", () => {
  xTo(0);
  yTo(0);
});
```

### 4. Animated Stats / Numeric Counters
```javascript
document.querySelectorAll(".stat-counter").forEach((counter) => {
  const targetVal = parseFloat(counter.dataset.target) || 0;
  const state = { val: 0 };

  gsap.to(state, {
    val: targetVal,
    duration: 1.8,
    ease: "power2.out",
    scrollTrigger: {
      trigger: counter,
      start: "top 85%",
      once: true
    },
    onUpdate: () => {
      counter.textContent = Math.floor(state.val).toLocaleString();
    }
  });
});
```

---

## Curated Examples

Review the production-ready templates inside `examples/`:
- `examples/scroll-reveal.js`
- `examples/hero-timeline.js`
- `examples/interactive-cards.js`
- `examples/count-up.js`
- `examples/split-text-reveal.js`

