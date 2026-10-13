"""Menu bar construction and action wiring."""

from __future__ import annotations

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMenuBar, QFileDialog


def build_menubar(window: QMainWindow) -> QMenuBar:
    bar = window.menuBar()

    file_menu = bar.addMenu("&File")
    open_action = QAction("&Open project…", window)
    open_action.setShortcut(QKeySequence.Open)
    open_action.triggered.connect(lambda: _open_project(window))
    file_menu.addAction(open_action)

    save_action = QAction("&Save project", window)
    save_action.setShortcut(QKeySequence.Save)
    file_menu.addAction(save_action)
    file_menu.addSeparator()
    file_menu.addAction(QAction("E&xit", window, triggered=window.close))

    edit_menu = bar.addMenu("&Edit")
    edit_menu.addAction(QAction("Regenerate cue", window))
    edit_menu.addAction(QAction("Split cue here", window))

    export_menu = bar.addMenu("E&xport")
    export_menu.addAction(QAction("SRT…", window))
    export_menu.addAction(QAction("VTT…", window))
    export_menu.addAction(QAction("Plain text…", window))

    return bar


def _open_project(window: QMainWindow) -> None:
    path, _ = QFileDialog.getOpenFileName(
        window, "Open project", "", "Voiceover projects (*.voscript)"
    )
    if path:
        window.statusBar().showMessage(f"Opened {path}", 4000)