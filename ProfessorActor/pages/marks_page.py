from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QTableWidget, QPushButton, QHeaderView, QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlDatabase


class MarksPage(QWidget):
    def __init__(self, prof_id):
        super().__init__()
        self.prof_id = prof_id
        self.current_section_id = None

        layout = QVBoxLayout(self)

        title = QLabel("Student Marks Management")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        layout.addWidget(title)

        self.course_combo = QComboBox()
        self.course_combo.currentIndexChanged.connect(self.load_students)
        layout.addWidget(self.course_combo)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Student ID", "Student Name", "Quiz (10%)", "Midterm (30%)",
            "Final (40%)", "Project (20%)", "Total", "Grade"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.btn_save = QPushButton("Save Grades")
        self.btn_save.clicked.connect(self.save_grades)
        layout.addWidget(self.btn_save)

        self.load_courses()

    # ---------------- COURSES ----------------
    def load_courses(self):
        db = QSqlDatabase.database("main_connection")
        q = QSqlQuery(db)

        q.prepare("""
            SELECT sec.Section_Id,
                   c.Course_Code || ' - ' || c.Course_Name
            FROM SECTIONS sec
            JOIN COURSES c ON sec.Course_Id = c.Course_Id
            WHERE sec.Instructor_Id = ?
        """)
        q.addBindValue(self.prof_id)
        q.exec_()

        self.course_combo.clear()
        self.course_combo.addItem("-- Select Section --", None)

        while q.next():
            self.course_combo.addItem(q.value(1), q.value(0))

    # ---------------- STUDENTS ----------------
    def load_students(self):
        if self.course_combo.currentData() is None:
            self.table.setRowCount(0)
            return

        self.current_section_id = self.course_combo.currentData()
        db = QSqlDatabase.database("main_connection")
        q = QSqlQuery(db)

        q.prepare("""
            SELECT s.Student_Id, s.Student_Name, sr.Reg_Id,
                   (SELECT Grade FROM ASSESSMENTS WHERE Reg_Id=sr.Reg_Id AND Type='Quiz'),
                   (SELECT Grade FROM ASSESSMENTS WHERE Reg_Id=sr.Reg_Id AND Type='Midterm'),
                   (SELECT Grade FROM ASSESSMENTS WHERE Reg_Id=sr.Reg_Id AND Type='Final'),
                   (SELECT Grade FROM ASSESSMENTS WHERE Reg_Id=sr.Reg_Id AND Type='Project'),
                   g.Final_Total, g.Grade_Letter
            FROM STUDENTS_REGISTRATIONS sr
            JOIN STUDENTS s ON sr.Student_Id = s.Student_Id
            LEFT JOIN GRADES g ON sr.Reg_Id = g.Reg_Id
            WHERE sr.Section_Id = ? AND sr.Status='Approved'
        """)
        q.addBindValue(self.current_section_id)
        q.exec_()

        self.table.setRowCount(0)

        while q.next():
            row = self.table.rowCount()
            self.table.insertRow(row)

            reg_id = q.value(2)

            item_id = QTableWidgetItem(str(q.value(0)))
            item_id.setFlags(item_id.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            name_item = QTableWidgetItem(q.value(1))
            name_item.setData(Qt.UserRole, reg_id)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, name_item)

            for i, col in enumerate([3, 4, 5, 6]):
                self.table.setItem(
                    row, i + 2,
                    QTableWidgetItem("" if q.value(col) is None else str(q.value(col)))
                )

            total_item = QTableWidgetItem("" if q.value(7) is None else str(q.value(7)))
            total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 6, total_item)

            grade_item = QTableWidgetItem("" if q.value(8) is None else q.value(8))
            grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 7, grade_item)

    # ---------------- CALCULATION ----------------
    def calculate_total_and_grade(self, q, m, f, p):
        q = float(q or 0)
        m = float(m or 0)
        f = float(f or 0)
        p = float(p or 0)

        total = q*0.1 + m*0.3 + f*0.4 + p*0.2

        if total >= 90: g='AA'
        elif total >= 85: g='BA'
        elif total >= 80: g='BB'
        elif total >= 70: g='CB'
        elif total >= 60: g='CC'
        elif total >= 55: g='DC'
        elif total >= 50: g='DD'
        elif total >= 40: g='FD'
        else: g='FF'

        points = {
            'AA':4,'BA':3.5,'BB':3,'CB':2.5,'CC':2,
            'DC':1.5,'DD':1,'FD':0.5,'FF':0
        }[g]

        return round(total,2), g, points

    # ---------------- SAVE ----------------
    def save_grades(self):
        db = QSqlDatabase.database("main_connection")

        for r in range(self.table.rowCount()):
            reg_id = self.table.item(r,1).data(Qt.UserRole)

            qz = self.table.item(r,2).text()
            md = self.table.item(r,3).text()
            fn = self.table.item(r,4).text()
            pr = self.table.item(r,5).text()

            total, grade, points = self.calculate_total_and_grade(qz,md,fn,pr)

            for t,val,w in [('Quiz',qz,10),('Midterm',md,30),('Final',fn,40),('Project',pr,20)]:
                if val.strip():
                    q = QSqlQuery(db)
                    q.prepare("""
                        INSERT INTO ASSESSMENTS (Reg_Id,Type,Weight,Grade)
                        VALUES (?,?,?,?)
                        ON CONFLICT(Reg_Id,Type)
                        DO UPDATE SET Grade=excluded.Grade
                    """)
                    q.addBindValue(reg_id)
                    q.addBindValue(t)
                    q.addBindValue(w)
                    q.addBindValue(float(val))
                    q.exec_()

            q = QSqlQuery(db)
            q.prepare("""
                INSERT INTO GRADES (Reg_Id,Final_Total,Grade_Letter,Grade_Points)
                VALUES (?,?,?,?)
                ON CONFLICT(Reg_Id)
                DO UPDATE SET
                Final_Total=excluded.Final_Total,
                Grade_Letter=excluded.Grade_Letter,
                Grade_Points=excluded.Grade_Points
            """)
            q.addBindValue(reg_id)
            q.addBindValue(total)
            q.addBindValue(grade)
            q.addBindValue(points)
            q.exec_()

        QMessageBox.information(self,"Success","Grades saved")
        self.load_students()
