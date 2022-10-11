import numpy as np
import PyQt5.QtWidgets as qtw

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
)
import matplotlib.pyplot as plt


class MPLWidget(qtw.QWidget):
    """
    A pyqt widget that displays a mpl plot, with a built in toolbar.

    Parameters
    ----------
    alignment : 4-tuple of floats, optional
        The area in figure coordinates where the axes will sit.  Defaults to None, in which
        case the value used is chosen based on the value of parameter blank.  If blank is
        True, uses the value (0.0, 0.0, 1.0, 1.0) in which case the axes cover exactly the
        whole drawing area, which is great if you are displaying an image.  If blank is False,
        uses (.1, .1, .898, .898) which is a good starter option for plots with displayed
        labels, but you may want to tweak manually.  .9 has a tendency to cut off the line on
        the left size of the plot.
        The first two numbers anchor the lower left corner, the second two
        are a span.  The values are all relative to the size of the canvas, so between 0 and
        1.
    fig_size : 2-tuple of floats, optional
        The default size of the figure.  But since pyqt messes with widget size a lot this
        is more of a rough starting guess than an actual set value..
    blank : bool, optional
        If False, the default, draws the plot as normal.
        If True, the canvas will be a blank white square with no axes or anything, ideal
        for drawing.
    args and kwargs passed to qtw.QWidget constructor

    Public Properties
    -----------------
    fig : mpl figure
        A handle to the generated mpl figure.
    ax : mpl axes
        A handle to the generated axes, where you can draw/plot stuff.
    fig_canvas : mpl backend object
        The canvas object that plugs into pyqt.

    Public Methods
    --------------
    draw() :
        Draw or redraw the figure.
    """

    def __init__(
            self,
            name=None,
            blank=False,
    ):
        super().__init__()
        self.fig, self.ax = plt.subplots(constrained_layout=True)
        self.fig_canvas = FigureCanvas(self.fig)
        if blank:
            self.ax.set_frame_on(False)
            self.ax.axes.get_xaxis().set_visible(False)
            self.ax.axes.get_yaxis().set_visible(False)
            self.ax.axes.get_xaxis().set_major_locator(plt.NullLocator())
            self.ax.axes.get_yaxis().set_major_locator(plt.NullLocator())

        layout = qtw.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        if name:
            label = qtw.QLabel(name)
            label.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
            layout.addWidget(label)
        layout.addWidget(self.fig_canvas)
        layout.addWidget(NavigationToolbar(self.fig_canvas, self))
        self.setLayout(layout)

    def draw(self):
        self.fig_canvas.draw()


class MplImshowWidget(MPLWidget):
    def __init__(
        self,
        initial_data=None,
        blank=False,
        *args,
        **kwargs
    ):
        super().__init__(blank=blank, *args, **kwargs)
        if initial_data is None:
            initial_data = np.zeros((1, 1))
        self.plot = self.ax.imshow(initial_data, origin="lower", cmap="gray")

    def set_data(self, data, extent):
        self.plot.set_data(data)
        self.plot.set_extent(extent)
        self.plot.set_clim(np.min(data), np.max(data))
        self.draw()