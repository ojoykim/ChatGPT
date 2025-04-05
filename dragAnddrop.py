from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
import sys

class DraggableLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        drag.exec(Qt.CopyAction)

app = QApplication(sys.argv)
label = DraggableLabel("이 텍스트를 웹 브라우저로 드래그 해보세요!")
label.resize(300, 50)
label.show()
sys.exit(app.exec())
