# ui/forms/add_student_dialog.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QCheckBox, \
    QMessageBox, QCalendarWidget, QVBoxLayout
from PyQt5.QtCore import QDate
from datetime import datetime
import re


class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбрать дату")
        self.layout = QVBoxLayout()

        # Используем QCalendarWidget вместо QDateEdit
        self.calendar = QCalendarWidget()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.layout.addWidget(self.calendar)

        self.save_button = QPushButton("Выбрать")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def get_date(self):
        selected_date = self.calendar.selectedDate()
        return selected_date.toString("dd/MM/yyyy")


class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить ученика")
        self.layout = QFormLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.department_combo = QComboBox()
        self.department_combo.addItems([
            "Бокс", "Лёгкая атлетика", "Гиревой спорт", "Греко-римская борьба",
            "Дзюдо", "Самбо", "Пулевая стрельба", "Плавание", "Полиатлон", "Шахматы"
        ])
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setPlaceholderText("ДД/ММ/ГГГГ")
        self.birth_date_button = QPushButton("📅")
        self.birth_date_button.setFixedWidth(30)
        self.birth_date_button.clicked.connect(lambda: self.show_date_picker(self.birth_date_input))
        self.group_input = QLineEdit()
        self.trainer_input = QLineEdit()
        self.school_input = QLineEdit()
        self.rank_input = QLineEdit()
        self.rank_date_input = QLineEdit()
        self.rank_date_input.setPlaceholderText("ДД/ММ/ГГГГ")
        self.rank_date_button = QPushButton("📅")
        self.rank_date_button.setFixedWidth(30)
        self.rank_date_button.clicked.connect(lambda: self.show_date_picker(self.rank_date_input))
        self.snils_input = QLineEdit()
        self.snils_input.setPlaceholderText("XXX-XXX-XXX XX")
        self.passport_input = QLineEdit()
        self.enrollment_date_input = QLineEdit()
        self.enrollment_date_input.setPlaceholderText("ДД/ММ/ГГГГ")
        self.enrollment_date_button = QPushButton("📅")
        self.enrollment_date_button.setFixedWidth(30)
        self.enrollment_date_button.clicked.connect(lambda: self.show_date_picker(self.enrollment_date_input))
        self.medical_clearance_checkbox = QCheckBox("Прошёл медосмотр")

        # Добавление полей в форму
        self.layout.addRow("Имя:", self.name_input)
        self.layout.addRow("Отделение:", self.department_combo)
        birth_date_layout = QHBoxLayout()
        birth_date_layout.addWidget(self.birth_date_input)
        birth_date_layout.addWidget(self.birth_date_button)
        self.layout.addRow("Дата рождения:", birth_date_layout)
        self.layout.addRow("Группа:", self.group_input)
        self.layout.addRow("Тренер:", self.trainer_input)
        self.layout.addRow("Школа:", self.school_input)
        self.layout.addRow("Спортивный разряд:", self.rank_input)
        rank_date_layout = QHBoxLayout()
        rank_date_layout.addWidget(self.rank_date_input)
        rank_date_layout.addWidget(self.rank_date_button)
        self.layout.addRow("Дата разряда:", rank_date_layout)
        self.layout.addRow("СНИЛС:", self.snils_input)
        self.layout.addRow("Паспорт:", self.passport_input)
        enrollment_date_layout = QHBoxLayout()
        enrollment_date_layout.addWidget(self.enrollment_date_input)
        enrollment_date_layout.addWidget(self.enrollment_date_button)
        self.layout.addRow("Дата зачисления:", enrollment_date_layout)
        self.layout.addRow("Медосмотр:", self.medical_clearance_checkbox)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def show_date_picker(self, line_edit):
        dialog = DatePickerDialog(self)
        if dialog.exec_():
            selected_date = dialog.get_date()
            line_edit.setText(selected_date)
            if line_edit == self.birth_date_input:
                self.calculate_age()

    def calculate_age(self):
        birth_date_str = self.birth_date_input.text()
        if birth_date_str and re.match(r'^\d{2}/\d{2}/\d{4}$', birth_date_str):
            try:
                birth_date = datetime.strptime(birth_date_str, '%d/%m/%Y')
                today = datetime.now()
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                return str(age)
            except ValueError:
                return ""
        return ""

    def validate_snils(self, snils):
        """Проверяет контрольную сумму СНИЛС."""
        if not re.match(r'^\d{11}$', snils):
            return False
        digits = [int(d) for d in snils]
        checksum = sum(d * w for d, w in zip(digits[:9], [9, 8, 7, 6, 5, 4, 3, 2, 1]))
        checksum = checksum % 101 % 100
        return checksum == int(snils[-2:])

    def clean_snils(self, snils):
        """Очищает СНИЛС от дефисов и пробелов."""
        return ''.join(c for c in snils if c.isdigit())

    def get_data(self):
        name = self.name_input.text()
        if not re.match(r'^[А-Яа-яЁё\s-]+$', name):
            raise ValueError("Имя должно содержать только кириллицу, пробелы и дефисы")
        department = self.department_combo.currentText()
        if not department:
            raise ValueError("Отделение обязательно для выбора")

        date_pattern = r'^\d{2}/\d{2}/\d{4}$'
        current_date = datetime.now()
        dates = [
            ("Дата рождения", self.birth_date_input.text(), True),
            ("Дата разряда", self.rank_date_input.text(), False),
            ("Дата зачисления", self.enrollment_date_input.text(), True)
        ]
        for field_name, date, required in dates:
            if required and not date:
                raise ValueError(f"{field_name} обязательна")
            if date:
                if not re.match(date_pattern, date):
                    raise ValueError(f"{field_name} должна быть в формате ДД/ММ/ГГГГ")
                try:
                    parsed_date = datetime.strptime(date, '%d/%m/%Y')
                    if field_name == "Дата рождения" and parsed_date > current_date:
                        raise ValueError("Дата рождения не может быть в будущем")
                    if field_name in ["Дата разряда", "Дата зачисления"] and parsed_date > current_date:
                        raise ValueError(f"{field_name} не может быть в будущем")
                except ValueError as e:
                    if "time data" in str(e):
                        raise ValueError(f"{field_name} содержит неверную дату")
                    raise e

        snils_input = self.snils_input.text().strip()
        snils = ""
        if snils_input:
            if not re.match(r'^\d{3}-\d{3}-\d{3}\s\d{2}$', snils_input):
                raise ValueError("СНИЛС должен быть в формате XXX-XXX-XXX XX")
            snils = self.clean_snils(snils_input)
            if not self.validate_snils(snils):
                raise ValueError("СНИЛС недействителен (неверная контрольная сумма)")

        passport = self.passport_input.text()
        if passport and not re.match(r'^\d{4}\s\d{6}$', passport):
            raise ValueError("Паспортные данные должны быть в формате XXXX XXXXXX")

        medical_clearance = 1 if self.medical_clearance_checkbox.isChecked() else 0
        age = self.calculate_age()

        return (name, age, self.birth_date_input.text(),
                self.department_combo.currentText(), self.group_input.text(),
                self.trainer_input.text(), self.school_input.text(),
                self.rank_input.text(), self.rank_date_input.text(), snils,
                passport, self.enrollment_date_input.text(), medical_clearance)


class EditStudentDialog(AddStudentDialog):
    def __init__(self, student_data):
        super().__init__()
        self.setWindowTitle("Редактировать ученика")
        self.student_id = student_data[0]  # ID ученика
        self.name_input.setText(student_data[1])
        self.department_combo.setCurrentText(student_data[4])
        self.birth_date_input.setText(student_data[3])
        self.group_input.setText(student_data[5])
        self.trainer_input.setText(student_data[6])
        self.school_input.setText(student_data[7])
        self.rank_input.setText(student_data[8])
        self.rank_date_input.setText(student_data[9])
        self.snils_input.setText(student_data[10])
        self.passport_input.setText(student_data[11])
        self.enrollment_date_input.setText(student_data[12])
        self.medical_clearance_checkbox.setChecked(bool(student_data[13]))

    def get_data(self):
        data = super().get_data()
        return (self.student_id,) + data