# ui/forms/main_window.py
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QMessageBox, QComboBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from datetime import datetime
from database.db_manager import DatabaseManager
from utils.export import export_to_csv
from ui.forms.add_student_dialog import AddStudentDialog, EditStudentDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sport School App")
        self.setGeometry(100, 100, 800, 600)
        self.db = DatabaseManager()
        self.sort_column = None  # Текущая колонка для сортировки
        self.sort_order = Qt.AscendingOrder  # Текущий порядок сортировки
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QHBoxLayout()
        self.department_filter = QComboBox()
        self.department_filter.addItems(["Все"])
        self.department_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Отделение:"))
        filter_layout.addWidget(self.department_filter)

        self.school_filter = QComboBox()
        self.school_filter.addItems(["Все"])
        self.school_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Школа:"))
        filter_layout.addWidget(self.school_filter)

        self.rank_filter = QComboBox()
        self.rank_filter.addItems(["Все"])
        self.rank_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Разряд:"))
        filter_layout.addWidget(self.rank_filter)

        self.medical_filter = QComboBox()
        self.medical_filter.addItems(["Все", "Да", "Нет"])
        self.medical_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(QLabel("Медосмотр:"))
        filter_layout.addWidget(self.medical_filter)

        reset_filters_button = QPushButton("Сбросить фильтры")
        reset_filters_button.clicked.connect(self.reset_filters)
        filter_layout.addWidget(reset_filters_button)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "Имя", "Возраст", "Дата рождения", "Отделение", "Группа", "Тренер",
            "Школа", "Разряд", "Дата разряда", "СНИЛС", "Паспорт", "Дата зачисления", "Прошёл медосмотр"
        ])
        # Включаем сортировку через заголовки
        self.table.setSortingEnabled(False)  # Отключаем встроенную сортировку
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        layout.addWidget(self.table)

        # Кнопки для добавления, редактирования и удаления
        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить ученика")
        add_button.clicked.connect(self.add_student)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать ученика")
        edit_button.clicked.connect(self.edit_student)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить ученика")
        delete_button.clicked.connect(self.delete_student)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        export_button = QPushButton("Экспорт в CSV")
        export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Заполняем фильтры динамически
        self.update_filters()
        self.load_students()

    def update_filters(self):
        # Получаем уникальные значения для фильтров
        self.db.cursor.execute("SELECT DISTINCT department FROM students WHERE department IS NOT NULL")
        departments = [row[0] for row in self.db.cursor.fetchall()]
        self.department_filter.clear()
        self.department_filter.addItems(["Все"] + sorted(departments))

        self.db.cursor.execute("SELECT DISTINCT school FROM students WHERE school IS NOT NULL")
        schools = [row[0] for row in self.db.cursor.fetchall()]
        self.school_filter.clear()
        self.school_filter.addItems(["Все"] + sorted(schools))

        self.db.cursor.execute("SELECT DISTINCT rank FROM students WHERE rank IS NOT NULL")
        ranks = [row[0] for row in self.db.cursor.fetchall()]
        self.rank_filter.clear()
        self.rank_filter.addItems(["Все"] + sorted(ranks))

    def on_header_clicked(self, column):
        column_to_field = {
            0: "name",
            1: "age",
            2: "birth_date",
            3: "department",
            4: "group_name",
            5: "coach",
            6: "school",
            7: "rank",
            8: "rank_date",
            9: "snils",
            10: "passport",
            11: "enrollment_date",
            12: "medical_clearance"
        }
        field = column_to_field.get(column)

        if field:
            # Сбрасываем текст заголовков
            for i in range(self.table.columnCount()):
                self.table.horizontalHeaderItem(i).setText(
                    self.table.horizontalHeaderItem(i).text().replace(" ↑", "").replace(" ↓", ""))
            # Если кликнули на ту же колонку, меняем порядок сортировки
            if self.sort_column == column:
                self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
            else:
                self.sort_order = Qt.AscendingOrder
            self.sort_column = column
            # Добавляем стрелку к текущему заголовку
            header_text = self.table.horizontalHeaderItem(column).text()
            self.table.horizontalHeaderItem(column).setText(
                header_text + (" ↑" if self.sort_order == Qt.AscendingOrder else " ↓"))
            self.load_students(sort_by=field)

    def load_students(self, sort_by=None):
        self.table.setRowCount(0)
        query = "SELECT * FROM students"
        conditions = []
        params = []

        # Применение фильтров
        department = self.department_filter.currentText()
        if department != "Все":
            conditions.append("department = ?")
            params.append(department)

        school = self.school_filter.currentText()
        if school != "Все":
            conditions.append("school = ?")
            params.append(school)

        rank = self.rank_filter.currentText()
        if rank != "Все":
            conditions.append("rank = ?")
            params.append(rank)

        medical = self.medical_filter.currentText()
        if medical != "Все":
            conditions.append("medical_clearance = ?")
            params.append(1 if medical == "Да" else 0)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Применение сортировки
        if sort_by:
            order = "ASC" if self.sort_order == Qt.AscendingOrder else "DESC"
            query += f" ORDER BY {sort_by} {order}"

        self.db.cursor.execute(query, params)
        students = self.db.cursor.fetchall()

        for row, student in enumerate(students):
            self.table.insertRow(row)
            # Пропускаем первую колонку (ID), начинаем с 1
            for col, data in enumerate(student[1:], start=0):
                if col == 1 and student[3]:  # Возраст (col 1 в таблице, student[3] — дата рождения)
                    try:
                        birth_date = datetime.strptime(student[3], '%d/%m/%Y')
                        today = datetime.now()
                        age = today.year - birth_date.year
                        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                            age -= 1
                        data = str(age)
                    except ValueError:
                        data = ""
                elif col == 12:  # Медосмотр (последняя колонка в таблице)
                    data = "Да" if data else "Нет"
                self.table.setItem(row, col, QTableWidgetItem(str(data) if data is not None else ""))
            # Сохраняем ID в данных строки для использования в edit/delete
            self.table.setProperty(f"student_id_{row}", student[0])

    def apply_filters(self):
        self.load_students()

    def reset_filters(self):
        self.department_filter.setCurrentText("Все")
        self.school_filter.setCurrentText("Все")
        self.rank_filter.setCurrentText("Все")
        self.medical_filter.setCurrentText("Все")
        self.load_students()

    def add_student(self):
        dialog = AddStudentDialog()
        while True:
            if not dialog.exec_():
                break
            try:
                data = dialog.get_data()
                self.db.add_student(data)
                self.update_filters()
                self.load_students()
                break
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def edit_student(self):
        selected = self.table.currentRow()
        if selected >= 0:
            student_id = self.table.property(f"student_id_{selected}")
            if student_id is None:
                QMessageBox.warning(self, "Ошибка", "Не удалось определить ID ученика")
                return
            student_id = int(student_id)
            student_data = self.db.get_all_students()[selected]
            dialog = EditStudentDialog(student_data)
            while True:
                if not dialog.exec_():
                    break
                try:
                    data = dialog.get_data()
                    self.db.update_student(student_id, data[1:])
                    self.update_filters()
                    self.load_students()
                    break
                except ValueError as e:
                    QMessageBox.warning(self, "Ошибка", str(e))
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для редактирования")

    def delete_student(self):
        selected = self.table.currentRow()
        if selected >= 0:
            student_id = self.table.property(f"student_id_{selected}")
            if student_id is None:
                QMessageBox.warning(self, "Ошибка", "Не удалось определить ID ученика")
                return
            student_id = int(student_id)
            self.db.delete_student(student_id)
            self.update_filters()
            self.load_students()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика для удаления")

    def export_to_csv(self):
        students = self.db.get_all_students()
        export_to_csv(students)
        QMessageBox.information(self, "Успех", "Данные экспортированы в students_export.csv")