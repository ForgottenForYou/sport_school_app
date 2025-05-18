class Group:
    """Модель группы"""

    def __init__(self, id=None, name="", department_id=None, coach_id=None):
        """Инициализация объекта группы

        Args:
            id (int, optional): ID группы. Defaults to None.
            name (str, optional): Название группы. Defaults to "".
            department_id (int, optional): ID отделения. Defaults to None.
            coach_id (int, optional): ID тренера. Defaults to None.
        """
        self.id = id
        self.name = name
        self.department_id = department_id
        self.coach_id = coach_id

    def to_dict(self):
        """Преобразование в словарь для сохранения в БД

        Returns:
            dict: Словарь с данными группы
        """
        return {
            'id': self.id,
            'name': self.name,
            'department_id': self.department_id,
            'coach_id': self.coach_id
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря

        Args:
            data (dict): Словарь с данными группы

        Returns:
            Group: Объект группы
        """
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            department_id=data.get('department_id'),
            coach_id=data.get('coach_id')
        )