#!/usr/bin/python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app_layout import input_layout
import sys

class Window(QWidget):
        def __init__(self):
                super().__init__()
                self.setWindowTitle("betelnut")

                # set default geometry.
                self.setGeometry(0, 0, 502, 375)

                # define the grid layout
                self.vbox = QVBoxLayout()
                self.input_grid = QGridLayout()
                self.setLayout(self.vbox)
                qtRectangle = self.frameGeometry()
                centerPoint = QDesktopWidget().availableGeometry().center()
                qtRectangle.moveCenter(centerPoint)
                self.move(qtRectangle.topLeft())

                self.inputs = {} # dict

                # storage
                self.line2auto = 0
                self.ans = 0


                # output
                self.line1txt = ""
                self.line2txt = "0"

                self.line1 = QLineEdit(self)
                self.line1.setText("")
                self.line1.setMinimumSize(0, 40)
                self.line1.setReadOnly(True)
                self.line1.setAlignment(Qt.AlignRight)
                self.vbox.addWidget(self.line1)

                self.line2 = QLineEdit(self)
                self.line2.setText(self.line2txt)
                self.line2.setMinimumSize(0, 40)
                self.line2.setReadOnly(True)
                self.line2.setAlignment(Qt.AlignRight)
                self.vbox.addWidget(self.line2)
                self.vbox.addStretch()


                # inputs
                self.vbox.addLayout(self.input_grid)
                input_layout(self)

                self.vbox.addStretch()
                self.show()

        def add_input_button(self, text, pos, size, callback=None):

                button = QPushButton()
                Text = QTextDocument()
                Text.setHtml(text);
                pixmap = QPixmap(int(Text.size().width()), int(Text.size().height()))
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                Text.drawContents(painter)
                painter.end()
                buttonicon = QIcon(pixmap)
                button.setIcon(buttonicon)
                button.setIconSize(pixmap.rect().size())
                self.input_grid.addWidget(button, *pos, *size)
                self.inputs[text]  = button

                if callback is not None:
                    button.clicked.connect(callback)

        def setLine1(self, text):
            self.line1.setText(text)

        def setLine2(self, text):
            self.line2.setText(text)




# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
