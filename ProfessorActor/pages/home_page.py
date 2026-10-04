from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QMessageBox,QTableWidget, QHeaderView, QTableView,QTableWidgetItem, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQueryModel
from PyQt5.QtCore import Qt



# HP CLASS
class HomePage(QWidget):
    def __init__(self, prof_id):
        super().__init__()
        self.prof_id = prof_id 

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(30)

        # Get professor name from database
        prof_name = self.get_prof_name()

        # Welcome
        welcome = QLabel(f"Welcome back, {prof_name}")
        welcome.setFont(QFont("Arial", 24, QFont.Bold))
        welcome.setStyleSheet("color: #0B3C5D;")
        self.main_layout.addWidget(welcome)

        # Metric cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Get real data from database
        pending = self.get_pending_approvals()
        courses = self.get_active_courses()
        students = self.get_total_students()

        # c1 - Pending Approvals
        self.card1 = self.create_card("Pending Approvals", str(pending), "#E74C3C") 
        cards_layout.addWidget(self.card1)

        # c2 - Active Courses
        self.card2 = self.create_card("Active Courses", str(courses), "#27AE60")
        cards_layout.addWidget(self.card2)

        # c3 - Total Students (advisees)
        self.card3 = self.create_card("Total Students", str(students), "#F39C12")
        cards_layout.addWidget(self.card3)

        self.main_layout.addLayout(cards_layout)

        # Schedule title
        lbl_schedule = QLabel("Today's Schedule")
        lbl_schedule.setFont(QFont("Arial", 18, QFont.Bold))
        lbl_schedule.setStyleSheet("color: #0B3C5D; margin-top: 20px;")
        self.main_layout.addWidget(lbl_schedule)

        # Schedule table
        self.model = QSqlQueryModel()

        sql = """
                SELECT

                    R.Room_Number,
                    R.Building,
                    C.Course_Code,
                    C.Course_Name,
                    S.Time
                FROM SECTIONS S
                JOIN COURSES C ON S.Course_Id = C.Course_Id
                JOIN CLASSROOMS R ON S.Room_Id = R.Room_Id
                WHERE S.Instructor_Id = ?
                And S.Sem_Id = (SELECT Sem_Id FROM SEMESTERS ORDER BY Start_Date DESC LIMIT 1
)
                """

        schedule_query = QSqlQuery(QSqlDatabase.database("main_connection"))
        schedule_query.prepare(sql)
        schedule_query.addBindValue(self.prof_id)
        schedule_query.exec_()
        self.model.setQuery(schedule_query)
        if not self.model.query().isActive():
            error = self.model.lastError().text()
            QMessageBox.critical(self, "Query Error", f"Failed to execute query:\n{error}")
            
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setShowGrid(True)
        self.view.setGridStyle(Qt.DashLine)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setStretchLastSection(True)

        
        # Load schedule data
        # self.load_schedule()
        self.main_layout.addWidget(self.view)

    def get_prof_name(self):
        """Get professor name from database."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        query.prepare("SELECT Instructor_Name FROM INSTRUCTORS WHERE Instructor_Id = ?")
        query.addBindValue(self.prof_id)
        
        if query.exec_() and query.next():
            return query.value(0)
        return "Professor"

    def get_pending_approvals(self):
        """Count pending registration approvals for students this professor advises."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        query.prepare("""
            SELECT COUNT(*) 
            FROM STUDENTS_REGISTRATIONS sr
            JOIN STUDENTS s ON sr.Student_Id = s.Student_Id
            WHERE s.Advisor_Id = ? AND sr.Status = 'Pending'
        """)
        query.addBindValue(self.prof_id)
        
        if query.exec_() and query.next():
            return query.value(0)
        return 0

    def get_active_courses(self):
        """Count sections this professor is currently teaching."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        query.prepare("""
            SELECT COUNT(*) 
            FROM SECTIONS 
            WHERE Instructor_Id = ?
        """)
        query.addBindValue(self.prof_id)
        
        if query.exec_() and query.next():
            return query.value(0)
        return 0

    def get_total_students(self):
        """Count students this professor advises."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        query.prepare("""
            SELECT COUNT(*) 
            FROM STUDENTS 
            WHERE Advisor_Id = ?
        """)
        query.addBindValue(self.prof_id)
        
        if query.exec_() and query.next():
            return query.value(0)
        return 0

    # def load_schedule(self):
        """Load professor's teaching schedule."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        query.prepare("""
            SELECT 
                sec.Time,
                c.Course_Code || ' - ' || c.Course_Name AS Course,
                cl.Building || ' ' || cl.Room_Number AS Room

            FROM SECTIONS sec
            JOIN COURSES c ON sec.Course_Id = c.Course_Id
            JOIN CLASSROOMS cl ON sec.Room_Id = cl.Room_Id
            WHERE sec.Instructor_Id = ?
            ORDER BY sec.Time
        """)
        query.addBindValue(self.prof_id)
        
        if not query.exec_():
            print("Error loading schedule:", query.lastError().text())
            return
        
        # Clear existing rows
        self.schedule_table.setRowCount(0)
        
        # Add data to table
        row = 0
        while query.next():
            self.schedule_table.insertRow(row)
            
            time = query.value(0)
            course = query.value(1)
            room = query.value(2)
            
            self.schedule_table.setItem(row, 0, QTableWidgetItem(time))
            self.schedule_table.setItem(row, 1, QTableWidgetItem(course))
            self.schedule_table.setItem(row, 2, QTableWidgetItem(room))
            
            row += 1
        
        # If no schedule, show a message
        if row == 0:
            self.schedule_table.insertRow(0)
            item = QTableWidgetItem("No classes scheduled")
            item.setForeground(QColor("gray"))
            self.schedule_table.setItem(0, 1, item)

    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)
        card.setFixedSize(250, 120)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        
        lbl_value = QLabel(value)
        lbl_value.setFont(QFont("Arial", 30, QFont.Bold))
        lbl_value.setStyleSheet(f"color: {color}; border: none;")
        
        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Arial", 12))
        lbl_title.setStyleSheet("color: gray; border: none;")
        
        layout.addWidget(lbl_value)
        layout.addWidget(lbl_title)
        
        return card