<<<<<<< HEAD
# hakunamatata-
=======
Smart Attendance System Architecture
A Complete High-Level Technical Breakdown | Stack: Python, FastAPI, MySQL, OpenCV, JS
Overview: This document outlines the technical workflow and data flow architecture for building an
automated, face-recognition-based attendance application. The system solves the problem of proxy
attendance by verifying physical presence through computer vision and syncing logs in real-time.
Step 1: Registration (One-Time Setup)
Before the system can recognize anyone, it needs to know what the students look like.
The Process: A student uploads a clear profile photo through the JavaScript frontend web
application.
The Backend: FastAPI receives the image payload. A specialized Python library (such as
face_recognition built on dlib/OpenCV) processes the photo to isolate facial landmarks (e.g., distance
between eyes, nose shape, jawline structure). It translates these unique features into a mathematical
array of 128 numerical values known as a face embedding.
The Database: MySQL stores the student's core details (Name, Roll Number) along with this
128-number array. Crucial Optimization: The system does not store raw, heavy image files in the
database, only the highly optimized array of numbers.
Step 2: Initiating the Class
Triggering the Session: The teacher logs into their centralized dashboard built with JavaScript.
API Communication: They select their specific subject/section and click 'Start Attendance'. This
actions a secure trigger to the FastAPI backend, initializing the classroom webcam stream handled
via OpenCV.
Step 3: Real-Time Face Recognition (The Core)
Frame Capture: OpenCV captures the live video stream from the classroom hardware
frame-by-frame.
Face Detection: In every individual frame, OpenCV isolates and bounding-boxes exactly where
human faces are positioned.
Feature Extraction & Matching: The Python runtime computes the live 128-number embedding for
each face detected in the frame. It systematically compares these numbers against the pre-saved
registry in the MySQL database. If the distance between numbers falls below a strict tolerance
threshold, a positive match is established.
Step 4: Updating the Database
Data Insertion: Once a student match is confirmed (e.g., Student ID 1042 is recognized), FastAPI
immediately executes an automated write query.
Logs Registry: MySQL inserts a new row into the attendance_log table with fields: [Student_ID,
Subject_ID, Date, Time, Status: 'PRESENT'].
Duplicate Prevention: The backend validation layer explicitly blocks duplicate writes if the exact
student has already been recorded present for that specific subject hour.
Step 5: Live Dashboard Update & Export
Real-Time Feedback: The FastAPI backend broadcasts a success response to the teacher's active
dashboard. The JavaScript frontend handles this stream gracefully, updating the UI dynamically
without a full-page reload. The student's name pops up instantly on-screen.
Report Generation: At the conclusion of the session, the teacher triggers an 'Export' utility. The
Python backend pulls the aggregated table records using pandas or openpyxl and outputs a clean
Microsoft Excel report file
>>>>>>> 4a33933278dafba20e6421373a9adf60f1eabd45
