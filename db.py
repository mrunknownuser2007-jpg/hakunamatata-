import mysql.connector
from datetime import date

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "159207",
    "database": "face_attendance"
}

def get_db():
    tmp = mysql.connector.connect(host=DB_CONFIG["host"], user=DB_CONFIG["user"], password=DB_CONFIG["password"])
    cur = tmp.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    tmp.commit()
    cur.close()
    tmp.close()
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students(rollno VARCHAR(50) PRIMARY KEY, name VARCHAR(100), role VARCHAR(20), branch VARCHAR(50), year VARCHAR(20))")
    cur.execute("CREATE TABLE IF NOT EXISTS attendance(id INT AUTO_INCREMENT PRIMARY KEY, rollno VARCHAR(50), date DATE, time TIME, status VARCHAR(20), UNIQUE KEY unique_roll_date (rollno, date))")
    conn.commit()
    cur.close()
    conn.close()
    print("Tables ready - 1 Day 1 Attendance Locked!")

def save_student(rollno, name, role, branch, year):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("REPLACE INTO students VALUES (%s,%s,%s,%s,%s)", (rollno, name, role, branch, year))
    conn.commit()
    cur.close()
    conn.close()

def get_all_students():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def mark_attendance_db(rollno):
    conn = get_db()
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("SELECT * FROM attendance WHERE rollno=%s AND date=%s", (rollno, today))
    if cur.fetchone():
        cur.close()
        conn.close()
        print(f"BLOCKED - Already marked today: {rollno} on {today}")
        return False
    cur.execute("INSERT INTO attendance (rollno, date, time, status) VALUES (%s, CURDATE(), CURTIME(), 'Present')", (rollno,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"SAVED - {rollno} on {today}")
    return True