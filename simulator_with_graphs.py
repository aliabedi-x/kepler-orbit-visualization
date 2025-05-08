import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, Dropdown, fixed, VBox, HBox, Button, Output, interactive, HTML
from scipy.optimize import fsolve
from matplotlib.collections import LineCollection


title = HTML("<h2 style='text-align:center;'>Kepler Orbit Simulator</h2>")

def safe_fsolve(func, x0):
    try:
        root, info, ier, msg = fsolve(func, x0, full_output=True)
        if ier == 1:
            return root[0]
        else:
            return None
    except:
        return None


def kepler_combined(m1, m2, Lz, alpha, E):
    mu = m1 * m2 / (m1 + m2)

    theta_full = np.linspace(0, 2 * np.pi, 1000)
    arg = 1 + (2 * E * Lz**2) / (mu * alpha**2)

    if arg < 0:
        print("❌ Invalid orbit: eccentricity would be complex. Choose higher E or lower Lz.")
        return

    epsilon = np.sqrt(arg)
    p = Lz**2 / (mu * alpha)
    if epsilon >= 1:
        valid = np.abs(1 + epsilon * np.cos(theta_full)) > 1e-3
        theta = theta_full[valid]
    else:
        theta = theta_full

    denom = 1 + epsilon * np.cos(theta)
    r = np.where(np.abs(denom) > 1e-5, p / denom, np.nan)
    x2 = r * np.cos(theta)
    y2 = r * np.sin(theta)

    dr_dtheta = (p * epsilon * np.sin(theta)) / (1 + epsilon * np.cos(theta))**2
    theta_dot = Lz / (mu * r**2)
    r_dot = dr_dtheta * theta_dot
    T = 0.5 * mu * (r_dot**2 + (r**2 * theta_dot**2))
    U = -alpha / r
    E_total = T + U

    r_plot = np.linspace(0.01, 30, 1000)
    Vcentral = -alpha / r_plot
    Veff = Lz**2 / (2 * mu * r_plot**2) + Vcentral

    def veff_eq(rval):
        return Lz**2 / (2 * mu * rval**2) - alpha / rval - E

    rmin = safe_fsolve(veff_eq, 0.5)
    rmax = safe_fsolve(veff_eq, 5.0)

    fig, axs = plt.subplots(1, 3, figsize=(20, 6))

    axs[0].plot(0, 0, 'ko', label='Fixed Mass (m1)', markersize=8)
    speed = np.sqrt(r_dot**2 + (r**2 * theta_dot**2))
    points = np.array([x2, y2]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap='plasma', norm=plt.Normalize(speed.min(), speed.max()))
    lc.set_array(speed)
    lc.set_linewidth(2)
    line = axs[0].add_collection(lc)
    fig.colorbar(line, ax=axs[0], label='Speed')
    axs[0].plot(x2, y2, 'r', label='Orbiting Mass (m2)')
    axs[0].set_aspect('equal')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y')
    axs[0].grid(True)
    axs[0].legend(loc='lower left')
    axs[0].set_title(f'Orbit (ε = {epsilon:.2f})')

    if epsilon < 1:
        orbit_type = 'Ellipse'
    elif np.isclose(epsilon, 1.0, atol=1e-2):
        orbit_type = 'Parabola'
    else:
        orbit_type = 'Hyperbola'

    axs[0].text(0.05, 0.95, orbit_type, transform=axs[0].transAxes,
                fontsize=12, verticalalignment='top',
                bbox=dict(boxstyle="round", facecolor="wheat"))
    if epsilon >= 1:
        axs[0].set_xlim(-10, 10)
        axs[0].set_ylim(-10, 10)

    axs[1].plot(r_plot, Veff, label=r'$V_{\mathrm{eff}}(r)$', lw=2)
    axs[1].plot(r_plot, Vcentral, '--', label=r'$V_{\mathrm{central}}$', color='orange')
    axs[1].hlines(E, r_plot[0], r_plot[-1], color='red', linestyle='--', label='Total Energy $E$')
    if rmin and rmax:
        axs[1].plot(rmin, E, 'go', label='Perihelion $r_{\min}$')
        axs[1].plot(rmax, E, 'mo', label='Aphelion $r_{\max}$')
        axs[1].plot((rmin + rmax) / 2, E, 'ro', label=r'Initial $r(t_0)$')
    axs[1].set_xlim(0, 30)
    axs[1].set_ylim(min(Veff) - 1, 2)
    axs[1].set_xlabel('r')
    axs[1].set_ylabel('Energy')
    axs[1].grid(True)
    axs[1].legend()
    axs[1].set_title('Effective Potential')

    axs[2].plot(theta, T, label='Kinetic Energy T', lw=2)
    axs[2].plot(theta, U, label='Potential Energy U', lw=2)
    axs[2].plot(theta, E_total, label='Total Energy E', linestyle='--', lw=2)
    axs[2].set_xlabel('θ (rad)')
    axs[2].set_ylabel('Energy')
    axs[2].grid(True)
    axs[2].legend()
    axs[2].set_title('Energy Breakdown vs. θ')

    plt.tight_layout()
    plt.show()


presets = {
    'Custom': {'m1': 1.0, 'm2': 6.0, 'Lz': 2.0, 'alpha': 2.0, 'E': -0.4},
}

m1_slider = FloatSlider(min=0.1, max=350000, step=0.1, value=1.0, description='Mass 1')
m2_slider = FloatSlider(min=0.1, max=10.0, step=0.1, value=6.0, description='Mass 2')
Lz_slider = FloatSlider(min=0.1, max=50.0, step=0.1, value=2.0, description='Lz')
alpha_slider = FloatSlider(min=0.1, max=100.0, step=0.1, value=2.0, description='α / k')
E_slider = FloatSlider(min=-5.0, max=5.0, step=0.1, value=-0.4, description='E')
preset_dropdown = Dropdown(options=list(presets.keys()), description='Preset')


def update_from_preset(change):
    preset = presets[change['new']]
    m1_slider = FloatSlider(..., layout=dict(width='300px'))
    m2_slider.value = preset['m2']
    Lz_slider.value = preset['Lz']
    alpha_slider.value = preset['alpha']
    E_slider.value = preset['E']

preset_dropdown.observe(update_from_preset, names='value')

ui = VBox([
    title,
    preset_dropdown,
])

interactive_plot = interactive(kepler_combined,
                               m1=m1_slider,
                               m2=m2_slider,
                               Lz=Lz_slider,
                               alpha=alpha_slider,
                               E=E_slider)

display(ui, interactive_plot)

