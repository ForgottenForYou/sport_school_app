# database/db_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_name="sport_school.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу students с новым полем medical_clearance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                birth_date TEXT,
                department TEXT,
                group_name TEXT,
                coach TEXT,
                school TEXT,
                rank TEXT,
                rank_date TEXT,
                snils TEXT,
                passport TEXT,
                enrollment_date TEXT,
                medical_clearance BOOLEAN DEFAULT 0
            )
        ''')
        self.conn.commit()

        # Проверяем, существует ли колонка medical_clearance, и добавляем её, если отсутствует
        self.cursor.execute("PRAGMA table_info(students)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if 'medical_clearance' not in columns:
            self.cursor.execute('ALTER TABLE students ADD COLUMN medical_clearance BOOLEAN DEFAULT 0')
            self.conn.commit()

    def add_student(self, student_data):
        self.cursor.execute('''
            INSERT INTO students (name, age, birth_date, department, group_name, coach, school, rank, rank_date, snils, passport, enrollment_date, medical_clearance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', student_data)
        self.conn.commit()

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def update_student(self, student_id, student_data):
        self.cursor.execute('''
            UPDATE students SET name=?, age=?, birth_date=?, department=?, group_name=?, coach=?, school=?, rank=?, rank_date=?, snils=?, passport=?, enrollment_date=?, medical_clearance=?
            WHERE id=?
        ''', (*student_data, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE id=?', (student_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()