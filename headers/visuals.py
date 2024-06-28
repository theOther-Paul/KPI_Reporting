import matplotlib
import matplotlib.pyplot as plt

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import numpy as np

"""
@package docstring

This file serves as a helper module for both the primary and secondary interfaces.
Its primary purpose is to generate graphics and dataframes for both visual representations and reports

"""

matplotlib.use("svg")


def show_fruits():
    """
    The function `show_fruits` creates a bar chart displaying the supply of different fruits categorized
    by color.
    :return: The function `show_fruits()` is returning a Matplotlib chart object with the specified
    fruit supply data plotted as bar charts categorized by kind and color.
    """
    fig, ax = plt.subplots()

    fruits = ["apple", "blueberry", "cherry", "orange"]
    counts = [40, 100, 30, 55]
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel("fruit supply")
    ax.set_title("Fruit supply by kind and color")
    ax.legend(title="Fruit color")

    return MatplotlibChart(fig, expand=True)


def show_line():
    """
    The function `show_line` generates two signals with a coherent part at 10Hz and a random part, plots
    them, calculates their coherence, and returns a Matplotlib chart.
    :return: The `show_line` function is returning a Matplotlib chart object created using the
    `MatplotlibChart` class with the figure `fig` that contains two subplots. The first subplot displays
    two signals `s1` and `s2` plotted against time `t`, while the second subplot displays the coherence
    between the two signals using the `cohere` function. The x-axis of the first
    """
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel("time")
    axs[0].set_ylabel("s1 and s2")
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1.0 / dt)
    axs[1].set_ylabel("coherence")

    fig.tight_layout()

    return MatplotlibChart(fig, expand=True)


def new_table_function():
    pass
