# GSAP Essential Plugins Overview

GSAP features a modular architecture. Core handles standard tweens and timelines, while specialized plugins handle advanced requirements.

---

## 1. Flip Plugin (Layout Morphing)

**Best for**: Grid filtering, expanding cards to full-screen modals, accordion reordering, list shuffle.

```javascript
gsap.registerPlugin(Flip);

// 1. Capture current DOM state
const state = Flip.getState(".grid-item, .modal-card");

// 2. Mutate DOM or change CSS classes (e.g., move item or add .active class)
item.classList.toggle("expanded");

// 3. Animate between states effortlessly
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  scale: true,
  absolute: true, // Fixes positioning glitches during grid shifts
  onComplete: () => console.log("Flip finished!")
});
```

---

## 2. Draggable Plugin

**Best for**: Sliders, interactive carousels, draggable bottom sheets, reorderable widgets.

```javascript
gsap.registerPlugin(Draggable);

Draggable.create(".drag-handle", {
  type: "x,y",              // "x", "y", "x,y", or "rotation"
  bounds: ".container",     // Constrain within parent element
  inertia: true,            // Throw physics (requires InertiaPlugin)
  edgeResistance: 0.65,     // Resistance when pulled beyond bounds
  onDrag: function() {
    console.log("Current X:", this.x, "Y:", this.y);
  },
  onDragEnd: function() {
    console.log("Drag ended");
  }
});
```

---

## 3. SplitText Plugin

**Best for**: Cinematic character-by-character or word-by-word headline reveals.

```javascript
gsap.registerPlugin(SplitText);

const split = new SplitText(".hero-headline", {
  type: "words,chars",
  charsClass: "char-item"
});

gsap.from(split.chars, {
  opacity: 0,
  y: 30,
  rotateX: -45,
  stagger: 0.02,
  duration: 0.8,
  ease: "back.out(1.4)",
  onComplete: () => split.revert() // Restore original DOM for clean screen reader accessibility
});
```

---

## 4. TextPlugin & ScrambleText

**Best for**: Typewriter effects, dynamic badge text changes, cyber scramble text.

```javascript
gsap.registerPlugin(TextPlugin);

// Typewriter replacement effect
gsap.to(".dynamic-typing", {
  duration: 2,
  text: "Industrial Wastewater & Septic Tank Solutions",
  ease: "none",
  delimiter: "" // Types character-by-character
});
```

---

## 5. Observer Plugin

**Best for**: Catching swipe/wheel gestures without relying on native scrolling (e.g. full-screen slide presentations, carousel navigation).

```javascript
gsap.registerPlugin(Observer);

Observer.create({
  target: window,
  type: "wheel,touch,pointer",
  onUp: () => goToPreviousSlide(),
  onDown: () => goToNextSlide(),
  tolerance: 15,
  preventDefault: true
});
```

---

## 6. ScrollToPlugin

**Best for**: Smooth navigation link scrolling with fixed header offset.

```javascript
gsap.registerPlugin(ScrollToPlugin);

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    const target = link.getAttribute("href");
    gsap.to(window, {
      duration: 0.8,
      scrollTo: { y: target, offsetY: 70 }, // 70px accounts for sticky navbar!
      ease: "power2.inOut"
    });
  });
});
```

