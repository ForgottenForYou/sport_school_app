class Coach:
    """Модель тренера"""

    def __init__(self, id=None, first_name="", last_name="", middle_name="",
                 phone="", email="", department_id=None):
        """Инициализация объекта тренера

        Args:
            id (int, optional): ID тренера. Defaults to None.
            first_name (str, optional): Имя. Defaults to "".
            last_name (str, optional): Фамилия. Defaults to "".
            middle_name (str, optional): Отчество. Defaults to "".
            phone (str, optional): Телефон. Defaults to "".
            email (str, optional): Email. Defaults to "".
            department_id (int, optional): ID отделения. Defaults to None.
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.phone = phone
        self.email = email
        self.department_id = department_id

    @property
    def full_name(self):
        """Полное имя тренера

        Returns:
            str: Полное имя (Фамилия Имя Отчество)
        """
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def to_dict(self):
        """Преобразование в словарь для сохранения в БД

        Returns:
            dict: Словарь с данными тренера
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'phone': self.phone,
            'email': self.email,
            'department_id': self.department_id
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря

        Args:
            data (dict): Словарь с данными тренера

        Returns:
            Coach: Объект тренера
        """
        return cls(
            id=data.get('id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            middle_name=data.get('middle_name', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            department_id=data.get('department_id')
        )
