import sys
import pathlib
import numpy as np
import pyvista as pv
from PyQt5 import QtCore, QtWidgets
from plyfile import PlyData
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import QApplication, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import PCGUI


class APP(QtWidgets.QMainWindow, PCGUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(APP, self).__init__(parent)
        self.setupUi(self)

        # initial variables
        self.file_path = None  # instance variable to store file path

        # create plot widget
        self.plotter = QtInteractor(self.PlotFrame)
        self.plotter.set_background('black')
        self.plotter.resize(781, 451)
        self.PlotFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # browse button: browse file and plot it
        self.browse_button.clicked.connect(self.getfileandplot)

        # show axes button - called when button is checked/unchecked:
        self.check_showaxes.stateChanged.connect(self.checkboxstate)

        # reset view button
        self.resetview_button.clicked.connect(self.resetview)

        # combo box with different plane views
        self.planeviews_combo.currentIndexChanged.connect(self.planeviewchange)

        # Fit to Z Plane button
        self.fittoz_button.clicked.connect(self.fitplane)

    def getfileandplot(self):
        # option - change currentPath to rootPath
        file_address, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath(),
                                                                '*.ply')
        self.file_path = pathlib.PurePath(file_address)

        # keep only the name of the file, no address, and put in text box in UI
        self.filename_box.setText(self.file_path.name)

        # load plot from file:
        pd = PlyData.read(self.file_path)['vertex']
        self.cp = np.array(np.stack([pd[i] for i in ['x', 'y', 'z']], axis=-1))
        cp = self.cp
        # scalar data for colormap (using z coordinates here)
        scalar_data = cp[:, 2]

        # clear previous plot
        self.plotter.clear()

        # plot
        #scalars are data for the colormap
        self.plotter.add_mesh(cp, scalars=scalar_data, cmap='coolwarm')
        self.plotter.show()

    def checkboxstate(self):
        if self.check_showaxes.isChecked():
            self.plotter.add_axes(interactive=True)
            self.plotter.show_grid()
        else:
            # add_axes and show_grid are wrapped implementations of the show_bounds function
            self.plotter.show_bounds(show_xaxis=False, show_yaxis=False, show_zaxis=False, grid=None)

    def resetview(self):
        self.plotter.isometric_view()

    def planeviewchange(self, i):
        # When the user selects a different item, the currentIndexChanged signal
        # is emitted and the planeviewchange() method is called with the new index as the argument.
        # the changed index can be seen at: self.planeviews_combo.currentIndex()

        if self.planeviews_combo.itemText(i) == 'View XY Plane':
            self.plotter.view_xy()
        elif self.planeviews_combo.itemText(i) == 'View XZ Plane':
            self.plotter.view_xz()
        elif self.planeviews_combo.itemText(i) == 'View YX Plane':
            self.plotter.view_yx()
        elif self.planeviews_combo.itemText(i) == 'View YZ Plane':
            self.plotter.view_yz()
        elif self.planeviews_combo.itemText(i) == 'View ZX Plane':
            self.plotter.view_zx()
        elif self.planeviews_combo.itemText(i) == 'View ZY Plane':
            self.plotter.view_zy()

    def fitplane(self):
        self.plotter.clear()
        plane = pv.fit_plane_to_points(self.cp[:2])
        self.plotter.add_mesh(plane)
        self.plotter.add_points(self.cp)
        self.plotter.show()




def main():
    app = QApplication(sys.argv)
    form = APP()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
