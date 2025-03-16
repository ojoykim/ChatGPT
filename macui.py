
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy,
    QLineEdit, QPushButton, QGroupBox, QFileDialog, QProgressBar, QCalendarWidget, QDialog
)
from PySide6.QtCore import Qt, QTimer
import sys
import os

def parse_fake_hex_info(filepath):
    # 시뮬레이션된 HEX 파일 정보 추출
    return {
        "version": "1.2.3",
        "model_id": "ABC123",
        "crc": "0xDEADBEEF",
        "rom_used": 6700,
        "ram_used": 3872
    }

class CalendarPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setFixedSize(300, 250)
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)
        select_btn = QPushButton("Select Date")
        select_btn.clicked.connect(self.accept)
        layout.addWidget(select_btn)
        self.setLayout(layout)

    def get_selected_date(self):
        return self.calendar.selectedDate().toString("yyyy-MM-dd")

class CombinedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("No Types, Just Click")
        self.setFixedSize(580, 520)
        self.setStyleSheet(self.mac_style_sheet())
        self.hex_file_path = None
        self.rom_total = 256 * 1024
        self.ram_total = 64 * 1024
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # HEX 파일 선택 버튼 (상단 단독)
        file_row = QHBoxLayout()
        # self.file_input = QLineEdit()
        # self.file_input.setReadOnly(True)
        file_btn = QPushButton("📂 Select hexa file")
        file_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # file_btn.setFixedWidth(50)

        file_btn.clicked.connect(self.select_hex_file)
        # file_row.addWidget(QLabel("HEX 파일:"))
        # file_row.addWidget(self.file_input)
        file_row.addWidget(file_btn, alignment=Qt.AlignLeft)
        layout.addLayout(file_row)

        # View Info Group
        info_group = QGroupBox("📄 View Info")
        info_layout = QVBoxLayout()

        self.version_input = QLineEdit()
        self.model_input = QLineEdit()
        self.crc_input = QLineEdit()

        for label, input_field in [
            ("Version", self.version_input),
            ("Model ID", self.model_input),
            ("CRC", self.crc_input)
        ]:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFixedWidth(100)
            input_field.setReadOnly(True)
            copybtn = QPushButton("Copy")
            copybtn.clicked.connect(self.makeCopyFunc(input_field, copybtn))
            row.addWidget(lbl)
            row.addWidget(input_field)
            row.addWidget(copybtn)
            info_layout.addLayout(row)

        # Memory usage bars
        # self.rom_bar = QProgressBar()
        # self.rom_label = QLabel("ROM: 0 KB / 256 KB")
        # self.ram_bar = QProgressBar()
        # self.ram_label = QLabel("RAM: 0 KB / 64 KB")

        # info_layout.addWidget(self.rom_label)
        # info_layout.addWidget(self.rom_bar)
        # info_layout.addWidget(self.ram_label)
        # info_layout.addWidget(self.ram_bar)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # OTA 생성 그룹
        ota_group = QGroupBox("📦 Make OTN test hex")
        ota_layout = QVBoxLayout()

        date_row = QHBoxLayout()
        self.date_input = QLineEdit()
        self.date_input.setReadOnly(True)
        date_btn = QPushButton("📅 OTN Date")
        date_btn.clicked.connect(self.show_calendar)
        date_row.addWidget(QLabel("Build Date:"))
        date_row.addWidget(self.date_input)
        date_row.addWidget(date_btn)
        ota_layout.addLayout(date_row)

        generate_btn = QPushButton("📁 Make file")
        generate_btn.clicked.connect(self.generate_ota_file)
        ota_layout.addWidget(generate_btn)

        ota_group.setLayout(ota_layout)
        layout.addWidget(ota_group)

        self.setLayout(layout)

    def select_hex_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "HEX 파일 선택", "", "HEX Files (*.hex);;All Files (*)")
        if file_path:
            self.hex_file_path = file_path
            self.file_input.setText(os.path.basename(file_path))
            info = parse_fake_hex_info(file_path)
            self.version_input.setText(info["version"])
            self.model_input.setText(info["model_id"])
            self.crc_input.setText(info["crc"])
            self.animate_memory(self.rom_bar, self.rom_label, info["rom_used"], self.rom_total, "ROM")
            self.animate_memory(self.ram_bar, self.ram_label, info["ram_used"], self.ram_total, "RAM")

    def show_calendar(self):
        popup = CalendarPopup(self)
        if popup.exec():
            self.date_input.setText(popup.get_selected_date())

    def generate_ota_file(self):
        if not self.hex_file_path:
            self.show_message("⚠️ HEX 파일을 먼저 선택하세요.")
        elif not self.date_input.text():
            self.show_message("⚠️ 날짜를 먼저 선택하세요.")
        else:
            self.show_message(f"📁 OTA 파일 생성 완료: {self.date_input.text()}")

    def show_message(self, msg):
        self.toast = QLabel(msg, self)
        self.toast.setStyleSheet("""
            QLabel {
                background-color: #444;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
            }
        """)
        self.toast.adjustSize()
        self.toast.move(self.width() - self.toast.width() - 20, self.height() - 60)
        self.toast.show()
        QTimer.singleShot(1800, self.toast.hide)

    def animate_memory(self, bar, label, used, total, name):
        percent = int((used / total) * 100)
        kb_used = used // 1024
        kb_total = total // 1024
        label.setText(f"{name}: {kb_used} KB / {kb_total} KB")
        current = 0
        def step():
            nonlocal current
            if current <= percent:
                bar.setValue(current)
                current += 1
            else:
                timer.stop()
        timer = QTimer(self)
        timer.timeout.connect(step)
        timer.start(15)
    def makeCopyFunc(self, field, button):
        def copy():
            QApplication.clipboard().setText(field.text())
            # self.show_toast(f"📋 Copied!: {field.text()}")
            button.setText("✅ Copied!")
            QTimer.singleShot(1000, lambda: button.setText("Copy"))
        return copy
    def mac_style_sheet(self):
        return '''
        QWidget {
            background-color: #F7F7F7;
            font-family: 'Helvetica Neue', 'Arial';
            font-size: 14px;
        }
        QLabel {
            color: #333;
        }
        QLineEdit {
            border: 1px solid #CCC;
            border-radius: 6px;
            padding: 6px 10px;
            background: white;
        }
        QPushButton {
            background-color: #E0E0E0;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #D0D0D0;
        }
        QGroupBox {
            border: 1px solid #CCC;
            border-radius: 6px;
            margin-top: 10px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
        '''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CombinedApp()
    win.show()
    app.exec()
