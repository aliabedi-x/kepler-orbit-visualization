# 🔭 Kepler Orbit & Effective Potential Visualizer

This project visualizes **Keplerian orbits** using two approaches:

1. 📊 A **graph-based interactive tool** showing:
   - Orbital shape (ellipse, parabola, hyperbola)
   - Effective potential \( V_{\text{eff}}(r) \)
   - Total energy, turning points \( r_{\min}, r_{\max} \)
2. 🎥 A **classical animation** of a body orbiting around a fixed central mass

---

## 🖼 Preview

### 📊 Interactive Plot (Orbit + Energy)

<img src="Images/interactive-kepler.png" alt="kepler-graph" width="100%">

### 🎥 Animated Orbit

<img src="Images/kepler-orbit-animation.gif" alt="kepler-anim" width="400">

---

## 🚀 Features

- Simulates orbits for:
  - Bound: Ellipses (ε < 1)
  - Unbound: Parabolas (ε = 1), Hyperbolas (ε > 1)
- Displays:
  - Effective potential curve \( V_{\text{eff}}(r) \)
  - Central potential \( -\alpha/r \)
  - Total energy line and turning points
- Interactive sliders to vary:
  - Masses \( m_1, m_2 \)
  - Angular momentum \( L_z \)
  - Potential strength \( \alpha \)
  - Total energy \( E \)

---

## 📦 Requirements

```bash
pip install numpy matplotlib scipy ipywidgets
