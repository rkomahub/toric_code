import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch

# This function visualizes stabilizer expectation values
# X-groups and Z-groups are colored differently
def excitation_plot(x_expvals, z_expvals, xgroup_sites, zgroup_sites, width, height):
    # Dark color = excitation (expval < 0)
    # Light color = no excitation (expval > 0)
    x_color = lambda val: "black" if val < 0 else "lavender"
    z_color = lambda val: "red" if val < 0 else "mistyrose"

    fig, ax = plt.subplots()

    # Draw torus boundaries and clean axes
    from .plot_groups import misc_plot_formatting
    fig, ax = misc_plot_formatting(fig, ax, width, height)

    # Draw X-groups (plaquettes → magnetic sector)
    for val, sites in zip(x_expvals, xgroup_sites):
        ax.add_patch(
            Polygon(sites, color=x_color(val), zorder=0)
        )

    # Draw Z-groups (stars → electric sector)
    for val, sites in zip(z_expvals, zgroup_sites):
        ax.add_patch(
            Polygon(sites, color=z_color(val), zorder=0)
        )

    # Legend (Kitaev convention)
    handles = [
        Patch(color="black", label="X-group excitation (magnetic m)"),
        Patch(color="lavender", label="X-group ground"),
        Patch(color="red", label="Z-group excitation (electric e)"),
        Patch(color="mistyrose", label="Z-group ground"),
    ]

    plt.legend(handles=handles, ncol=2, loc="lower left")

    return fig, ax