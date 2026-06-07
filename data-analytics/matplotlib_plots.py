"""
Matplotlib Plots line, bar, scatter, subplots, styling.

Matplotlib is the most versatile plotting library in Python.
Everything else (seaborn, plotly) is built on top of it.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# =============================================================================
# LINE PLOTS
# =============================================================================

def line_plot():
    """Basic line plot with styling."""
    x = np.linspace(0, 2 * np.pi, 100)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, np.sin(x), label="sin(x)", linewidth=2, color="#2196F3")
    ax.plot(x, np.cos(x), label="cos(x)", linewidth=2, color="#FF5722",
            linestyle="--")
    ax.plot(x, np.sin(x) * np.cos(x), label="sin·cos",
            linewidth=1.5, color="#4CAF50", linestyle="-.")

    ax.set_xlabel("x (radians)")
    ax.set_ylabel("y")
    ax.set_title("Trigonometric Functions")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color="black", linewidth=0.5)

    plt.tight_layout()
    plt.savefig("line_plot.png", dpi=150)
    plt.close()
    print("  Saved: line_plot.png")


# =============================================================================
# BAR CHARTS
# =============================================================================

def bar_chart():
    """Vertical and horizontal bar charts."""
    categories = ["Python", "JavaScript", "TypeScript", "Go", "Rust"]
    values = [85, 72, 68, 45, 38]
    colors = ["#3776AB", "#F7DF1E", "#3178C6", "#00ADD8", "#CE422B"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Vertical bar chart
    bars = ax1.bar(categories, values, color=colors, edgecolor="white", linewidth=0.5)
    ax1.set_title("Language Popularity (Vertical)")
    ax1.set_ylabel("Score")
    ax1.set_ylim(0, 100)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(val), ha="center", va="bottom", fontweight="bold")

    # Horizontal bar chart
    ax2.barh(categories, values, color=colors, edgecolor="white", linewidth=0.5)
    ax2.set_title("Language Popularity (Horizontal)")
    ax2.set_xlabel("Score")
    ax2.set_xlim(0, 100)

    plt.tight_layout()
    plt.savefig("bar_chart.png", dpi=150)
    plt.close()
    print("  Saved: bar_chart.png")


# =============================================================================
# SCATTER PLOTS
# =============================================================================

def scatter_plot():
    """Scatter plot with size and color mapping."""
    np.random.seed(42)
    n = 50

    x = np.random.rand(n) * 100         # Experience (months)
    y = x * 800 + np.random.randn(n) * 10000 + 40000  # Salary
    sizes = np.random.rand(n) * 200 + 50  # Bubble size
    colors = np.random.rand(n)            # Color mapping

    fig, ax = plt.subplots(figsize=(10, 7))

    scatter = ax.scatter(x, y, s=sizes, c=colors, cmap="viridis",
                         alpha=0.7, edgecolors="white", linewidth=0.5)

    ax.set_xlabel("Experience (months)")
    ax.set_ylabel("Salary ($)")
    ax.set_title("Experience vs Salary")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x:,.0f}"))

    plt.colorbar(scatter, ax=ax, label="Performance Score")
    plt.tight_layout()
    plt.savefig("scatter_plot.png", dpi=150)
    plt.close()
    print("  Saved: scatter_plot.png")


# =============================================================================
# SUBPLOTS multiple plots in one figure
# =============================================================================

def subplots_demo():
    """Create a grid of subplots."""
    np.random.seed(42)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Histogram
    data = np.random.randn(1000)
    axes[0, 0].hist(data, bins=30, color="#42A5F5", edgecolor="white",
                     alpha=0.8)
    axes[0, 0].set_title("Normal Distribution")
    axes[0, 0].axvline(data.mean(), color="red", linestyle="--", label="Mean")
    axes[0, 0].legend()

    # Plot 2: Pie chart
    sizes = [35, 25, 20, 15, 5]
    labels = ["Python", "JS", "Go", "Rust", "Other"]
    explode = (0.05, 0, 0, 0, 0)
    axes[0, 1].pie(sizes, explode=explode, labels=labels, autopct="%1.0f%%",
                    colors=plt.cm.Set3.colors[:5])
    axes[0, 1].set_title("Language Usage")

    # Plot 3: Box plot
    data = [np.random.normal(loc, 1, 100) for loc in [2, 3, 4, 3.5]]
    bp = axes[1, 0].boxplot(data, labels=["Q1", "Q2", "Q3", "Q4"],
                             patch_artist=True)
    for patch, color in zip(bp["boxes"], ["#66BB6A", "#42A5F5", "#FFA726", "#EF5350"]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    axes[1, 0].set_title("Quarterly Performance")
    axes[1, 0].set_ylabel("Score")

    # Plot 4: Area/Fill plot
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) + 2
    y2 = np.cos(x) + 2
    axes[1, 1].fill_between(x, y1, alpha=0.3, label="Series A", color="#42A5F5")
    axes[1, 1].fill_between(x, y2, alpha=0.3, label="Series B", color="#FFA726")
    axes[1, 1].plot(x, y1, color="#1565C0", linewidth=1.5)
    axes[1, 1].plot(x, y2, color="#E65100", linewidth=1.5)
    axes[1, 1].set_title("Area Chart")
    axes[1, 1].legend()

    plt.suptitle("Subplot Gallery", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("subplots.png", dpi=150)
    plt.close()
    print("  Saved: subplots.png")


# =============================================================================
# STYLING make publication-ready plots
# =============================================================================

def styled_plot():
    """Demonstrate plot styling and customization."""
    # Use a built-in style
    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Generate sample time series data
        dates = np.arange("2024-01", "2025-01", dtype="datetime64[M]")
        revenue = np.cumsum(np.random.randn(12) * 5000 + 10000)
        costs = np.cumsum(np.random.randn(12) * 3000 + 7000)

        ax.plot(dates, revenue, marker="o", linewidth=2.5,
                color="#1976D2", label="Revenue", markersize=6)
        ax.plot(dates, costs, marker="s", linewidth=2.5,
                color="#D32F2F", label="Costs", markersize=6)

        # Fill the profit area
        ax.fill_between(dates, costs, revenue,
                        where=(revenue > costs),
                        alpha=0.1, color="green", label="Profit")
        ax.fill_between(dates, costs, revenue,
                        where=(revenue <= costs),
                        alpha=0.1, color="red", label="Loss")

        ax.set_title("Revenue vs Costs 2024", fontsize=14, pad=15)
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount ($)")
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x/1000:.0f}K"))
        ax.legend(loc="upper left", framealpha=0.9)

        # Annotations
        max_idx = np.argmax(revenue - costs)
        ax.annotate(
            f"Best month\n${(revenue[max_idx]-costs[max_idx])/1000:.0f}K profit",
            xy=(dates[max_idx], revenue[max_idx]),
            xytext=(dates[max_idx], revenue[max_idx] + 15000),
            arrowprops=dict(arrowstyle="->", color="gray"),
            fontsize=9, ha="center",
        )

        plt.tight_layout()
        plt.savefig("styled_plot.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("  Saved: styled_plot.png")


# =============================================================================
# HEATMAP
# =============================================================================

def heatmap():
    """Correlation heatmap useful for data exploration."""
    np.random.seed(42)

    # Simulate correlated data
    data = np.random.randn(100, 5)
    data[:, 1] = data[:, 0] * 0.8 + np.random.randn(100) * 0.5
    data[:, 3] = -data[:, 2] * 0.6 + np.random.randn(100) * 0.7

    labels = ["Revenue", "Users", "Bounce", "Sessions", "CTR"]
    correlation = np.corrcoef(data.T)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(correlation, cmap="RdBu_r", vmin=-1, vmax=1)

    # Add labels
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    # Add correlation values
    for i in range(len(labels)):
        for j in range(len(labels)):
            color = "white" if abs(correlation[i, j]) > 0.5 else "black"
            ax.text(j, i, f"{correlation[i, j]:.2f}",
                   ha="center", va="center", color=color, fontsize=10)

    plt.colorbar(im, ax=ax, label="Correlation")
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig("heatmap.png", dpi=150)
    plt.close()
    print("  Saved: heatmap.png")


if __name__ == "__main__":
    print("=" * 60)
    print("Matplotlib Demo Generating Plots")
    print("=" * 60)
    print("(Plots saved as PNG files in current directory)\n")

    line_plot()
    bar_chart()
    scatter_plot()
    subplots_demo()
    styled_plot()
    heatmap()

    print("\nAll plots generated! Open the PNG files to view.")
    print("\nAvailable styles:", plt.style.available[:10])
