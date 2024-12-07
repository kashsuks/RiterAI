import os
import shutil
import subprocess
import sys
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEvent, QFile
from PyQt6.QtGui import QFont, QColor, QPalette, QKeySequence, QImageReader, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QFileDialog, QTextEdit, QComboBox, QScrollArea
)

class StartupAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.setWindowOpacity(0)  

        self.label_main = QLabel("RiterI", self)
        self.label_main.setStyleSheet("color: white; font-size: 50px; font-weight: bold;")
        self.label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_sub = QLabel("", self)
        self.label_sub.setStyleSheet("color: white; font-size: 20px; font-weight: normal;")
        self.label_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label_main)
        layout.addWidget(self.label_sub)
        self.setLayout(layout)

        
        