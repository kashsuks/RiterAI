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

        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_text)
        self.sub_label_text = "Applications for the lazy"
        self.sub_label_index = 0
        self.typing_timer.start(50) 

        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(1000)  
        self.fade_in_animation.setStartValue(0)  
        self.fade_in_animation.setEndValue(1)    
        self.fade_in_animation.start()

        QTimer.singleShot(4000, self.start_fade_out)

    def type_text(self):
        if self.sub_label_index < len(self.sub_label_text):
            self.label_sub.setText(self.sub_label_text[:self.sub_label_index + 1])
            self.sub_label_index += 1
        else:
            self.typing_timer.stop()  

    def start_fade_out(self):
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(1000)  
        self.fade_out_animation.setStartValue(1)   
        self.fade_out_animation.setEndValue(0)     
        self.fade_out_animation.start()

        QTimer.singleShot(1000, self.close)  