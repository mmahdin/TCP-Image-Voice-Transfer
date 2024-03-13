import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Example")
        self.setGeometry(100, 100, 800, 600)  # Set initial geometry

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.create_layout()

    def create_layout(self):
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # IP layout
        ip_layout = QHBoxLayout()
        main_layout.addLayout(ip_layout)

        ip_entry1 = QLineEdit()
        ip_entry2 = QLineEdit()
        ip_button = QPushButton("Submit")
        ip_layout.addWidget(ip_entry1)
        ip_layout.addWidget(ip_entry2)
        ip_layout.addWidget(ip_button)

        # Image layout
        image_layout = QHBoxLayout()
        main_layout.addLayout(image_layout)

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
        main_layout.addLayout(send_layout)

        send_button = QPushButton("Send")
        send_layout.addWidget(send_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
