from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QLineEdit, QComboBox, QCheckBox,
                             QPushButton, QDateEdit, QSpinBox)
from PyQt5.QtCore import Qt, QDate


class StudentFilterForm(QDialog):
    def __init__(self, parent=None, department_manager=None, group_manager=None, coach_manager=None):
        super().__init__(parent)
        self.department_manager = department_manager
        self.group_manager = group_manager
        self.coach_manager = coach_manager

        self.setWindowTitle("Фильтрация учеников")
        self.resize(500, 400)

        self.init_ui()

    def init_ui(self):
        # Главный лейаут
        main_layout = QVBoxLayout()

        # Форма с полями фильтрации
        form_layout = QFormLayout()

        # Текстовый поиск
        self.search_text = QLineEdit()
        form_layout.addRow("Поиск по имени/фамилии:", self.search_text)

        # Год рождения
        self.birth_year = QSpinBox()
        self.birth_year.setMinimum(1990)
        self.birth_year.setMaximum(2020)
        self.birth_year.setSpecialValueText(" ")  # Пустое значение
        self.birth_year.setValue(
            self.birth_year.minimum() - 1)  # Устанавливаем значение меньше минимума для "пустого" значения
        form_layout.addRow("Год рождения:", self.birth_year)

        # Отделение
        self.department_combo = QComboBox()
        self.department_combo.addItem("Все отделения", None)
        if self.department_manager:
            departments = self.department_manager.get_all_departments()
            for department in departments:
                self.department_combo.addItem(department['name'], department['id'])
        form_layout.addRow("Отделение:", self.department_combo)

        # Группа
        self.group_combo = QComboBox()
        self.group_combo.addItem("Все группы", None)
        if self.group_manager:
            groups = self.group_manager.get_all_groups()
            for group in groups:
                self.group_combo.addItem(group['name'], group['id'])
        form_layout.addRow("Группа:", self.group_combo)

        # Тренер
        self.coach_combo = QComboBox()
        self.coach_combo.addItem("Все тренеры", None)
        if self.coach_manager:
            coaches = self.coach_manager.get_all_coaches()
            for coach in coaches:
                coach_name = f"{coach['last_name']} {coach['first_name']}"
                self.coach_combo.addItem(coach_name, coach['id'])
        form_layout.addRow("Тренер:", self.coach_combo)

        # Дата медосмотра (от)
        self.medical_date_from = QDateEdit()
        self.medical_date_from.setCalendarPopup(True)
        self.medical_date_from.setDate(QDate.currentDate().addYears(-1))
        self.medical_date_from.setDisplayFormat("dd.MM.yyyy")
        self.medical_date_checkbox_from = QCheckBox("Учитывать")
        self.medical_date_checkbox_from.setChecked(False)

        date_from_layout = QHBoxLayout()
        date_from_layout.addWidget(self.medical_date_from)
        date_from_layout.addWidget(self.medical_date_checkbox_from)

        form_layout.addRow("Дата медосмотра от:", date_from_layout)

        # Дата медосмотра (до)
        self.medical_date_to = QDateEdit()
        self.medical_date_to.setCalendarPopup(True)
        self.medical_date_to.setDate(QDate.currentDate())
        self.medical_date_to.setDisplayFormat("dd.MM.yyyy")
        self.medical_date_checkbox_to = QCheckBox("Учитывать")
        self.medical_date_checkbox_to.setChecked(False)

        date_to_layout = QHBoxLayout()
        date_to_layout.addWidget(self.medical_date_to)
        date_to_layout.addWidget(self.medical_date_checkbox_to)

        form_layout.addRow("Дата медосмотра до:", date_to_layout)

        # Допуск к тренировкам
        self.training_allowed_combo = QComboBox()
        self.training_allowed_combo.addItem("Все", None)
        self.training_allowed_combo.addItem("Допущены", True)
        self.training_allowed_combo.addItem("Не допущены", False)
        form_layout.addRow("Допуск к тренировкам:", self.training_allowed_combo)

        # Добавляем форму в главный лейаут
        main_layout.addLayout(form_layout)

        # Кнопки
        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.accept)

        self.reset_button = QPushButton("Сбросить")
        self.reset_button.clicked.connect(self.reset_filters)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.apply_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def reset_filters(self):
        self.search_text.setText("")
        self.birth_year.setValue(self.birth_year.minimum() - 1)
        self.department_combo.setCurrentIndex(0)
        self.group_combo.setCurrentIndex(0)
        self.coach_combo.setCurrentIndex(0)
        self.medical_date_checkbox_from.setChecked(False)
        self.medical_date_checkbox_to.setChecked(False)
        self.training_allowed_combo.setCurrentIndex(0)

    def get_filters(self):
        """Возвращает словарь с параметрами фильтрации"""
        filters = {}

        # Текстовый поиск
        if self.search_text.text():
            filters['search_text'] = self.search_text.text()

        # Год рождения
        if self.birth_year.value() >= self.birth_year.minimum():
            filters['birth_year'] = self.birth_year.value()

        # Отделение
        if self.department_combo.currentData():
            filters['department_id'] = self.department_combo.currentData()

        # Группа
        if self.group_combo.currentData():
            filters['group_id'] = self.group_combo.currentData()

        # Тренер
        if self.coach_combo.currentData():
            filters['coach_id'] = self.coach_combo.currentData()

        # Дата медосмотра (от)
        if self.medical_date_checkbox_from.isChecked():
            filters['medical_date_from'] = self.medical_date_from.date().toString("yyyy-MM-dd")

        # Дата медосмотра (до)
        if self.medical_date_checkbox_to.isChecked():
            filters['medical_date_to'] = self.medical_date_to.date().toString("yyyy-MM-dd")

        # Допуск к тренировкам
        if self.training_allowed_combo.currentData() is not None:
            filters['training_allowed'] = self.training_allowed_combo.currentData()

        return filters