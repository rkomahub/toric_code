import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from .groups import build_xgroup_sites, build_zgroup_sites

def misc_plot_formatting(fig, ax, width, height):
    plt.hlines([-0.5, height - 0.5], -0.5, width - 0.5,
               linestyle="dotted", color="black")
    plt.vlines([-0.5, width - 0.5], -0.5, height - 0.5,
               linestyle="dashed", color="black")

    plt.xticks(range(width + 1), [str(i % width) for i in range(width + 1)])
    plt.yticks(range(height + 1), [str(i % height) for i in range(height + 1)])

    for d in ["top", "right", "bottom", "left"]:
        ax.spines[d].set_visible(False)

    return fig, ax


width, height = 6, 4

xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)

fig, ax = plt.subplots()
fig, ax = misc_plot_formatting(fig, ax, width, height)

for group in xgroup_sites:
    x_patch = ax.add_patch(Polygon(group, color="lavender", zorder=0))

for group in zgroup_sites:
    z_patch = ax.add_patch(Polygon(group, color="mistyrose", zorder=0))

all_sites = [(i, j) for i in range(width) for j in range(height)]
plt_sites = ax.scatter(*zip(*all_sites), color="black", zorder=1)

plt.legend([x_patch, z_patch, plt_sites],
           ["XGroup", "ZGroup", "Site"],
           loc="upper left")

plt.savefig("groups.png", dpi=200, bbox_inches="tight")