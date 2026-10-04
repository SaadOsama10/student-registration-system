# 🎓 Student Registration System

**A desktop student information system with Admin, Instructor and Student roles: course registration with advisor approval, grading, transcripts and tuition payments, built with PyQt5 and SQLite.**

<p>
  <img src="https://img.shields.io/badge/Python-1a1b27?style=flat-square&logo=python&logoColor=7aa2f7" alt="Python" />
  <img src="https://img.shields.io/badge/PyQt5-1a1b27?style=flat-square&logo=qt&logoColor=7aa2f7" alt="PyQt5" />
  <img src="https://img.shields.io/badge/SQLite-1a1b27?style=flat-square&logo=sqlite&logoColor=7aa2f7" alt="SQLite" />
</p>

👥 Team: Saed O S Radi, Abdulrahman Zeineddin, and Zigzag2Z — university course project (FSMVU)

---

## Overview

The app is a university **student information system** (in the style of an OBS, *Öğrenci Bilgi Sistemi*) built as a Database Systems course project. A launcher lets users sign in as an **Admin**, a **Staff member (instructor)** or a **Student**, and each role gets its own dashboard. All data lives in a local SQLite database that the app creates, together with its schema, on first launch.

<p align="center">
  <img src="screenshots/login.png" width="600" alt="Role selection screen" />
</p>

## Features

### 🛠️ Admin
- Manage **students**, **instructors (staff)**, **courses**, **departments**, **majors** and **user accounts** (add / edit / delete)
- Semester management: **semesters**, **classrooms**, **course sections** (room, instructor, time) and **tuition payments**

### 👩‍🏫 Instructor
- Home dashboard with pending approvals, active courses, total students and today's schedule
- **Approve or reject** course registration requests from advisees
- **My Courses**: sections taught, with enrolment against classroom capacity
- **Marks entry** per section: Quiz (10%), Midterm (30%), Final (40%) and Project (20%), with weighted total and letter grade
- Profile page

### 🧑‍🎓 Student
- Dashboard with personal info, advisor, year, total credits and GPA
- **Course registration** for the current semester's sections. A request is created as *Pending* for advisor approval and is only allowed once the semester fee is marked *Paid*. Students can withdraw a request.
- **Transcript** with completed courses, letter grades, total credits and cumulative GPA (A.G.N.O.)
- Profile (phone, address, birth date, gender, nationality, photo)

## Screenshots

*Captured from the running app with fictional test data.*

| Admin dashboard | Admin: tuition payments |
|:---:|:---:|
| ![Admin dashboard](screenshots/admin-dashboard.png) | ![Payments](screenshots/admin-payments.png) |

| Student dashboard | Course registration |
|:---:|:---:|
| ![Student dashboard](screenshots/student-dashboard.png) | ![Course registration](screenshots/course-registration.png) |

| Instructor: approvals | Instructor: marks entry |
|:---:|:---:|
| ![Instructor approvals](screenshots/instructor-approvals.png) | ![Marks entry](screenshots/instructor-marks.png) |

| Student transcript |
|:---:|
| ![Transcript](screenshots/transcript.png) |

## Database Schema

`deb_con.py` creates 16 tables on first launch (`CREATE TABLE IF NOT EXISTS`):

| Table | Purpose / key columns |
|---|---|
| `USERS` | Login accounts: `Username`, `Password`, `Role` (Admin / Instructor / Student) |
| `DEPARTMENTS` | `Department_Name`, `Head_Instructor_Id` |
| `MAJORS` | `Major_Name` → `DEPARTMENTS` |
| `INSTRUCTORS` | Name, email → `DEPARTMENTS`, `USERS` |
| `STUDENTS` | Student number, name, email, `TC_Kimlik` → `USERS`, `MAJORS`, advisor (`INSTRUCTORS`) |
| `PROFILE` | Student contact and personal details, photo path |
| `COURSES` | Code, name, credits, type (compulsory / elective) |
| `SEMESTERS` | Year, term, start and end dates |
| `CLASSROOMS` | Building, room number, capacity, type |
| `SECTIONS` | Course offering: course, instructor, room, semester, time |
| `STUDENTS_REGISTRATIONS` | Student ↔ section, `Status` (Pending / Approved / Denied), request and approval dates, approver |
| `ASSESSMENTS` | Per-registration component grades (Quiz, Midterm, Final, Project) with weights |
| `GRADES` | Final total, letter grade and grade points per registration |
| `PAYMENTS` | Tuition payments per student and semester (status, date, amount) |
| `TRANSCRIPT`, `TRANSCRIPT_DETAILS` | Per-semester GPA and course rows (defined, not populated by the current code) |

**Relationships:** `MAJORS` and `INSTRUCTORS` belong to a `DEPARTMENTS` row. `STUDENTS` link to a `MAJORS` row, an advisor in `INSTRUCTORS` and a login in `USERS`. A `SECTIONS` row ties a `COURSES` row to an instructor, a `CLASSROOMS` row and a `SEMESTERS` row. `STUDENTS_REGISTRATIONS` joins students to sections, and each registration has its `ASSESSMENTS` and one `GRADES` row. `PAYMENTS` link students to semesters.

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python 3 |
| GUI | PyQt5 (Qt Widgets) |
| Database | SQLite via `PyQt5.QtSql` (`QSqlDatabase`, `QSqlQuery`, `QSqlQueryModel`) |

## How to Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Rule.py
```

Run it from the project root: the database (`student_management.db`) and the `assets/` icons are resolved relative to the working directory.

On first launch the app creates the database and a default admin account, **`admin` / `1234`** (stored hashed; see Known Limitations). Sign in as Admin to add departments, majors, instructors, students, courses, semesters, classrooms and sections. Students can register for courses once a *Paid* payment exists for the current semester.

## Project Structure

```
.
├── Rule.py                       # Launcher: role selection (Admin / Staff / Student)
├── deb_con.py                    # SQLite connection, schema creation, default admin
├── security.py                   # PBKDF2 password hashing and verification
├── AdminActor/                   # Admin login, dashboard and CRUD screens
│   ├── Course/ Department/ Major/ Staff/ Student/
│   ├── Semester/                 # Semesters, classrooms, sections, payments
│   └── Users.py, ManageSem.py
├── ProfessorActor/               # Instructor login, dashboard and pages
│   └── pages/                    # home, approve, courses, marks, profile
├── StudentActor/                 # Student login, dashboard, registration, transcript, profile
├── StudentAcademicCalculator.py  # Standalone calculator class (commented out, see below)
├── assets/                       # Icons and logo
├── screenshots/                  # README screenshots
└── requirements.txt
```

## Improvements

Changes made after the original course project:

- **SQL injection fixed.** Every query that used f-string SQL (logins, admin add/edit/delete screens, course registration, profile, transcript, instructor schedule) now uses parameterized queries: `QSqlQuery.prepare()` + `addBindValue()`, mostly through a shared `DatabaseConnect.query()` helper. The one `QSqlTableModel.setFilter()` call, which cannot take bound values, uses an `int()`-cast student id.
- **Hashed passwords.** Passwords are hashed with PBKDF2-HMAC-SHA256 (600,000 iterations, random 16-byte salt; standard library only, see `security.py`). All three logins go through `DatabaseConnect.authenticate()`, which compares in constant time. Plain-text passwords in databases created by older versions still work once and are upgraded to a hash on that login. New users are stored hashed, and the Manage Users table no longer shows the password column. An unused admin-login method that opened the dashboard without checking a password was removed.
- **Real transcript header.** The header GPA is now calculated from the student's grades (the same value as A.G.N.O. below the table), not a fixed "3.5". **Student State** shows *Active* when the current semester's fee is paid and *Inactive* otherwise. The "Sucess" typo is fixed.
- **Admin delete buttons work.** The nine admin delete actions used Qt's *default* database connection, which the app never opens, so deletes silently failed. They now run on the app's connection; deletes that would break foreign keys (e.g. a course that still has sections) are still refused with a message.
- **Withdrawals limited to the student's own registrations.** The delete query now also checks `Student_Id`.

These changes were verified off-screen with fictional test data: 35 automated checks (logins, injection attempts, legacy-password upgrade, user creation, deletes, registration rules, transcript values) and all 13 screens open with no errors.

## Known Limitations

- **Default admin account.** On every launch the app makes sure an `admin` account exists, re-creating it as `admin` / `1234` (stored hashed) if it is missing. There is no change-password screen, so this default login cannot be retired from inside the app.
- **Commented-out GPA calculator.** `StudentAcademicCalculator.py` (term/total credits, term GPA, total GPA) is entirely commented out and unused. GPA comes from `calculate_gpa()` in `Transcript.py` instead.
- **Unused tables.** `TRANSCRIPT` and `TRANSCRIPT_DETAILS` are created but never written by the current code.
- **Two fixed transcript fields.** The schema has no program-type or preparatory-school data, so *Program Type* ("Bachelor's") and *Preparatory Success Status* ("Success") are still fixed text.
- **Desktop-only, local database.** Single-user SQLite file, with no network or multi-user access.
