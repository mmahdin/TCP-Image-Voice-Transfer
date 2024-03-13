import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal

# Global flag for image change
global_flag = True


class ImageThread(QThread):
    change_image_signal = Signal(np.ndarray)

    def run(self):
        global global_flag
        while True:
            if global_flag:
                # Load the new image, you can replace this with your own logic
                image = cv2.imread("imgs/no_image1.jpg")
                image = cv2.resize(image, (400, 500))
                self.change_image_signal.emit(image)
                # Reset the flag after updating the image
                global_flag = False
            else:
                pass
            # Sleep to avoid busy wait
            self.sleep(1)


class WebcamThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                self.change_pixmap_signal.emit(frame)
            else:
                pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Example")
        self.setGeometry(100, 100, 1400, 800)  # Set initial geometry

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.create_layout()
        self.webcam_thread = WebcamThread()
        self.webcam_thread.change_pixmap_signal.connect(self.update_image)
        self.webcam_thread.start()

        # Create and start the image thread
        self.image_thread = ImageThread()
        self.image_thread.change_image_signal.connect(self.update_left_image)
        self.image_thread.start()

    def create_layout(self):
        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        ################################### IP layout ###################################
        ip_widget = QWidget(self)

        ip_layout = QHBoxLayout()
        ip_layout.setObjectName("ipLayout")  # Set object name for styling

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

        ip_widget.setLayout(ip_layout)
        main_layout.addWidget(ip_widget, 1)

        ################################### Image layout ###################################
        image_widget = QWidget(self)
        left_vertical_widget = QWidget(self)
        right_vertical_widget = QWidget(self)

        image_layout = QHBoxLayout()
        image_layout.setObjectName("imageLayout")

        image_widget.setLayout(image_layout)
        main_layout.addWidget(image_widget, 10)

        left_vertical_layout = QVBoxLayout()
        right_vertical_layout = QVBoxLayout()

        # Change this to instance variable
        self.left_image_label = QLabel("Left Image")
        left_button = QPushButton("Left Button")

        self.right_top_image_label = QLabel("Right Top Image")
        right_top_button = QPushButton("Right Top Button")

        right_bottom_layout = QHBoxLayout()
        right_bottom_button1 = QPushButton("Button 1")
        right_bottom_button2 = QPushButton("Button 2")
        right_bottom_layout.addWidget(right_bottom_button1)
        right_bottom_layout.addWidget(right_bottom_button2)

        # Change this to instance variable
        left_vertical_layout.addWidget(self.left_image_label)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum,
                             QSizePolicy.Expanding)
        left_vertical_layout.addItem(spacer)
        left_vertical_layout.addWidget(left_button)

        right_vertical_layout.addWidget(self.right_top_image_label)
        right_vertical_layout.addWidget(right_top_button)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum,
                             QSizePolicy.Expanding)
        right_vertical_layout.addItem(spacer)
        right_vertical_layout.addLayout(right_bottom_layout)

        left_vertical_widget.setLayout(left_vertical_layout)
        right_vertical_widget.setLayout(right_vertical_layout)
        left_vertical_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        right_vertical_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        image_layout.addWidget(left_vertical_widget)
        image_layout.addWidget(right_vertical_widget)

        ################################### Send layout ###################################
        send_layout = QHBoxLayout()
        send_layout.setObjectName("sendLayout")
        main_layout.addLayout(send_layout, 1)

        send_button = QPushButton("Send")
        send_layout.addWidget(send_button)

    def update_image(self, cv_img):
        qt_img = QImage(
            cv_img.data, cv_img.shape[1], cv_img.shape[0], QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qt_img)
        self.right_top_image_label.setPixmap(pixmap)

    def update_left_image(self, cv_img):
        height, width, channel = cv_img.shape
        bytesPerLine = 3 * width
        qt_img = QImage(
            cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qt_img)
        self.left_image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
