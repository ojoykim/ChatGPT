from PySide6.QtWidgets import (
    QApplication, QTextEdit, QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QMimeData, QPoint
from PySide6.QtGui import QDrag, QPixmap, QPainter, QColor, QFont
import sys

class SmartTextEdit(QTextEdit):
    def __init__(self, default_text):
        super().__init__()
        self.setPlainText(default_text)
        self.setAcceptDrops(True)           # 브라우저 → 드롭 허용
        self.setReadOnly(False)             # 브라우저에서 텍스트 붙여넣기 허용
        self.drag_start_position = None     # 자동 드래그 감지용

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.LeftButton and
            self.drag_start_position is not None and
            (event.pos() - self.drag_start_position).manhattanLength() > QApplication.startDragDistance()
        ):
            # 드래그 시작
            mime = QMimeData()
            mime.setText(self.toPlainText())

            drag = QDrag(self)
            drag.setMimeData(mime)

            # 🎨 미리보기 아이콘 생성
            pixmap = QPixmap(200, 40)
            pixmap.fill(QColor("white"))
            painter = QPainter(pixmap)
            painter.setFont(QFont("Arial", 12))
            painter.setPen(Qt.black)
            painter.drawText(pixmap.rect(), Qt.AlignCenter, self.toPlainText()[:30] + "...")
            painter.end()

            drag.setPixmap(pixmap)
            drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))

            drag.exec(Qt.CopyAction)

        super().mouseMoveEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self.setPlainText(event.mimeData().text())  # 브라우저에서 온 텍스트 덮어쓰기
            event.acceptProposedAction()

class DragDropApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📋 텍스트 드래그 & 드롭 (브라우저 연동)")
        self.setFixedSize(500, 600)

        layout = QVBoxLayout()
        label = QLabel("🔄 텍스트창을 드래그 → 웹으로 복사\n🌐 웹에서 텍스트를 드래그 → 텍스트창에 드롭")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        default_texts = [
            "Hello from Box 1",
            "Drag this into Google Docs",
            "여기에서 웹으로 바로 드래그 해봐!",
            "브라우저에서 복사한 텍스트를 여기로 드롭해도 돼요",
            "🚀 PySide6 DnD 미리보기까지 완성!"
        ]

        for txt in default_texts:
            box = SmartTextEdit(txt)
            box.setFixedHeight(80)
            layout.addWidget(box)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropApp()
    window.show()
    sys.exit(app.exec())
