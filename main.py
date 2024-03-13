import sys
from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Example")
        self.setGeometry(100, 100, 1000, 600)  # Set initial geometry

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.create_layout()

    def create_layout(self):
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # IP layout
        ip_layout = QHBoxLayout()
        ip_layout.setObjectName("ipLayout")  # Set object name for styling
        main_layout.addLayout(ip_layout, 1)  # Set the stretch factor to 1

        ip_entry1 = QLineEdit()
        ip_entry2 = QLineEdit()
        ip_button = QPushButton("Submit")

        # Set fixed sizes for the widgets
        ip_entry1.setFixedSize(200, 30)
        ip_entry2.setFixedSize(100, 30)
        ip_button.setFixedSize(100, 30)

        ip_layout.addWidget(ip_entry1, 4)  # Set the stretch factor to 4
        ip_layout.addWidget(ip_entry2, 1)  # Set the stretch factor to 1
        ip_layout.addWidget(ip_button, 1)   # Set the stretch factor to 1

        ip_layout.setAlignment(Qt.AlignHCenter)

        # Image layout
        image_layout = QHBoxLayout()
        # Set object name for styling
        image_layout.setObjectName("imageLayout")
        main_layout.addLayout(image_layout, 2)  # Set the stretch factor to 2

        left_vertical_layout = QVBoxLayout()
        right_vertical_layout = QVBoxLayout()

        left_image_label = QLabel("Left Image")
        left_button = QPushButton("Left Button")

        right_top_image_label = QLabel("Right Top Image")
        right_top_button = QPushButton("Right Top Button")

        right_bottom_layout = QHBoxLayout()
        right_bottom_button1 = QPushButton("Button 1")
        right_bottom_button2 = QPushButton("Button 2")
        right_bottom_layout.addWidget(right_bottom_button1)
        right_bottom_layout.addWidget(right_bottom_button2)

        left_vertical_layout.addWidget(left_image_label)
        left_vertical_layout.addWidget(left_button)

        right_vertical_layout.addWidget(right_top_image_label)
        right_vertical_layout.addWidget(right_top_button)
        right_vertical_layout.addLayout(right_bottom_layout)

        image_layout.addLayout(left_vertical_layout)
        image_layout.addLayout(right_vertical_layout)

        # Send layout
        send_layout = QHBoxLayout()
        send_layout.setObjectName("sendLayout")  # Set object name for styling
        main_layout.addLayout(send_layout, 1)  # Set the stretch factor to 1

        send_button = QPushButton("Send")
        send_layout.addWidget(send_button)

        # Apply style sheets to layouts
        self.setStyleSheet("""
        #ipLayout {
            background-color: black;
        }

        #imageLayout {
            background-color: lightgreen;
        }

        #sendLayout {
            background-color: lightyellow;
        }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
