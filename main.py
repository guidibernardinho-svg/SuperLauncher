import sys
import json
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QInputDialog, QLabel, QMessageBox
)
from PySide6.QtCore import Qt

SAVE_FILE = "games.json"


class SuperLauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎮 SuperLauncher")
        self.resize(900, 600)

        self.layout = QVBoxLayout()

        self.title = QLabel("🎮 SuperLauncher")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.game_list = QListWidget()

        self.add_button = QPushButton("➕ Adicionar Jogo")
        self.remove_button = QPushButton("🗑️ Remover Jogo")
        self.launch_button = QPushButton("🚀 Abrir Jogo")

        self.add_button.clicked.connect(self.add_game)
        self.remove_button.clicked.connect(self.remove_game)
        self.launch_button.clicked.connect(self.launch_game)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.game_list)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.remove_button)
        self.layout.addWidget(self.launch_button)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Arial;
            }
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #8e7dff;
            }
            QListWidget {
                background-color: #1f1f1f;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;
            }
        """)

        self.load_games()

    def load_games(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                games = json.load(f)
                for game in games:
                    self.game_list.addItem(game)

    def save_games(self):
        games = []
        for i in range(self.game_list.count()):
            games.append(self.game_list.item(i).text())

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(games, f, indent=4)

    def add_game(self):
        game_name, ok = QInputDialog.getText(self, "Adicionar Jogo", "Nome do jogo:")
        if ok and game_name:
            self.game_list.addItem(game_name)
            self.save_games()

    def remove_game(self):
        selected = self.game_list.currentRow()
        if selected >= 0:
            self.game_list.takeItem(selected)
            self.save_games()

    def launch_game(self):
        selected_item = self.game_list.currentItem()
        if selected_item:
            QMessageBox.information(
                self,
                "Abrir Jogo",
                f"Aqui você pode configurar para abrir: {selected_item.text()}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SuperLauncher()
    window.show()

    sys.exit(app.exec())
