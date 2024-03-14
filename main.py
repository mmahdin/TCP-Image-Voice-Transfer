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
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/play2b.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/play2b2.png);
    }
"""

button_style_si = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/capb.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/capb2.png);
    }
"""

button_style_sv = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/mic2b2.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/mic2b.png);
    }
"""

button_style_sav = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/dirb.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/dirb2.png);
    }
"""

button_style_send = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        min-width: 50px;
        font-size: 24px;
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/sv7.png);
    }
    
    QPushButton:pressed {
        border-image: url(/home/mahdi/Documents/term7/multiMedia/prj1/env/imgs/sv7b.png);
    }
"""

button_style_sub = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 10px;
        font-size: 16px;
        border-radius: 10px;
        color: #2eff04;
        border: 1px solid #2eff04;
    }
    
    QPushButton:pressed {
        border-radius: 12px;
        color: #fffd0a;
        border: 1px solid #fffd0a;
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

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet("background-color: #000100;")

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
        # ip_widget.setStyleSheet("background-color: #140032;")

        ip_layout = QHBoxLayout()
        ip_layout.setObjectName("ipLayout")  # Set object name for styling

        desc = QLabel("IP : Port")
        desc.setStyleSheet(
            "color: #e500e8 ;background-color: None;font-size:25px; font-family:Comic Sans MS;")

        ip_entry1 = QLineEdit()
        ip_entry1.setPlaceholderText("  IP")
        ip_entry1.setStyleSheet(
            "color: white; background-color: black; border: 1px solid #ed1ee7; border-radius: 10px;")

        ip_entry2 = QLineEdit()
        ip_entry2.setStyleSheet(
            "color: white; background-color: black; border: 1px solid #ed1ee7; border-radius: 10px;")
        ip_entry2.setPlaceholderText("  Port")

        ip_button = QPushButton("Connect")
        ip_button.setStyleSheet(button_style_sub)
        ip_button.clicked.connect(self.connect)

        # Set fixed sizes for the widgets
        desc.setFixedSize(80, 30)
        ip_entry1.setFixedSize(150, 30)
        ip_entry2.setFixedSize(70, 30)
        ip_button.setFixedSize(100, 30)

        ip_layout.addWidget(desc, 1)
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
        left_button.clicked.connect(self.play_voice)

        self.right_top_image_label = QLabel(right_vertical_widget)
        self.right_top_image_label.resize(500, 400)
        # self.right_top_image_label.move(100, 1)

        right_top_button = QPushButton(right_vertical_widget)
        right_top_button.setStyleSheet(button_style_si)
        right_top_button.move(120, 410)
        right_top_button.resize(80, 80)
        right_top_button.clicked.connect(self.capture_image)

        right_bottom_button1 = QPushButton(right_vertical_widget)
        right_bottom_button1.setStyleSheet(button_style_sv)
        right_bottom_button1.move(220, 410)
        right_bottom_button1.resize(70, 70)
        right_bottom_button1.clicked.connect(self.record_voice)

        right_bottom_button2 = QPushButton(right_vertical_widget)
        right_bottom_button2.setStyleSheet(button_style_sav)
        right_bottom_button2.move(320, 410)
        right_bottom_button2.resize(70, 70)
        right_bottom_button2.clicked.connect(self.choose_voice_path)

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

    def connect(self):
        pass

    def play_voice(self):
        pass

    def capture_image(self):
        pass

    def record_voice(self):
        pass

    def choose_voice_path(sefl):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
