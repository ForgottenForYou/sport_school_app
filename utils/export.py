# utils/export.py
import csv

def export_to_csv(data, filename="students_export.csv"):
    headers = [
        "Имя", "Возраст", "Дата рождения", "Отделение", "Группа", "Тренер",
        "Школа", "Разряд", "Дата разряда", "СНИЛС", "Паспорт", "Дата зачисления", "Прошёл медосмотр"
    ]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            # Пропускаем ID (первый элемент), форматируем медосмотр
            row = list(row[1:])  # Исключаем ID
            row[12] = "Да" if row[12] else "Нет"  # Медосмотр (последний элемент)
            writer.writerow(row)