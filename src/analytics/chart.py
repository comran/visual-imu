from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class Chart:
    def __init__(self, title):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title=title)
        self.rt_plot = self.win.addPlot(title="Realtime plot")
        self.rt_plot.addLegend()

        self.curves = list()
        self.plot_data = list()

        self.window_width = 500
        self.ptr = -self.window_width
        self.colors = list()
        self.colors.append((255, 0, 0))
        self.colors.append((255, 125, 0))
        self.colors.append((255, 255, 0))
        self.colors.append((125, 255, 0))
        self.colors.append((0, 255, 0))
        self.colors.append((0, 255, 125))
        self.colors.append((0, 255, 255))
        self.colors.append((0, 125, 255))
        self.colors.append((0, 0, 255))
        self.colors.append((125, 0, 255))
        self.colors.append((255, 0, 255))
        self.colors.append((255, 0, 125))

        self.first_print = True

    def write(self, keys, keys_to_values):
        self.ptr += 1

        if self.first_print:
            i = 0
            for key in keys:
                color_index = i % len(self.colors)
                self.curves.append(self.rt_plot.plot(
                    name=key,
                    pen=pg.mkPen(color=self.colors[color_index], width=1)))
                self.plot_data.append(np.linspace(0, 0, self.window_width))
                i += 1

        i = 0
        for component in self.plot_data:
            signal = keys_to_values[keys[i]]
            component[:-1] = component[1:]
            component[-1] = float(signal)
            self.curves[i].setData(component)
            self.curves[i].setPos(self.ptr, 0)
            i = i + 1

        QtGui.QApplication.processEvents()

        self.first_print = False
