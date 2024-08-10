#FUNCIONES DE COLOR
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class ColorManager(QObject):
    def __init__(self, widget, theme_button, modo_claro_icon_path, modo_oscuro_icon_path):
        super().__init__()
        self.widget = widget
        self.theme_button = theme_button
        self.modo_claro_icon_path = modo_claro_icon_path
        self.modo_oscuro_icon_path = modo_oscuro_icon_path
        self.dark_mode = False

    def apply_styles(self):
        if self.dark_mode:
            style_sheet = """
                QMainWindow {
                    background-color: #1d1d1d;
                }
                QToolTip {
                    background-color: #1d1d1d;
                    color: #000000;
                    padding: 5px;
                    border-radius: 30px;
                }
                QWidget {
                    background-color: #131313;
                    filter: drop-shadow(1 1 1.75rem white);
                    color:  #ffffff;
                }
                QWidget:hover {
                    border: 1px solid #e70000;
                }
                QPushButton {
                    background-color:  #ffffff;
                    color: #ffffff;
                    padding: 5px;
                    border-radius: 5px;
                    min-width: 10px;
                    min-height: 10px;
                }
                QPushButton:hover {
                    background-color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #ffffff;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ffffff;
                    border-radius: 5px;
                    color: #ffffff;
                    background-color: #242424;
                }
                QWidget#title_bar {
                    background-color: #131313;
                }
            """
            self.theme_button.setIcon(QIcon(self.modo_claro_icon_path))
        else:   #claro
            style_sheet = """
                QMainWindow {
                    background-color: #000;
                }
                QToolTip {
                    background-color: white;
                    color: black;
                    border: 1px solid black;
                }
                QWidget {
                    background-color: #fff;
                    color: #000;
                }             
                QPushButton {
                    background-color: white;
                    color: #000;
                    border: 1px solid #ccc;
                    padding: 5px;
                    border-radius: 5px;
                    min-width: 10px;
                    min-height: 10px;
                }
                QPushButton:hover {
                    background-color: #fcbe86;
                    color: #ffffff;
                }
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    color: #000;
                    background-color: #fff;
                }
                QWidget#title_bar {
                    background-color: #fff;
                }
            """
            self.theme_button.setIcon(QIcon(self.modo_oscuro_icon_path))
        self.widget.setStyleSheet(style_sheet)
        return style_sheet

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_styles()