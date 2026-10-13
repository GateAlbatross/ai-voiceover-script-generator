"""Main Qt window. Wires menus, panels, and the generation worker."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from ai_voiceover.config.constants import APP_NAME, ORG_NAME
from ai_voiceover.handlers.generation_worker import GenerationWorker
from ai_voiceover.handlers.menu_actions import build_menubar
from ai_voiceover.handlers.panels.brief_panel import BriefPanel
from ai_voiceover.handlers.panels.script_panel import ScriptPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1180, 760)

        self.brief_panel = BriefPanel()
        self.script_panel = ScriptPanel()
        self._worker: GenerationWorker | None = None

        tabs = QTabWidget()
        tabs.addTab(self.brief_panel, "Brief")
        tabs.addTab(self.script_panel, "Script")
        self.setCentralWidget(tabs)

        self.setMenuBar(build_menubar(self))
        self.brief_panel.generate_requested.connect(self._on_generate)

    def _on_generate(self, brief: dict) -> None:
        self._worker = GenerationWorker(brief)
        self._worker.finished_ok.connect(self.script_panel.load_script)
        self._worker.failed.connect(self.script_panel.show_error)
        self._worker.start()


def launch(argv: list[str]) -> int:
    app = QApplication(argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORG_NAME)
    window = MainWindow()
    window.show()
    return app.exec()