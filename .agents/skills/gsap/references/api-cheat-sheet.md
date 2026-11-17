# GSAP 3 API Cheatsheet & Syntax Reference

## 1. Core Tweening Methods

```javascript
// Animate from current state to destination
gsap.to(".box", { x: 100, duration: 1 });

// Animate from specified values to current state
gsap.from(".box", { opacity: 0, y: 50, duration: 0.8 });

// Explicit starting and ending states
gsap.fromTo(".box", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6 });

// Instant state change (zero duration)
gsap.set(".box", { transformOrigin: "50% 50%", visibility: "visible" });
```

---

## 2. Special Properties

| Property | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `duration` | Number | Duration in seconds (defaults to `0.5`) | `duration: 1.2` |
| `delay` | Number | Wait time in seconds before starting | `delay: 0.3` |
| `ease` | String/Function | Timing/easing curve | `ease: "power2.out"` |
| `stagger` | Number/Object | Time offset between matched elements | `stagger: 0.08` or `{ each: 0.05, from: "center" }` |
| `repeat` | Integer | Repetition count (`-1` for infinite loop) | `repeat: -1` |
| `yoyo` | Boolean | Reverses direction on alternate repeats | `yoyo: true` |
| `repeatDelay`| Number | Wait time between repetitions | `repeatDelay: 0.5` |
| `paused` | Boolean | Starts paused if `true` | `paused: true` |
| `overwrite` | Boolean/String| Tween overwrite mode | `overwrite: "auto"` |

---

## 3. High-Performance CSS Transforms

Always favor GPU-composited CSS properties:

```javascript
gsap.to(element, {
  // Positioning
  x: 50,              // translateX(50px)
  y: -20,             // translateY(-20px)
  xPercent: -50,      // translateX(-50%)
  yPercent: -50,      // translateY(-50%)
  z: 10,              // translateZ(10px)

  // Scaling & Rotation
  scale: 1.1,         // scale(1.1)
  scaleX: 1.2,
  scaleY: 0.8,
  rotation: 45,       // rotate(45deg)
  rotationX: 15,
  rotationY: 20,
  skewX: 10,

  // Visuals
  opacity: 1,
  autoAlpha: 1,       // Sets opacity AND toggles visibility: hidden at 0
  transformOrigin: "center center",
  duration: 0.5
});
```

---

## 4. Timelines & The Position Parameter

Timelines synchronize complex multi-element choreographies.

```javascript
const tl = gsap.timeline({
  defaults: { duration: 0.5, ease: "power2.out" },
  repeat: 0,
  onComplete: () => console.log("Timeline finished!")
});

tl.to(".header", { y: 0, opacity: 1 })
  .to(".sidebar", { x: 0 }, "-=0.2")       // Overlap: starts 0.2s before header ends
  .to(".card", { scale: 1 }, "<")          // Aligns with start of previous tween
  .to(".badge", { rotation: 360 }, "+=0.3")// Gap: starts 0.3s after card ends
  .addLabel("step2")                       // Timeline bookmark
  .to(".footer", { opacity: 1 }, "step2"); // Plays at the marker
```

### Timeline Controls:
- `tl.play()` / `tl.pause()` / `tl.resume()`
- `tl.reverse()`
- `tl.seek(1.5)` (Jump to timestamp in seconds)
- `tl.progress(0.5)` (Jump to percentage: 0 to 1)
- `tl.timeScale(2)` (2x fast forward) or `tl.timeScale(0.5)` (slow motion)
- `tl.kill()` (Destroys tween, stops ticker updates)

---

## 5. Easing Curves

GSAP eases follow a `<type>.<direction>` convention:

- **Standard Eases**:
  - `power1.out` (gentle ease-out)
  - `power2.out` (standard UI ease-out - recommended default)
  - `power3.out` (strong ease-out for modals and slides)
  - `power4.out` (dramatic, high-velocity deceleration)
  - `none` (linear - ideal for endless continuous loops)
- **Expressive Eases**:
  - `back.out(1.7)` (slight overshoot, playful UI badges)
  - `elastic.out(1, 0.4)` (springy bounce back)
  - `bounce.out` (ball bounce effect)
  - `expo.out` (hyper-fast explosion out, smooth deceleration)
  - `circ.out` (steep curve)

---

## 6. Utility Functions

GSAP provides high-performance utility helpers under `gsap.utils`:

```javascript
// Convert NodeList or selector to Array cleanly
const items = gsap.utils.toArray(".item");

// Clamp number between min and max
const clamp = gsap.utils.clamp(0, 100, inputValue);

// Map range (e.g. scroll 0..500px to opacity 1..0)
const mapper = gsap.utils.mapRange(0, 500, 1, 0);
const opacity = mapper(window.scrollY);

// Random number or item selection
const randomDelay = gsap.utils.random(0.1, 0.5);
const randomColor = gsap.utils.random(["#2563eb", "#059669", "#dc2626"]);

// Optimize mousemove loops (zero allocation)
const quickX = gsap.quickTo(".ball", "x", { duration: 0.2, ease: "power3" });
window.addEventListener("mousemove", (e) => quickX(e.clientX));
```

