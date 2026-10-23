from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import shutil, os
from db import save_student, get_all_students, mark_attendance_db, init_db, get_db
from face_engine import register_face, recognize_face

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

init_db()

@app.post("/register")
async def register(rollno: str = Form(...), name: str = Form(...), role: str = Form(...), branch: str = Form(...), year: str = Form(...), photo: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    path = f"temp/{rollno}.jpg"
    with open(path, "wb") as f:
        shutil.copyfileobj(photo.file, f)
    save_student(rollno, name, role, branch, year)
    register_face(path, rollno)
    return {"rollno": rollno, "status": "Registered"}

@app.post("/mark-attendance")
async def mark_attendance(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    path = "temp/check.jpg"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    result = recognize_face(path)
    if not result:
        return {"error": "Face not recognized - Please register first"}
    
    rollno = result
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE rollno=%s", (rollno,))
    student = cur.fetchone()
    cur.close()
    conn.close()

    if not student:
        return {"error": "Student not in DB"}

    success = mark_attendance_db(rollno)
    if not success:
        return {"status": "Already Marked", "rollno": rollno, "name": student['name'], "branch": student['branch'], "message": "Attendance Already Marked for Today - 1 Day 1 Attendance Only"}

    return {"status": "Present", "rollno": rollno, "name": student['name'], "branch": student['branch'], "role": student['role']}

@app.get("/view-tables", response_class=HTMLResponse)
def view_tables():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
    attendance = cur.fetchall()
    cur.close()
    conn.close()
    html = "<h2>Students</h2><table border=1><tr><th>Roll</th><th>Name</th><th>Branch</th></tr>"
    for s in students:
        html+=f"<tr><td>{s['rollno']}</td><td>{s['name']}</td><td>{s['branch']}</td></tr>"
    html+="</table><h2>Attendance</h2><table border=1><tr><th>Roll</th><th>Date</th><th>Time</th><th>Status</th></tr>"
    for a in attendance:
        html+=f"<tr><td>{a['rollno']}</td><td>{a['date']}</td><td>{a['time']}</td><td>{a['status']}</td></tr>"
    html+="</table>"
    return html