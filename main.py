import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Simple GUI")

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create components
        ip_label = QLabel("IP:")
        ip_input = QLineEdit()
        image_label = QLabel("Image Placeholder")
        send_button = QPushButton("Send")

        # Add components to the layout
        layout.addWidget(ip_label)
        layout.addWidget(ip_input)
        layout.addWidget(image_label)
        layout.addWidget(send_button)

        # Set the layout for the window
        self.setLayout(layout)


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    # Create and show the window
    window = MyWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec())
