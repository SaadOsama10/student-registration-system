from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

class MyCoursesPage(QWidget):
    def __init__(self, prof_id):
        super().__init__()
        self.prof_id = prof_id
        
        layout = QVBoxLayout(self)
        
        title = QLabel("My Courses")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #196297; margin-bottom: 20px;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("View all sections you are currently teaching")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: gray; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Code", "Course Name", "Schedule", "Room", "Semester", "Enrolled", "Capacity"
        ])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dcdcdc;
                font-size: 14px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #f1f2f6;
                padding: 12px;
                border: none;
                font-weight: bold;
                color: #0B3C5D;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        layout.addWidget(self.table)

        self.load_data()

    def load_data(self):
        """Load all sections taught by this professor."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        
        query.prepare("""
            SELECT 
                c.Course_Code,
                c.Course_Name,
                sec.Time,
                cl.Building || ' ' || cl.Room_Number AS Room,
                sem.Year || ' ' || sem.Term AS Semester,
                (
                    SELECT COUNT(*) 
                    FROM STUDENTS_REGISTRATIONS sr 
                    WHERE sr.Section_Id = sec.Section_Id 
                    AND sr.Status = 'Approved'
                ) AS Enrolled,
                cl.Capacity
            FROM SECTIONS sec
            JOIN COURSES c ON sec.Course_Id = c.Course_Id
            JOIN CLASSROOMS cl ON sec.Room_Id = cl.Room_Id
            JOIN SEMESTERS sem ON sec.Sem_Id = sem.Sem_Id
            WHERE sec.Instructor_Id = ?
            ORDER BY sem.Year DESC, sem.Term, sec.Time
        """)
        query.addBindValue(self.prof_id)
        
        if not query.exec_():
            print("Error loading courses:", query.lastError().text())
            return
        
        # Clear table
        self.table.setRowCount(0)
        
        # Populate table
        row = 0
        while query.next():
            self.table.insertRow(row)
            
            course_code = query.value(0)
            course_name = query.value(1)
            time = query.value(2)
            room = query.value(3)
            semester = query.value(4)
            enrolled = query.value(5)
            capacity = query.value(6)
            
            # Add data to columns
            self.table.setItem(row, 0, QTableWidgetItem(course_code))
            self.table.setItem(row, 1, QTableWidgetItem(course_name))
            self.table.setItem(row, 2, QTableWidgetItem(time))
            self.table.setItem(row, 3, QTableWidgetItem(room))
            self.table.setItem(row, 4, QTableWidgetItem(semester))
            
            # Enrolled count
            enrolled_item = QTableWidgetItem(str(enrolled))
            enrolled_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, enrolled_item)
            
            # Capacity - color code if near full
            capacity_item = QTableWidgetItem(str(capacity))
            capacity_item.setTextAlignment(Qt.AlignCenter)
            
            # Color code based on enrollment percentage
            if enrolled >= capacity:
                capacity_item.setBackground(QColor("#E74C3C")) 
                capacity_item.setForeground(QColor("white"))
            elif enrolled >= capacity * 0.8:
                capacity_item.setBackground(QColor("#F39C12")) 
                capacity_item.setForeground(QColor("white"))
            else:
                capacity_item.setBackground(QColor("#27AE60"))  
                capacity_item.setForeground(QColor("white"))
            
            self.table.setItem(row, 6, capacity_item)
            
            row += 1
        
        # Show message if no courses
        if row == 0:
            self.table.insertRow(0)
            item = QTableWidgetItem("No courses assigned")
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor("gray"))
            self.table.setItem(0, 3, item)
            self.table.setSpan(0, 0, 1, 7)