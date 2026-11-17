# Performance Optimization & Accessibility in GSAP

Smooth 60fps animations require strict adherence to browser rendering pipeline constraints and universal accessibility standards.

---

## 1. Browser Rendering Pipeline & GPU Compositing

Modern browsers render in three main stages:
1. **Layout (Reflow)**: Calculating geometric positions. (`width`, `height`, `top`, `left`, `margin`, `padding`). *Expensive!*
2. **Paint (Repaint)**: Rasterizing pixels, colors, text, borders, shadows. (`background`, `color`, `box-shadow`). *Moderate.*
3. **Composite**: Combining GPU layers. (`transform`, `opacity`). *Ultra Fast (GPU accelerated).*

### Golden Rule:
**Only animate `transform` (`x`, `y`, `scale`, `rotation`) and `opacity`** whenever possible.

```javascript
// ❌ BAD: Triggers continuous Layout & Paint calculations
gsap.to(".box", { top: 100, left: 200, width: 300 });

// ✅ GOOD: Composited entirely on the GPU thread
gsap.to(".box", { y: 100, x: 200, scale: 1.5 });
```

---

## 2. Strategic Use of `will-change`

Applying `will-change: transform` informs the browser to promote the element to its own GPU compositor layer:

```css
/* Apply only to elements undergoing intensive, continuous animation */
.animated-card {
  will-change: transform, opacity;
}
```

> **Warning**: Do not apply `will-change` globally to hundreds of elements, as excessive layer creation exhausts device VRAM. Remove `will-change` after the animation completes:
```javascript
gsap.to(".heavy-element", {
  x: 200,
  duration: 1,
  onStart: () => gsap.set(".heavy-element", { willChange: "transform" }),
  onComplete: () => gsap.set(".heavy-element", { willChange: "auto" })
});
```

---

## 3. High-Frequency Events: Avoid Tween Allocation Churn

In mousemove or scroll event handlers, instantiating new `gsap.to()` tweens on every frame causes heavy garbage collection pauses.

Use `gsap.quickTo()`:

```javascript
// ❌ SLOW: Allocates 60+ tween objects per second
window.addEventListener("pointermove", (e) => {
  gsap.to(".follower", { x: e.clientX, y: e.clientY, duration: 0.2 });
});

// ✅ FAST: Pre-allocates single tween, updates target values instantaneously
const xTo = gsap.quickTo(".follower", "x", { duration: 0.25, ease: "power2" });
const yTo = gsap.quickTo(".follower", "y", { duration: 0.25, ease: "power2" });

window.addEventListener("pointermove", (e) => {
  xTo(e.clientX);
  yTo(e.clientY);
});
```

---

## 4. Accessibility & `prefers-reduced-motion`

Under WCAG 2.2 (Success Criterion 2.3.3: Animation from Interactions), users can configure their OS to reduce non-essential motion.

### Implementing Reduced Motion with `gsap.matchMedia()`

```javascript
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Option A: Instant jump to final state
  gsap.set(".reveal-item", { opacity: 1, y: 0, scale: 1 });

  // Option B: Subtle fade only without spatial movement
  gsap.from(".fade-item", { opacity: 0, duration: 0.3 });
});

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // Full expressive animation suite
  gsap.from(".reveal-item", {
    opacity: 0,
    y: 40,
    scale: 0.95,
    stagger: 0.1,
    duration: 0.8,
    ease: "power3.out"
  });
});
```

---

## 5. Memory Management & Cleanup Protocols

When components unmount or pages change via AJAX / Turbolinks / HTMX:

```javascript
// Scope all animations inside a gsap.context()
const ctx = gsap.context(() => {
  gsap.to(".card", { y: -10 });
  ScrollTrigger.create({ trigger: ".hero", start: "top top" });
}, document.querySelector("#feature-section"));

// On unmount / view teardown:
ctx.revert(); // Automatically kills all tweens, timelines, and ScrollTriggers within context!
```

