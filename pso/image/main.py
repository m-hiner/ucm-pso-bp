from pathlib import Path

from pso.config import Config
from pso.typing import CircleArray


def plot(position_array: CircleArray, config: Config, path: Path):
    # imported here so runs without image output don't need matplotlib
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle

    width = config.search_space_width
    height = config.search_space_height
    radius = config.circle_radius
    iterations = config.iterations

    fig, ax = plt.subplots(figsize=(6, 6 * height / width))
    ax.add_patch(Rectangle((0, 0), width, height,
                           fill=False, edgecolor="black", linewidth=1.5))
    for x, y in position_array:
        ax.add_patch(Circle((x, y), radius, facecolor="tab:blue",
                            edgecolor="navy", alpha=0.6))

    margin = 0.05 * max(width, height)
    ax.set_xlim(-margin, width + margin)
    ax.set_ylim(-margin, height + margin)
    ax.set_aspect("equal")
    ax.set_title(
        f"{len(position_array)} circles, r = {radius}, "
        f"{width} × {height}, {iterations} iterations")

    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
