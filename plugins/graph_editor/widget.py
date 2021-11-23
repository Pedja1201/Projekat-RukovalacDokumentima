import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar

from .canvas import MplCanvas
import pandas as pd



class GraphWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        # Create our pandas DataFrame with some simple
        # data and headers.
        df = pd.DataFrame([
           [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        ], columns=['A', 'B'])

        # plot the pandas DataFrame, passing in the
        # matplotlib Canvas axes.
        df.plot(ax=sc.axes)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
