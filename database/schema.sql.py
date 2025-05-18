-- database/schema.sql
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
);

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
    enrollment_date TEXT
);

CREATE TABLE IF NOT EXISTS medical_exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    exam_date TEXT,
    results TEXT,
    clearance BOOLEAN,
    FOREIGN KEY (student_id) REFERENCES students(id)
);