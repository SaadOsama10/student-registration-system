from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox


class DatabaseConnect:

    def __init__(self):
        self.database = "student_management.db"
        self.conn_name = "main_connection"
        self.db = None

    def initialize(self):
        if not self.connect():
            return False

        self._create_tables()
        self.create_default_admin()
        return True

    def connect(self) -> bool:
        if QSqlDatabase.contains(self.conn_name):
            self.db = QSqlDatabase.database(self.conn_name)
        else:
            self.db = QSqlDatabase.addDatabase("QSQLITE", self.conn_name)
            self.db.setDatabaseName(self.database)

        if not self.db.open():
            QMessageBox.critical(None, "DB Error", self.db.lastError().text())
            return False

        print("Connected to SQLite successfully!")
        return True

    def _exec(self, sql: str):
        query = QSqlQuery(self.db)
        if not query.exec_(sql):
            print("SQL error:", query.lastError().text())
            print(sql)
        return query

    def create_default_admin(self):
        query = QSqlQuery(self.db)
        query.exec_("SELECT 1 FROM USERS WHERE Username='admin'")
        if query.next():
            return

        query.exec_("""
            INSERT INTO USERS (Username, Password, Role)
            VALUES ('admin', '1234', 'Admin')
        """)
        print("Default admin created")

    def _create_tables(self):
        self._exec("PRAGMA foreign_keys = ON;")

        self._exec("""
        CREATE TABLE IF NOT EXISTS USERS (
            User_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            Role TEXT NOT NULL
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS DEPARTMENTS (
            Department_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Department_Name TEXT NOT NULL,
            Head_Instructor_Id INTEGER
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS MAJORS (
            Major_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Major_Name TEXT NOT NULL,
            Dept_Id INTEGER NOT NULL,
            FOREIGN KEY (Dept_Id) REFERENCES DEPARTMENTS(Department_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS INSTRUCTORS (
            Instructor_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Instructor_Name TEXT NOT NULL,
            Instructor_Email TEXT UNIQUE NOT NULL,
            Department_Id INTEGER NOT NULL,
            User_Id INTEGER NOT NULL,
            FOREIGN KEY (Department_Id) REFERENCES DEPARTMENTS(Department_Id),
            FOREIGN KEY (User_Id) REFERENCES USERS(User_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS STUDENTS (
            Student_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_Number TEXT UNIQUE,
            Student_Name TEXT NOT NULL,
            Student_Email TEXT UNIQUE,
            TC_Kimlik TEXT UNIQUE,
            User_Id INTEGER,
            Major_Id INTEGER,
            Advisor_Id INTEGER,
            FOREIGN KEY (User_Id) REFERENCES USERS(User_Id),
            FOREIGN KEY (Major_Id) REFERENCES MAJORS(Major_Id),
            FOREIGN KEY (Advisor_Id) REFERENCES INSTRUCTORS(Instructor_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS COURSES (
            Course_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Course_Code TEXT UNIQUE,
            Course_Name TEXT NOT NULL,
            Course_Credits INTEGER NOT NULL,
            Course_Type TEXT
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS SEMESTERS (
            Sem_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Year INTEGER NOT NULL,
            Term TEXT NOT NULL,
            Start_Date TEXT,
            End_Date TEXT
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS CLASSROOMS (
            Room_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Building TEXT,
            Room_Number TEXT,
            Capacity INTEGER,
            Type TEXT
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS SECTIONS (
            Section_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Room_Id INTEGER,
            Course_Id INTEGER,
            Instructor_Id INTEGER,
            Sem_Id INTEGER,
            Time TEXT,
            FOREIGN KEY (Room_Id) REFERENCES CLASSROOMS(Room_Id),
            FOREIGN KEY (Course_Id) REFERENCES COURSES(Course_Id),
            FOREIGN KEY (Instructor_Id) REFERENCES INSTRUCTORS(Instructor_Id),
            FOREIGN KEY (Sem_Id) REFERENCES SEMESTERS(Sem_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS STUDENTS_REGISTRATIONS (
            Reg_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_Id INTEGER,
            Section_Id INTEGER,
            Status TEXT,
            Request_Date TEXT,
            Approval_Date TEXT,
            Approved_By INTEGER,
            FOREIGN KEY (Student_Id) REFERENCES STUDENTS(Student_Id),
            FOREIGN KEY (Section_Id) REFERENCES SECTIONS(Section_Id),
            FOREIGN KEY (Approved_By) REFERENCES INSTRUCTORS(Instructor_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS GRADES (
            Grade_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Reg_Id INTEGER UNIQUE,
            Final_Total REAL,
            Grade_Letter TEXT,
            Grade_Points REAL,
            FOREIGN KEY (Reg_Id) REFERENCES STUDENTS_REGISTRATIONS(Reg_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS PROFILE (
            Student_Id INTEGER PRIMARY KEY,
            Phone TEXT,
            Address TEXT,
            Birth_Date TEXT,
            Gender TEXT,
            Nationality TEXT,
            Photo_Path TEXT,
            FOREIGN KEY (Student_Id) REFERENCES STUDENTS(Student_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS PAYMENTS (
            Payment_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Status TEXT NOT NULL,
            Sem_Id INTEGER NOT NULL,
            Student_Id INTEGER NOT NULL,
            Pay_Date TEXT NOT NULL,
            Amount REAL NOT NULL,
            FOREIGN KEY (Sem_Id) REFERENCES SEMESTERS(Sem_Id),
            FOREIGN KEY (Student_Id) REFERENCES STUDENTS(Student_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS ASSESSMENTS (
    Assessment_Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Reg_Id INTEGER NOT NULL,
    Type TEXT NOT NULL,
    Weight REAL NOT NULL,
    Grade REAL,
    UNIQUE(Reg_Id, Type),
    FOREIGN KEY (Reg_Id) REFERENCES STUDENTS_REGISTRATIONS(Reg_Id)
);
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS TRANSCRIPT (
            Transcript_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Student_Id INTEGER NOT NULL,
            Sem_Id INTEGER NOT NULL,
            GPA REAL,
            FOREIGN KEY (Student_Id) REFERENCES STUDENTS(Student_Id),
            FOREIGN KEY (Sem_Id) REFERENCES SEMESTERS(Sem_Id)
        );
        """)

        self._exec("""
        CREATE TABLE IF NOT EXISTS TRANSCRIPT_DETAILS (
            Transcript_Id INTEGER NOT NULL,
            Course_Id INTEGER NOT NULL,
            Grade_Letter TEXT,
            Grade_Points REAL,
            Credits INTEGER,
            PRIMARY KEY (Transcript_Id, Course_Id),
            FOREIGN KEY (Transcript_Id) REFERENCES TRANSCRIPT(Transcript_Id),
            FOREIGN KEY (Course_Id) REFERENCES COURSES(Course_Id)
        );
        """)
