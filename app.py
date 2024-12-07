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