from datetime import datetime


class MedicalExamination:
    """Модель углубленного медицинского осмотра (УМО)"""

    def __init__(self, id=None, student_id=None, examination_date=None,
                 result="", next_examination_date=None, notes=""):
        """Инициализация объекта медосмотра

        Args:
            id (int, optional): ID медосмотра. Defaults to None.
            student_id (int, optional): ID ученика. Defaults to None.
            examination_date (datetime.date, optional): Дата осмотра. Defaults to None.
            result (str, optional): Результат осмотра. Defaults to "".
            next_examination_date (datetime.date, optional): Дата следующего осмотра. Defaults to None.
            notes (str, optional): Примечания. Defaults to "".
        """
        self.id = id
        self.student_id = student_id
        self.examination_date = examination_date if examination_date else datetime.now().date()
        self.result = result
        self.next_examination_date = next_examination_date
        self.notes = notes

    def to_dict(self):
        """Преобразование в словарь для сохранения в БД

        Returns:
            dict: Словарь с данными медосмотра
        """
        return {
            'id': self.id,
            'student_id': self.student_id,
            'examination_date': self.examination_date.strftime('%Y-%m-%d') if self.examination_date else None,
            'result': self.result,
            'next_examination_date': self.next_examination_date.strftime(
                '%Y-%m-%d') if self.next_examination_date else None,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря

        Args:
            data (dict): Словарь с данными медосмотра

        Returns:
            MedicalExamination: Объект медосмотра
        """
        return cls(
            id=data.get('id'),
            student_id=data.get('student_id'),
            examination_date=datetime.strptime(data.get('examination_date'), '%Y-%m-%d').date() if data.get(
                'examination_date') else None,
            result=data.get('result', ''),
            next_examination_date=datetime.strptime(data.get('next_examination_date'), '%Y-%m-%d').date() if data.get(
                'next_examination_date') else None,
            notes=data.get('notes', '')
        )