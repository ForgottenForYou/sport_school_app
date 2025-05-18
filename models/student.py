from PyQt5.QtCore import QDate
from datetime import datetime


class Student:
    """Модель ученика"""

    def __init__(self, id=None, first_name="", last_name="", middle_name="",
                 birth_date=None, group_id=None, coach_id=None,
                 educational_institution="", sports_rank="",
                 rank_assignment_date=None, snils="", passport_data="",
                 enrollment_date=None):
        """Инициализация объекта ученика

        Args:
            id (int, optional): ID ученика. Defaults to None.
            first_name (str, optional): Имя. Defaults to "".
            last_name (str, optional): Фамилия. Defaults to "".
            middle_name (str, optional): Отчество. Defaults to "".
            birth_date (datetime.date, optional): Дата рождения. Defaults to None.
            group_id (int, optional): ID группы. Defaults to None.
            coach_id (int, optional): ID тренера. Defaults to None.
            educational_institution (str, optional): Образовательное учреждение. Defaults to "".
            sports_rank (str, optional): Спортивный разряд. Defaults to "".
            rank_assignment_date (datetime.date, optional): Дата присвоения разряда. Defaults to None.
            snils (str, optional): СНИЛС. Defaults to "".
            passport_data (str, optional): Паспортные данные. Defaults to "".
            enrollment_date (datetime.date, optional): Дата зачисления. Defaults to None.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = birth_date if birth_date else datetime.now().date()
        self.group_id = group_id
        self.coach_id = coach_id
        self.educational_institution = educational_institution
        self.sports_rank = sports_rank
        self.rank_assignment_date = rank_assignment_date
        self.snils = snils
        self.passport_data = passport_data
        self.enrollment_date = enrollment_date if enrollment_date else datetime.now().date()

    @property
    def full_name(self):
        """Полное имя ученика

        Returns:
            str: Полное имя (Фамилия Имя Отчество)
        """
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    @property
    def age(self):
        """Возраст ученика

        Returns:
            int: Возраст в годах
        """
        if not self.birth_date:
            return 0

        today = datetime.now().date()
        age = today.year - self.birth_date.year

        # Проверка, был ли уже день рождения в этом году
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1

        return age

    def to_dict(self):
        """Преобразование в словарь для сохранения в БД

        Returns:
            dict: Словарь с данными ученика
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'birth_date': self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            'group_id': self.group_id,
            'coach_id': self.coach_id,
            'educational_institution': self.educational_institution,
            'sports_rank': self.sports_rank,
            'rank_assignment_date': self.rank_assignment_date.strftime(
                '%Y-%m-%d') if self.rank_assignment_date else None,
            'snils': self.snils,
            'passport_data': self.passport_data,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря

        Args:
            data (dict): Словарь с данными ученика

        Returns:
            Student: Объект ученика
        """
        return cls(
            id=data.get('id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            middle_name=data.get('middle_name', ''),
            birth_date=datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date() if data.get('birth_date') else None,
            group_id=data.get('group_id'),
            coach_id=data.get('coach_id'),
            educational_institution=data.get('educational_institution', ''),
            sports_rank=data.get('sports_rank', ''),
            rank_assignment_date=datetime.strptime(data.get('rank_assignment_date'), '%Y-%m-%d').date() if data.get(
                'rank_assignment_date') else None,
            snils=data.get('snils', ''),
            passport_data=data.get('passport_data', ''),
            enrollment_date=datetime.strptime(data.get('enrollment_date'), '%Y-%m-%d').date() if data.get(
                'enrollment_date') else None
        )

    def filter_students(self, filters=None):
        """
        Фильтрация учеников по различным параметрам

        :param filters: словарь с параметрами фильтрации, например:
            {
                'birth_year': 2010,  # Год рождения
                'department_id': 1,  # ID отделения
                'group_id': 2,       # ID группы
                'coach_id': 3,       # ID тренера
                'medical_date_from': '2023-01-01',  # Дата медосмотра от
                'medical_date_to': '2023-12-31',    # Дата медосмотра до
                'training_allowed': True,           # Допуск к тренировкам
                'search_text': 'Иван'               # Поиск по имени/фамилии
            }
        :return: список отфильтрованных учеников
        """
        if not filters:
            return self.get_all_students()

        query_parts = ["SELECT s.*, g.name as group_name, d.name as department_name, "
                       "c.last_name || ' ' || c.first_name as coach_name "
                       "FROM students s "
                       "LEFT JOIN groups g ON s.group_id = g.id "
                       "LEFT JOIN departments d ON g.department_id = d.id "
                       "LEFT JOIN coaches c ON g.coach_id = c.id "
                       "WHERE 1=1"]
        parameters = []

        # Фильтр по году рождения
        if 'birth_year' in filters and filters['birth_year']:
            query_parts.append("AND strftime('%Y', s.birth_date) = ?")
            parameters.append(str(filters['birth_year']))

        # Фильтр по отделению
        if 'department_id' in filters and filters['department_id']:
            query_parts.append("AND g.department_id = ?")
            parameters.append(filters['department_id'])

        # Фильтр по группе
        if 'group_id' in filters and filters['group_id']:
            query_parts.append("AND s.group_id = ?")
            parameters.append(filters['group_id'])

        # Фильтр по тренеру
        if 'coach_id' in filters and filters['coach_id']:
            query_parts.append("AND g.coach_id = ?")
            parameters.append(filters['coach_id'])

        # Фильтр по дате медосмотра (от)
        if 'medical_date_from' in filters and filters['medical_date_from']:
            query_parts.append("AND s.medical_exam_date >= ?")
            parameters.append(filters['medical_date_from'])

        # Фильтр по дате медосмотра (до)
        if 'medical_date_to' in filters and filters['medical_date_to']:
            query_parts.append("AND s.medical_exam_date <= ?")
            parameters.append(filters['medical_date_to'])

        # Фильтр по допуску к тренировкам
        if 'training_allowed' in filters:
            if filters['training_allowed']:
                query_parts.append("AND s.training_allowed = 1")
            else:
                query_parts.append("AND s.training_allowed = 0")

        # Поиск по тексту (имя, фамилия)
        if 'search_text' in filters and filters['search_text']:
            query_parts.append("AND (s.last_name LIKE ? OR s.first_name LIKE ? OR s.middle_name LIKE ?)")
            search_term = f"%{filters['search_text']}%"
            parameters.extend([search_term, search_term, search_term])

        # Составляем финальный запрос
        query = " ".join(query_parts)

        # Выполняем запрос
        cursor = self.db_manager.execute_query(query, parameters)
        if not cursor:
            return []

        # Преобразуем результаты в список словарей
        students = []
        for row in cursor:
            student = dict(row)
            students.append(student)

        return students

    def filter_students(self, filters=None):
        """
        Фильтрация учеников по различным параметрам

        :param filters: словарь с параметрами фильтрации, например:
            {
                'birth_year': 2010,  # Год рождения
                'department_id': 1,  # ID отделения
                'group_id': 2,       # ID группы
                'coach_id': 3,       # ID тренера
                'medical_date_from': '2023-01-01',  # Дата медосмотра от
                'medical_date_to': '2023-12-31',    # Дата медосмотра до
                'training_allowed': True,           # Допуск к тренировкам
                'search_text': 'Иван'               # Поиск по имени/фамилии
            }
        :return: список отфильтрованных учеников
        """
        if not filters:
            return self.get_all_students()

        query_parts = ["SELECT s.*, g.name as group_name, d.name as department_name, "
                       "c.last_name || ' ' || c.first_name as coach_name "
                       "FROM students s "
                       "LEFT JOIN groups g ON s.group_id = g.id "
                       "LEFT JOIN departments d ON g.department_id = d.id "
                       "LEFT JOIN coaches c ON g.coach_id = c.id "
                       "WHERE 1=1"]
        parameters = []

        # Фильтр по году рождения
        if 'birth_year' in filters and filters['birth_year']:
            query_parts.append("AND strftime('%Y', s.birth_date) = ?")
            parameters.append(str(filters['birth_year']))

        # Фильтр по отделению
        if 'department_id' in filters and filters['department_id']:
            query_parts.append("AND g.department_id = ?")
            parameters.append(filters['department_id'])

        # Фильтр по группе
        if 'group_id' in filters and filters['group_id']:
            query_parts.append("AND s.group_id = ?")
            parameters.append(filters['group_id'])

        # Фильтр по тренеру
        if 'coach_id' in filters and filters['coach_id']:
            query_parts.append("AND g.coach_id = ?")
            parameters.append(filters['coach_id'])

        # Фильтр по дате медосмотра (от)
        if 'medical_date_from' in filters and filters['medical_date_from']:
            query_parts.append("AND s.medical_exam_date >= ?")
            parameters.append(filters['medical_date_from'])

        # Фильтр по дате медосмотра (до)
        if 'medical_date_to' in filters and filters['medical_date_to']:
            query_parts.append("AND s.medical_exam_date <= ?")
            parameters.append(filters['medical_date_to'])

        # Фильтр по допуску к тренировкам
        if 'training_allowed' in filters and filters['training_allowed'] is not None:
            query_parts.append("AND s.training_allowed = ?")
            parameters.append(1 if filters['training_allowed'] else 0)

        # Поиск по тексту (имя, фамилия)
        if 'search_text' in filters and filters['search_text']:
            query_parts.append("AND (s.last_name LIKE ? OR s.first_name LIKE ? OR s.middle_name LIKE ?)")
            search_term = f"%{filters['search_text']}%"
            parameters.extend([search_term, search_term, search_term])

        # Составляем финальный запрос
        query = " ".join(query_parts)

        # Выполняем запрос
        cursor = self.db_manager.execute_query(query, parameters)
        if not cursor:
            return []

        # Преобразуем результаты в список словарей
        students = []
        for row in cursor:
            student = dict(row)
            students.append(student)

        return students