import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QStackedWidget, QSizePolicy, QLabel, QGraphicsDropShadowEffect,
    QDialog, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QColor, QBrush, QPalette
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import csv
import os


class StartMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        title_label = QLabel("Python")
        title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #2E86C1;")

        subtitle_label = QLabel("Searcher")
        subtitle_label.setStyleSheet("font-size: 60px; font-weight: bold; color: #3498DB;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(5, 5)

        title_label.setGraphicsEffect(shadow)

        subtitle_shadow = QGraphicsDropShadowEffect()
        subtitle_shadow.setBlurRadius(10)
        subtitle_shadow.setColor(QColor(0, 0, 0, 150))
        subtitle_shadow.setOffset(5, 5)

        subtitle_label.setGraphicsEffect(subtitle_shadow)

        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)

        start_button = QPushButton("Начать")
        start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 20px; padding: 10px;")
        start_button.clicked.connect(parent.switch_to_main_widget)

        instruction_button = QPushButton("Инструкция")
        instruction_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 20px; padding: 10px;")
        instruction_button.clicked.connect(parent.show_instruction)

        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        layout.addWidget(instruction_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)


class AddCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавить команду")

        form_layout = QFormLayout()

        self.command_name_input = QLineEdit()
        self.command_description_input = QLineEdit()

        form_layout.addRow("Команда:", self.command_name_input)
        form_layout.addRow("Описание:", self.command_description_input)

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_command)

        form_layout.addRow(add_button)
        form_layout.setAlignment(add_button, Qt.AlignCenter)

        self.setLayout(form_layout)

    def get_command_data(self):
        command_name = self.command_name_input.text()
        command_description = self.command_description_input.text()
        return command_name, command_description

    def add_command(self):
        command_name, command_description = self.get_command_data()
        if command_name and command_description:
            self.accept()
        else:
            QMessageBox.warning(self, "Предупреждение", "Заполните оба поля перед добавлением команды.")


class InstructionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        instruction_text = (
            "Добро пожаловать в приложение по поиску команд!\n\n"
            "1. Введите ключевое слово в поле ввода.\n"
            "2. Нажмите кнопку 'Начать поиск'.\n"
            "3. Результаты будут отображены в таблице ниже.\n"
            "4. Пользуйтесь удобным и эффективным поиском!"
        )

        instruction_label = QLabel(instruction_text)
        instruction_label.setStyleSheet("font-size: 18px; color: #2C3E50; font-weight: bold; margin-bottom: 20px;")

        back_button = QPushButton("Назад")
        back_button.setStyleSheet("background-color: #3498DB; color: white; font-size: 20px; padding: 10px;")

        back_button.clicked.connect(parent.switch_to_start_menu)

        self.setStyleSheet(
            "QWidget { background-color: #ECF0F1; border: 2px solid #BDC3C7; border-radius: 10px; padding: 20px; }")

        layout.addWidget(instruction_label, alignment=Qt.AlignCenter)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)


class CommandsSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.commands_data = self.load_data()

        self.stacked_widget = QStackedWidget()

        self.start_menu_widget = StartMenuWidget(self)
        self.instruction_widget = InstructionWidget(self)
        self.main_widget = QWidget()

        self.stacked_widget.addWidget(self.start_menu_widget)
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.instruction_widget)

        self.create_main_widget()

        self.button_click_player = QMediaPlayer()

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)
        self.setWindowTitle("Commands Search App")
        self.setGeometry(100, 100, 800, 600)

    def load_data(self):
        data = []
        with open('final.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def create_main_widget(self):
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("font-size: 18px; padding: 10px;")
        self.start_search_button = QPushButton("Начать поиск")
        self.start_search_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;")
        self.start_search_button.clicked.connect(self.perform_search)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Команда", "Описание"])
        self.result_table.setStyleSheet(
            "font-size: 16px; background-color: #f0f0f0; border: 1px solid #ccc; margin-bottom: 1px;")
        self.result_table.setColumnWidth(0, 200)

        header = self.result_table.horizontalHeader()
        for i in range(self.result_table.columnCount()):
            header_item = self.result_table.horizontalHeaderItem(i)
            header_item.setForeground(QBrush(QColor('#000000')))

        self.result_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setShowGrid(False)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.result_table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        for row in range(self.result_table.rowCount()):
            for col in range(self.result_table.columnCount()):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.result_table.setItem(row, col, item)

        add_command_button = QPushButton("Добавить команду")
        add_command_button.setStyleSheet(
            "background-color: #3498DB; color: white; font-size: 16px; padding: 10px;")

        return_to_menu_button = QPushButton("Вернуться в главное меню")
        return_to_menu_button.setStyleSheet(
            "background-color: #3498DB; color: white; font-size: 16px; padding: 10px;")

        add_command_button.clicked.connect(self.show_add_command_dialog)
        return_to_menu_button.clicked.connect(self.switch_to_start_menu)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_command_button)
        button_layout.addWidget(return_to_menu_button)

        layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.start_search_button)
        layout.addLayout(search_layout)
        layout.addWidget(self.result_table)
        layout.addLayout(button_layout)

        self.main_widget.setLayout(layout)

    def switch_to_main_widget(self):
        self.stacked_widget.setCurrentIndex(1)
        self.play_button_click_sound()

    def show_instruction(self):
        self.stacked_widget.setCurrentIndex(2)
        self.play_button_click_sound()

    def switch_to_start_menu(self):
        self.stacked_widget.setCurrentIndex(0)
        self.play_button_click_sound()

    def show_add_command_dialog(self):
        try:
            dialog = AddCommandDialog(self)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                command_name, command_description = dialog.get_command_data()
                self.add_command_to_database(command_name, command_description)
                self.update_table_view()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def add_command_to_database(self, command_name, command_description):
        new_command = {"Command": command_name, "Description": command_description}
        self.commands_data.append(new_command)
        self.save_data()

    def save_data(self):
        with open('final.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Command", "Description"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csvfile.seek(0, os.SEEK_END)
            if csvfile.tell() == 0:
                writer.writeheader()

            for row in self.commands_data:
                filtered_row = {key: row[key] for key in fieldnames if key in row}
                writer.writerow(filtered_row)

    def update_table_view(self):
        self.display_results(self.commands_data)

    def perform_search(self):
        search_text = self.search_input.text().lower()
        if search_text:
            exact_match_rows = self.find_exact_match_rows(search_text)
            self.result_table.setRowCount(0)
            self.display_results(exact_match_rows)
        else:
            self.result_table.setRowCount(0)

    def find_exact_match_rows(self, search_text):
        exact_match_rows = []
        for row in self.commands_data:
            if search_text in row["Command"].lower() or search_text in row["Description"].lower():
                exact_match_rows.append(row)
        return exact_match_rows

    def display_results(self, results):
        self.result_table.setRowCount(len(results))
        for i, row_data in enumerate(results):
            command_item = self.result_table.item(i, 0)
            description_item = self.result_table.item(i, 1)

            if not command_item:
                command_item = QTableWidgetItem(row_data.get("Command", ""))
                command_item.setFlags(command_item.flags() & ~Qt.ItemIsEditable)
                self.result_table.setItem(i, 0, command_item)

            if not description_item:
                description_item = QTableWidgetItem(row_data.get("Description", ""))
                description_item.setFlags(description_item.flags() & ~Qt.ItemIsEditable)
                self.result_table.setItem(i, 1, description_item)

    def play_button_click_sound(self):
        sound_url = QUrl.fromLocalFile('sound.mp3')
        media_content = QMediaContent(sound_url)
        self.button_click_player.setMedia(media_content)
        self.button_click_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    ex = CommandsSearchApp()
    ex.show()
    sys.exit(app.exec_())
