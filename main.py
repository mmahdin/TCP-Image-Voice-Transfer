import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal
from functools import partial

# Global flag for image change
global_flag = True

button_style_r = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/play2.png);
    }
    
    QPushButton:pressed {
        border-image: url(C:/Users/Mahdi/Documents/first/icon/login3p.png);
    }
"""

button_style_si = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/cap.png);
    }
    
    QPushButton:pressed {
        border-image: url(C:/Users/Mahdi/Documents/first/icon/login3p.png);
    }
"""

button_style_sv = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/mic2.png);
    }
    
    QPushButton:pressed {
        border-image: url(C:/Users/Mahdi/Documents/first/icon/login3p.png);
    }
"""

button_style_sav = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/dir.png);
    }
    
    QPushButton:pressed {
        border-image: url(C:/Users/Mahdi/Documents/first/icon/login3p.png);
    }
"""

button_style_send = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/sv2.png);
    }
    
    QPushButton:pressed {
        border-image: url(C:/Users/Mahdi/Documents/first/icon/login3p.png);
    }
"""


class ImageThread(QThread):
    change_image_signal = Signal(np.ndarray)

    def run(self):
        global global_flag
        while True:
            if global_flag:
                # Load the new image, you can replace this with your own logic
                image = cv2.imread("imgs/no_image2.jpg")
                image = cv2.resize(image, (500, 400))
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

        self.setWindowTitle("TCP connection")
        self.setWindowTitle("Fixed Size Window")
        self.setGeometry(100, 100, 1050, 670)  # Set initial geometry

        self.change_titlebar_color(QColor(100, 100, 255))

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
        ip_entry1.setPlaceholderText("IP")
        ip_entry2 = QLineEdit()
        ip_entry2.setPlaceholderText("Port")
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
        left_vertical_widget = QWidget(image_widget)
        right_vertical_widget = QWidget(image_widget)

        image_layout = QHBoxLayout()
        image_layout.setObjectName("imageLayout")

        image_widget.setLayout(image_layout)
        main_layout.addWidget(image_widget, 10)

        # Change this to instance variable
        self.left_image_label = QLabel(left_vertical_widget)
        self.left_image_label.resize(500, 400)
        # self.left_image_label.move(1, 1)

        left_button = QPushButton(left_vertical_widget)
        left_button.setStyleSheet(button_style_r)
        left_button.move(210, 410)
        left_button.resize(70, 70)

        self.right_top_image_label = QLabel(right_vertical_widget)
        self.right_top_image_label.resize(500, 400)
        # self.right_top_image_label.move(100, 1)

        right_top_button = QPushButton(right_vertical_widget)
        right_top_button.setStyleSheet(button_style_si)
        right_top_button.move(120, 410)
        right_top_button.resize(80, 80)

        right_bottom_button1 = QPushButton(right_vertical_widget)
        right_bottom_button1.setStyleSheet(button_style_sv)
        right_bottom_button1.move(220, 410)
        right_bottom_button1.resize(70, 70)

        right_bottom_button2 = QPushButton(right_vertical_widget)
        right_bottom_button2.setStyleSheet(button_style_sav)
        right_bottom_button2.move(320, 410)
        right_bottom_button2.resize(70, 70)

        image_layout.addWidget(left_vertical_widget)
        image_layout.addWidget(right_vertical_widget)

        ################################### Send layout ###################################
        send_button = QPushButton(self)
        send_button.setStyleSheet(button_style_send)
        send_button.move(500, 600)
        send_button.resize(70, 70)

    def update_image(self, cv_img):
        cv_img = cv2.resize(cv_img, (500, 400))
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
