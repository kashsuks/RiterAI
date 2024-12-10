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

        self.label_main = QLabel("RiterAI", self)
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

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: white;")
        
        # Header
        self.header = QLabel("RiterAI")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.subheader = QLabel("Applications for the lazy")
        self.subheader.setStyleSheet("font-size: 14px; font-style: italic; color: #bbbbbb;")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(self.header)
        header_layout.addWidget(self.subheader)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Upload Documents Section
        doc_section = QVBoxLayout()
        doc_title = QLabel("Provide Relevant Documents (max 4)")
        doc_title.setStyleSheet("font-size: 18px;")

        self.file_preview = QLabel()
        self.file_preview.setFixedSize(150, 150)
        self.file_preview.setStyleSheet(
            "background-color: #333333; border-radius: 10px; border: 1px dashed #444444;"
        )
        self.file_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_preview.setText("No File Selected")

        self.doc_button = QPushButton("Choose File")
        self.doc_button.setStyleSheet(
            "background-color: #1e90ff; color: white; border-radius: 10px; padding: 10px;"
        )
        self.doc_button.clicked.connect(self.load_file_preview)

        self.doc_error_label = QLabel("")
        self.doc_error_label.setStyleSheet("color: red; font-size: 12px;")

        doc_section.addWidget(doc_title)
        doc_section.addWidget(self.file_preview, alignment=Qt.AlignmentFlag.AlignLeft)
        doc_section.addWidget(self.doc_button, alignment=Qt.AlignmentFlag.AlignLeft)
        doc_section.addWidget(self.doc_error_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Provide Questions Section
        question_section = QVBoxLayout()
        question_title = QLabel("Provide Questions")
        question_title.setStyleSheet("font-size: 18px;")

        self.question_text_box = QTextEdit()
        self.question_text_box.setPlaceholderText("Enter each question on a new line")
        self.question_text_box.setFixedHeight(90)
        self.question_text_box.setStyleSheet(
            "background-color: #333333; color: white; border-radius: 10px; padding: 5px; "
        )
        self.question_text_box.textChanged.connect(self.adjust_question_box_height)

        self.question_error_label = QLabel("")
        self.question_error_label.setStyleSheet("color: red; font-size: 12px;")
        
        question_section.addWidget(question_title)
        question_section.addWidget(self.question_text_box)
        question_section.addWidget(self.question_error_label)

        # Style Section
        style_section = QVBoxLayout()
        style_title = QLabel("Style (optional)")
        style_title.setStyleSheet("font-size: 18px;")

        self.style_dropdown = QComboBox()
        self.style_dropdown.addItems(["Formal", "Casual"])
        self.style_dropdown.setStyleSheet(
            "background-color: #333333; color: white; border: none; padding: 5px; border-radius: 10px;"
        )

        style_note = QLabel("Choose how you want the response to sound.")
        style_note.setStyleSheet("font-size: 12px; color: #bbbbbb;")

        style_section.addWidget(style_title)
        style_section.addWidget(self.style_dropdown)
        style_section.addWidget(style_note)

        # Footer
        next_button = QPushButton("Next")
        next_button.setStyleSheet(
            "background-color: #1e90ff; color: white; font-size: 16px; padding: 10px; border-radius: 10px;"
        )
        next_button.setFixedSize(100, 40)
        next_button.clicked.connect(self.on_next_button_click)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(next_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(doc_section)
        main_layout.addSpacing(20)
        main_layout.addLayout(question_section)
        main_layout.addSpacing(20)
        main_layout.addLayout(style_section)
        main_layout.addStretch()
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

        self.style = "Formal"   #default

    def load_file_preview(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose File")
        if file_name:
            image_reader = QImageReader(file_name)
            pixmap = QPixmap.fromImageReader(image_reader)
            scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.file_preview.setPixmap(scaled_pixmap)
            self.upload_file(file_name)  
        else:
            self.file_preview.setText("No File Selected")

    def upload_file(self, file_path):
        os.makedirs('user_files', exist_ok=True)

        file_name = os.path.basename(file_path)
        destination = os.path.join('user_files', file_name)

        shutil.copy(file_path, destination)  

    def adjust_question_box_height(self):
        document = self.question_text_box.document()
        line_count = document.blockCount()
        self.question_text_box.setFixedHeight(min(90 + (line_count - 3) * 20, 300))

    def on_next_button_click(self):
        is_valid = True
        
        if not self.file_preview.pixmap():
            self.doc_error_label.setText("This field must be completed.")
            is_valid = False
        else:
            self.doc_error_label.clear()

        questions = self.question_text_box.toPlainText().strip()
        if not questions:
            self.question_error_label.setText("This field must be completed.")
            is_valid = False
        else:
            self.question_error_label.clear()

        self.style = self.style_dropdown.currentText() if self.style_dropdown.currentText() else "Formal"

        if is_valid:
            uploaded_files = [os.path.join('user_files', f) for f in os.listdir('user_files')]
            data = {
                "uploaded_files": uploaded_files,
                "questions": questions,
                "style": self.style
            }
            subprocess.run(["python", "extract.py"], input=str(data), text=True)
        else:
            print("Please complete all fields.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RiterAI")
        self.showFullScreen()

        self.startup = StartupAnimation()
        self.startup.setFixedSize(self.size())
        
        self.home_page = HomePage()
        self.setCentralWidget(self.startup)
        QTimer.singleShot(2000, self.show_home)

    def show_home(self):
        self.setCentralWidget(self.home_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(36, 36, 36))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(36, 36, 36))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)

    app.setPalette(dark_palette)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

#TO-DO:
"""
Make the UI look better 
"""