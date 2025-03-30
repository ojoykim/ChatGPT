from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt
import sys

class UpdatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("업데이트 중")
        self.setFixedSize(300, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        label = QLabel("🔄 업데이트 중입니다...", self)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, 300, 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdatingWindow()
    window.show()
    sys.exit(app.exec())
