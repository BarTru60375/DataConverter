#!/usr/bin/env python3
"""
Task8: wersja programu z interfejsem graficznym (PyQt5).

UI pozwala wybrac plik zrodlowy i docelowy oraz wykonac konwersje.
Logika konwersji jest wspoldzielona z wersja konsolowa (converter.py).
"""
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

import converter


class ConverterWindow(QWidget):
    FILTER = "Obslugiwane (*.json *.yml *.yaml *.xml);;Wszystkie pliki (*)"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter danych JSON / YAML / XML")
        self.resize(560, 180)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Wiersz: plik zrodlowy
        src_row = QHBoxLayout()
        self.src_edit = QLineEdit()
        self.src_edit.setPlaceholderText("Plik zrodlowy...")
        src_btn = QPushButton("Wybierz...")
        src_btn.clicked.connect(self.pick_source)
        src_row.addWidget(QLabel("Zrodlo:"))
        src_row.addWidget(self.src_edit)
        src_row.addWidget(src_btn)
        layout.addLayout(src_row)

        # Wiersz: plik docelowy
        dst_row = QHBoxLayout()
        self.dst_edit = QLineEdit()
        self.dst_edit.setPlaceholderText("Plik docelowy (z rozszerzeniem .json/.yml/.xml)...")
        dst_btn = QPushButton("Wybierz...")
        dst_btn.clicked.connect(self.pick_destination)
        dst_row.addWidget(QLabel("Cel:   "))
        dst_row.addWidget(self.dst_edit)
        dst_row.addWidget(dst_btn)
        layout.addLayout(dst_row)

        # Przycisk konwersji + status
        self.convert_btn = QPushButton("Konwertuj")
        self.convert_btn.clicked.connect(self.run_conversion)
        layout.addWidget(self.convert_btn)

        self.status = QLabel("Gotowy.")
        layout.addWidget(self.status)

    def pick_source(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik zrodlowy", "", self.FILTER)
        if path:
            self.src_edit.setText(path)

    def pick_destination(self):
        path, _ = QFileDialog.getSaveFileName(self, "Wybierz plik docelowy", "", self.FILTER)
        if path:
            self.dst_edit.setText(path)

    def run_conversion(self):
        source = self.src_edit.text().strip()
        destination = self.dst_edit.text().strip()
        if not source or not destination:
            QMessageBox.warning(self, "Brak danych", "Podaj plik zrodlowy i docelowy.")
            return
        self.status.setText("Konwertowanie...")
        try:
            src_fmt, dst_fmt = converter.convert(source, destination)
        except Exception as e:
            self.status.setText("Blad.")
            QMessageBox.critical(self, "Blad konwersji", str(e))
            return
        self.status.setText("OK: %s -> %s" % (src_fmt, dst_fmt))
        QMessageBox.information(self, "Sukces", "Zapisano plik:\n%s" % destination)


def main():
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
