#!/usr/bin/env python3
"""
Task9: wersja UI, w ktorej wczytywanie i zapis pliku odbywaja sie
asynchronicznie (w osobnym watku QThread), dzieki czemu interfejs
nie zawiesza sie podczas konwersji wiekszych plikow.

Logika konwersji jest wspoldzielona z wersja konsolowa (converter.py).
"""
import sys

from PyQt5.QtCore import QThread, pyqtSignal
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


class ConversionWorker(QThread):
    """Watek wykonujacy konwersje w tle (asynchronicznie wzgledem UI)."""

    finished_ok = pyqtSignal(str, str)   # (src_fmt, dst_fmt)
    failed = pyqtSignal(str)             # komunikat bledu

    def __init__(self, source, destination):
        super().__init__()
        self.source = source
        self.destination = destination

    def run(self):
        try:
            src_fmt, dst_fmt = converter.convert(self.source, self.destination)
        except Exception as e:
            self.failed.emit(str(e))
            return
        self.finished_ok.emit(src_fmt, dst_fmt)


class ConverterWindow(QWidget):
    FILTER = "Obslugiwane (*.json *.yml *.yaml *.xml);;Wszystkie pliki (*)"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter danych JSON / YAML / XML (asynchroniczny)")
        self.resize(560, 180)
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        src_row = QHBoxLayout()
        self.src_edit = QLineEdit()
        self.src_edit.setPlaceholderText("Plik zrodlowy...")
        src_btn = QPushButton("Wybierz...")
        src_btn.clicked.connect(self.pick_source)
        src_row.addWidget(QLabel("Zrodlo:"))
        src_row.addWidget(self.src_edit)
        src_row.addWidget(src_btn)
        layout.addLayout(src_row)

        dst_row = QHBoxLayout()
        self.dst_edit = QLineEdit()
        self.dst_edit.setPlaceholderText("Plik docelowy (z rozszerzeniem .json/.yml/.xml)...")
        dst_btn = QPushButton("Wybierz...")
        dst_btn.clicked.connect(self.pick_destination)
        dst_row.addWidget(QLabel("Cel:   "))
        dst_row.addWidget(self.dst_edit)
        dst_row.addWidget(dst_btn)
        layout.addLayout(dst_row)

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

        # Blokujemy przycisk na czas pracy watku, aby uniknac podwojnego uruchomienia.
        self.convert_btn.setEnabled(False)
        self.status.setText("Konwertowanie (w tle)...")

        self.worker = ConversionWorker(source, destination)
        self.worker.finished_ok.connect(self.on_success)
        self.worker.failed.connect(self.on_error)
        self.worker.finished.connect(lambda: self.convert_btn.setEnabled(True))
        self.worker.start()

    def on_success(self, src_fmt, dst_fmt):
        self.status.setText("OK: %s -> %s" % (src_fmt, dst_fmt))
        QMessageBox.information(self, "Sukces", "Zapisano plik:\n%s" % self.dst_edit.text())

    def on_error(self, message):
        self.status.setText("Blad.")
        QMessageBox.critical(self, "Blad konwersji", message)


def main():
    app = QApplication(sys.argv)
    window = ConverterWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
