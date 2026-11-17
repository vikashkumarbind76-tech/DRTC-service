# ScrollTrigger Expert Guide

`ScrollTrigger` turns any GSAP tween or timeline into a scroll-driven or scroll-triggered animation.

## 1. Setup & Registration

Always register the plugin once before creating any scroll-bound tweens:

```javascript
gsap.registerPlugin(ScrollTrigger);
```

---

## 2. Basic ScrollTrigger Syntax

Attach the `scrollTrigger` object directly to a tween or timeline:

```javascript
gsap.to(".box", {
  x: 200,
  duration: 1,
  scrollTrigger: {
    trigger: ".box",        // Element that triggers the animation
    start: "top 80%",       // When top of trigger hits 80% down viewport
    end: "bottom 20%",      // When bottom of trigger hits 20% from viewport top
    toggleActions: "play none none reverse", // onEnter onLeave onEnterBack onLeaveBack
    markers: false          // Set to true only during development!
  }
});
```

---

## 3. Understanding `toggleActions`

`toggleActions` controls playback across 4 scroll events:
`"onEnter onLeave onEnterBack onLeaveBack"`

Options for each position:
- `play` - Plays tween forward.
- `pause` - Pauses tween at current position.
- `resume` - Resumes playback in current direction.
- `reverse` - Reverses animation back to beginning.
- `restart` - Restarts from beginning.
- `reset` - Instantly returns to start values without animating.
- `complete` - Instantly jumps to final state.
- `none` - No action taken.

**Common Combinations:**
- `"play none none none"`: Runs once when scrolled into view.
- `"play none none reverse"`: Runs forward when scrolling down, reverses when scrolling back up.
- `"restart pause resume reverse"`: Restarts on enter, pauses if scrolled past, resumes if scrolled back in.

---

## 4. Scrubbing & Pinning

### Continuous Scrub (`scrub`)
Binds the animation progress directly to the scrollbar:

```javascript
gsap.to(".progress-bar", {
  scaleX: 1,
  ease: "none",
  scrollTrigger: {
    trigger: "#main-content",
    start: "top top",
    end: "bottom bottom",
    scrub: 0.8 // Number in seconds creates a smooth catch-up effect!
  }
});
```

### Sticky Pinning (`pin`)
Locks an element in place while subsequent content scrolls through:

```javascript
gsap.timeline({
  scrollTrigger: {
    trigger: ".pinned-section",
    start: "top top",
    end: "+=2000",       // Pins for 2000px of scrolling
    pin: true,
    pinSpacing: true,    // Adds padding to push downstream content
    scrub: 1
  }
})
.to(".slide-1", { opacity: 0, y: -50 })
.from(".slide-2", { opacity: 0, y: 50 }, "<")
.to(".slide-2", { opacity: 0, y: -50 })
.from(".slide-3", { opacity: 0, y: 50 }, "<");
```

---

## 5. Efficient Grid Batching (`ScrollTrigger.batch`)

When animating 20+ grid items, creating 20 individual triggers creates overhead. Use `ScrollTrigger.batch` instead:

```javascript
ScrollTrigger.batch(".gallery-item", {
  start: "top 85%",
  onEnter: (batch) => {
    gsap.from(batch, {
      opacity: 0,
      y: 30,
      stagger: 0.1,
      duration: 0.6,
      ease: "power2.out",
      overwrite: true
    });
  },
  once: true // Only animate once
});
```

---

## 6. Responsive Breakpoints & Reduced Motion (`gsap.matchMedia`)

Never bind heavy scroll pins on mobile without media queries. `gsap.matchMedia()` cleanly builds and automatically destroys triggers when resizing across breakpoints:

```javascript
const mm = gsap.matchMedia();

mm.add({
  // Desktop
  isDesktop: "(min-width: 992px)",
  // Mobile / Tablet
  isMobile: "(max-width: 991px)",
  // Accessibility check
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (context) => {
  const { isDesktop, isMobile, reduceMotion } = context.conditions;

  if (reduceMotion) {
    // Render static visible elements with no animations
    gsap.set(".hero-card, .scroll-fade", { opacity: 1, y: 0 });
    return;
  }

  if (isDesktop) {
    // Rich multi-column parallax & pin
    gsap.to(".sticky-sidebar", {
      scrollTrigger: {
        trigger: ".content-wrapper",
        start: "top 80px",
        end: "bottom bottom",
        pin: true
      }
    });
  }

  if (isMobile) {
    // Simple lightweight fade
    gsap.from(".card", {
      scrollTrigger: {
        trigger: ".card",
        start: "top 90%"
      },
      opacity: 0,
      y: 15,
      duration: 0.4
    });
  }
});
```

---

## 7. Dynamic Layout Recalculation (`ScrollTrigger.refresh()`)

If layout changes after page load (e.g., images loading, accordion expanding, web fonts rendering):

```javascript
// Force ScrollTrigger to re-calculate trigger offsets
ScrollTrigger.refresh();

// Or hook to window load event
window.addEventListener("load", () => ScrollTrigger.refresh());
```

