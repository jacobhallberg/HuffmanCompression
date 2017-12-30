# Author: Jacob Hallberg
# Last Edited: 12/25/2017
from pathlib import Path
from math import log2
from encode_UI import Ui_HuffmanEncode
import huffman
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QFileDialog, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)


class Huffman_Encode(QMainWindow, Ui_HuffmanEncode):
    def __init__(self, parent=None):
        super(Huffman_Encode, self).__init__(parent)
        self.setupUi(self)

        self.original_file_size, self.encoding_size, self.lower_bound = 0, 0, 0
        self.decoded_file, self.file_name, self.encoding, self.code_book = "", "", "", ""
        self.uploaded, self.save_or, self.saveable = False, 0, 0
        self.frequency = {}

        self.UploadFile.clicked.connect(self.encode_button_clicked)
        self.DecodeFile.clicked.connect(self.decode_button_clicked)

    def decode_button_clicked(self):
        if not self.save_or:
            self.openFileNamesDialog()
        else:
            self.saveFileDialog('write_decode')

    def encode_button_clicked(self):
        if not self.saveable:
            self.openFileNameDialog()

            if self.uploaded:
                self.envoke_encode()
                self.calculate_size()
                self.translate_button()
                self.create_plot()
                self.uploaded = False
                self.saveable = True

        elif self.saveable == 1:
            self.saveFileDialog('write_binary')
            self.saveable += 1

        else:
            self.saveFileDialog('write_code_book')
            self.reset()
            # huffman.decode_file(self.code_book, self.file_name)

    def openFileNameDialog(self):
        # Settng up elements for saving.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_name, _ = QFileDialog.getOpenFileName(
            self, "Select file for encoding", "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)", options=options)

        if self.file_name:
            self.uploaded = True

    def openFileNamesDialog(self):
        if not self.save_or:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(
                self, "QFileDialog.getOpenFileNames()", "", "All Files (*);;Binary Files (*.bin)", options=options)
            if len(files) == 2:
                decoded_file = huffman.decode_file(files[1], files[0])
                self.textBrowser.setText(decoded_file)
                self.label.setText("Upload Complete")
                self.DecodeFile.setText("Click Again to Save File")
            else:
                self.DecodeFile.setText("You Must Upload Two Files")
        else:
            self.save_or = 0

    def saveFileDialog(self, operation):
        # Settng up elements for saving.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        sfile_name, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "All Files (*);;Binary Files (*.bin)", options=options)

        # Operation string determines function call.
        if sfile_name and operation == 'write_binary':
            huffman.write_binary_encoding(self.encoding, sfile_name)
            self.UploadFile.setText("Click again to save Code Book")

        elif sfile_name and operation == 'write_code_book':
            huffman.write_code_book(self.code_book, sfile_name)
            self.UploadFile.setText("Click to compress another file")
        elif sfile_name and operation == 'write_decode':
            with open(sfile_name, 'w') as decode:
                decode.write(self.decoded_file)

        self.file_name = sfile_name

    def calculate_size(self):
        file = Path(self.file_name)
        self.original_file_size = file.stat().st_size
        self.encoding_size = len(self.encoding) + 8 - (len(self.encoding) % 8)

        # Theoretical limit based on:
        #    https://en.wikipedia.org/wiki/Entropy_(information_theory)

        p_xi = lambda freq, n=self.original_file_size: freq / n

        entropy_sum = 0
        for _, value in self.frequency.items():
            entropy_sum += p_xi(value) * log2(p_xi(value))

        self.lower_bound = int(
            round(entropy_sum * -1 * self.original_file_size, 0))
        self.original_file_size = self.original_file_size * 8

        # Bit comparisons between the original file and my compression.
        # Added 7 bits to my implementation size because
        print("- Original File Size    :", self.original_file_size, "bits.")
        print("- My Implementation Size:", self.encoding_size, "bits.")
        print("- Theoretical Limit Size:", self.lower_bound, "bits.")

    def envoke_encode(self):
        # Open file using the passed in file_name.
        with open(self.file_name) as stream:
            read_file = stream.read()
        # Run the encoding functions from huffman.py.
        self.frequency = huffman.calculate_frequency(read_file)
        self.encoding, self.code_book = huffman.create_encoding(
            self.frequency, read_file)

    def translate_button(self):
        _translate = QtCore.QCoreApplication.translate
        percentage_change = 100 - \
            ((self.encoding_size / self.original_file_size) * 100)
        changed_string = "File size reducable by: " + \
            str(round(percentage_change, 0)) + "%"
        self.label_2.setText(_translate("HuffmanEncode", changed_string))
        self.UploadFile.setText(_translate(
            "HuffmanEncode", "Click Again to Save Encoding"))

    def reset(self):
        self.setupUi(self)

        self.original_file_size, self.encoding_size, self.lower_bound = 0, 0, 0
        self.file_name, self.encoding, self.code_book = "", "", ""
        self.uploaded, self.saveable = False, 0
        self.frequency = {}

        self.UploadFile.clicked.connect(self.encode_button_clicked)
        self.DecodeFile.clicked.connect(self.decode_button_clicked)

    def create_plot(self):
        size_l = [self.original_file_size,
                  self.encoding_size, self.lower_bound]
        m = PlotCanvas(self.Encode, 7, 5, 100, size_l)
        m.move(35, 15)
        m.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, hi=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(hi)

    def plot(self, size_l):
        # Increase font size beacuse of resolution.
        matplotlib.rcParams.update({'font.size': 34})
        x_data = ["Original File", "Our Implementation", "Theoretical Limit"]
        y_data = size_l

        # Create 1x1 area and plot.
        axes = self.figure.add_subplot(1, 1, 1)
        axes.bar(x_data, y_data, width=.5)
        # axes.legend(('r','g','b'), ('Original File', 'My Implementation', 'Thoeretical Limit'))
        # red_patch = mpatches.Patch(color='red', label='The red data')
        # axes.legend(handles=[red_patch])
        axes.set_ylabel("Size (bits)", fontsize=18)
        axes.set_xlabel("Compression Type", fontsize=18)
        self.draw()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    nextGui = Huffman_Encode()
    nextGui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
