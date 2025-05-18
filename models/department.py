# Файл models/student.py
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


# Файл models/department.py
class Department:
    """Модель отделения (вида спорта)"""

    def __init__(self, id=None, name=""):
        """Инициализация объекта отделения

        Args:
            id (int, optional): ID отделения. Defaults to None.
            name (str, optional): Название отделения. Defaults to "".
        """
        self.id = id
        self.name = name

    def to_dict(self):
        """Преобразование в словарь для сохранения в БД

        Returns:
            dict: Словарь с данными отделения
        """
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря

        Args:
            data (dict): Словарь с данными отделения

        Returns:
            Department: Объект отделения
        """
        return cls(
            id=data.get('id'),
            name=data.get('name', '')
        )