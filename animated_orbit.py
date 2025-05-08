import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Parameters
m1 = 1
m2 = 6
Lz = 2.0
alpha = 2.0
E = -0.20

mu = m1 * m2 / (m1 + m2)
arg = 1 + (2 * E * Lz**2) / (mu * alpha**2)

if arg < 0:
    print("❌ Unphysical parameters: eccentricity would be complex.")
else:
    p = Lz**2 / (mu * alpha)
    epsilon = np.sqrt(arg)

    theta = np.linspace(0, 2 * np.pi, 1000)
    denom = 1 + epsilon * np.cos(theta)
    r = np.where(np.abs(denom) > 1e-3, p / denom, np.nan)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    valid = denom > 0
    x = r[valid] * np.cos(theta[valid])
    y = r[valid] * np.sin(theta[valid])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title(f"Orbit of Mass 2 (ε = {epsilon:.2f})")

    ax.plot(x, y, 'r', lw=1, label='Orbit')
    mass2, = ax.plot([], [], 'ro', label='Mass 2')
    ax.plot(0, 0, 'ko', label='Fixed Mass 1')
    ax.legend()

    # Store arrow in a list to allow reassignment inside update()
    velocity_arrow = [ax.arrow(0, 0, 0, 0, head_width=0.5, color='blue')]

    def update(frame):
        i = frame
        mass2.set_data([x[i]], [y[i]])
        r_i = np.sqrt(x[i]**2 + y[i]**2)

        # Real velocity magnitude from mechanics
        if r_i == 0:
            v_mag = 0
        else:
            v_mag = np.sqrt(2 * (E + alpha / r_i) / mu)

        # Tangent direction
        if i < len(x) - 1:
            dx = x[i+1] - x[i]
            dy = y[i+1] - y[i]
        else:
            dx = x[i] - x[i-1]
            dy = y[i] - y[i-1]

        tangent_norm = np.sqrt(dx**2 + dy**2)
        if tangent_norm == 0:
            vx, vy = 0, 0
        else:
            vx = v_mag * dx / tangent_norm
            vy = v_mag * dy / tangent_norm

        # Remove and redraw arrow
        velocity_arrow[0].remove()
        velocity_arrow[0] = ax.arrow(x[i], y[i], vx, vy, head_width=0.5, color='blue')

        return mass2, velocity_arrow[0]

    anim = FuncAnimation(fig, update, frames=len(x), interval=10, blit=True)

    html_anim = anim.to_html5_video()
    display(HTML(html_anim))
