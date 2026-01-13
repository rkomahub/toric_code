import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from toric.plot_groups import misc_plot_formatting


def set_matplotlib_style():
    plt.rcParams.update({
        "figure.figsize": (6, 6),
        "font.size": 12,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def save(fig, name, folder="output/png"):
    fig.savefig(f"{folder}/{name}.png", bbox_inches="tight")


def excitation_plot(
    x_expvals,
    z_expvals,
    xgroup_sites,
    zgroup_sites,
    width,
    height,
):
    """
    Visualize X- and Z-group stabilizer expectation values.

    Kitaev convention:
    - Z-group (∏Z, stars)     → electric anyons (e)
    - X-group (∏X, plaquettes) → magnetic anyons (m)

    Dark color = excitation (expval < 0)
    Light color = ground state (expval > 0)
    """
    # Colors encode stabilizer eigenvalues only
    x_color = lambda v: "firebrick" if v < 0 else "mistyrose"   # X-group → magnetic
    z_color = lambda v: "steelblue" if v < 0 else "lavender"   # Z-group → electric

    fig, ax = plt.subplots()
    fig, ax = misc_plot_formatting(fig, ax, width, height)

    # X-group stabilizers (plaquettes → magnetic)
    for val, sites in zip(x_expvals, xgroup_sites):
        ax.add_patch(Polygon(sites, color=x_color(val), zorder=0))

    # Z-group stabilizers (stars → electric)
    for val, sites in zip(z_expvals, zgroup_sites):
        ax.add_patch(Polygon(sites, color=z_color(val), zorder=0))

    handles = [
        Patch(color="steelblue", label="Z-group excitation (electric e)"),
        Patch(color="lavender", label="Z-group ground"),
        Patch(color="firebrick", label="X-group excitation (magnetic m)"),
        Patch(color="mistyrose", label="X-group ground"),
    ]
    ax.legend(handles=handles, ncol=2, loc="lower left")

    return fig, ax