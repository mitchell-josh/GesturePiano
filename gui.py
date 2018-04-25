import logging
import sys

from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

import capture
import piano
import ai

LOG_LEVEL = logging.DEBUG
app = QApplication(sys.argv)


class LogTextEdit(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        log_msg = self.format(record)
        self.widget.appendPlainText(log_msg)


class UpdateThread(QThread):
    signal_lbl_cam = pyqtSignal(QPixmap)
    signal_lbl_piano = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.stream = capture.VideoStream()
        self.piano = piano.Piano(4)  # 4 - number of octaves
        self.ai = ai.AI()

        self.is_pianolbl_reset = True
        self.is_running = True
        logging.debug("UpdateThread Initialized")

    def run(self):
        logging.debug("UpdateThread Running")

        while self.is_running:
            if self.stream.is_open() is False:
                # Retry
                logging.debug("Trying to open camera stream")
                self.stream = capture.VideoStream()
                continue

            # Change to stream.get_next_frame_raw() for raw Image from camera
            frame = self.stream.get_next_frame()

            # Piano demo
            note = self.ai.detect_gesture(frame)
            if self.piano.is_valid_note(note):
                self.piano.play(note)
                self.signal_lbl_piano.emit(QPixmap("res/" + note.split("-")[0].lower() + "_down.png").scaledToWidth(520))
                logging.debug("Piano label updated to res/" + note[0].lower() + "_down.png")

                self.is_pianolbl_reset = False

            # reset key label if the note is no longer being played
            if not self.is_pianolbl_reset and not self.piano.is_note_playing():
                self.signal_lbl_piano.emit(QPixmap("res/keys.png").scaledToWidth(520))
                logging.debug("Piano label reset to res/keys.png")
                self.is_pianolbl_reset = True

            # Convert image
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            image = QPixmap.fromImage(image)

            rescaled_image = image.scaled(520, 360, Qt.KeepAspectRatio)
            self.signal_lbl_cam.emit(rescaled_image)

        logging.debug("UpdateImage Thread out of loop")

    def stop(self):
        self.is_running = False
        self.stream.destroy()
        self.terminate()


class GUI(QWidget):
    def __init__(self, window_title='Virtual Piano'):
        QWidget.__init__(self)
        self.setWindowTitle(window_title)
        self.layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()

        self.lbl_image = QLabel(self)
        self.lbl_image.resize(520, 360)

        self.lbl_keys = QLabel(self)
        self.lbl_keys.setPixmap(QPixmap("res/keys.png").scaledToWidth(520))
        self.lbl_keys.resize(520, 360)

        logger = LogTextEdit(self)
        logging.getLogger().addHandler(logger)
        logger.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s", "%d/%m/%y %H:%M:%S"))
        logging.getLogger().addHandler(logger)
        logging.getLogger().setLevel(LOG_LEVEL)

        self.thread = UpdateThread(self)
        self.thread.signal_lbl_cam.connect(self.lbl_image.setPixmap)
        self.thread.signal_lbl_piano.connect(self.lbl_keys.setPixmap)
        self.thread.start()

        self.inner_layout.addWidget(self.lbl_image)
        self.inner_layout.addWidget(self.lbl_keys)

        self.layout.addLayout(self.inner_layout)
        self.layout.addWidget(logger.widget)

        self.setLayout(self.layout)

        logging.debug("GUI Initialized")

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


def main():
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
