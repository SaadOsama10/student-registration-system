from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView, 
    QHBoxLayout, QPushButton, QTableWidgetItem, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

# Approval class
class ApproveCoursesPage(QWidget):
    def __init__(self, prof_id):
        super().__init__()
        self.prof_id = prof_id
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Approve Student Course Enrollment")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #196297; margin-bottom: 10px;")
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Changed to 5 columns
        self.table.setHorizontalHeaderLabels(["Select", "Student Name", "Course", "Section Time", "Request Date"])
        
        # Table styling
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dcdcdc;
                font-size: 14px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f1f2f6;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #0B3C5D;
            }
        """)

        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_reject = QPushButton("Reject Selected")
        self.btn_reject.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; 
                color: white; 
                font-size: 16px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        self.btn_reject.clicked.connect(self.reject_selected)

        self.btn_approve = QPushButton("Approve Selected")
        self.btn_approve.setStyleSheet("""
            QPushButton {
                background-color: #27AE60; 
                color: white; 
                font-size: 16px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #219150; }
        """)
        self.btn_approve.clicked.connect(self.approve_selected)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_reject)
        btn_layout.addWidget(self.btn_approve)
        
        layout.addLayout(btn_layout)
        
        # Load data
        self.load_requests()
    
    def load_requests(self):
        """Load pending registration requests from advisees."""
        db = QSqlDatabase.database("main_connection")
        query = QSqlQuery(db)
        
        query.prepare("""
            SELECT 
                sr.Reg_Id,
                s.Student_Name,
                c.Course_Code || ' - ' || c.Course_Name AS Course
,
                sec.Time,
                date(sr.Request_Date) AS Request_Date

            FROM STUDENTS_REGISTRATIONS sr
            JOIN STUDENTS s ON sr.Student_Id = s.Student_Id
            JOIN SECTIONS sec ON sr.Section_Id = sec.Section_Id
            JOIN COURSES c ON sec.Course_Id = c.Course_Id
            WHERE s.Advisor_Id = ? AND sr.Status = 'Pending'
            ORDER BY sr.Request_Date
        """)
        query.addBindValue(self.prof_id)
        
        if not query.exec_():
            print("Error loading requests:", query.lastError().text())
            return
        
        # Clear table
        self.table.setRowCount(0)
        
        # Populate table
        row = 0
        while query.next():
            self.table.insertRow(row)
            
            reg_id = query.value(0)
            student_name = query.value(1)
            course = query.value(2)
            time = query.value(3)
            request_date = query.value(4)
            
            # Checkbox
            checkbox = QCheckBox()
            checkbox.setProperty("reg_id", reg_id)  # Store reg_id
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 0, checkbox_widget)
            
            # Data columns
            self.table.setItem(row, 1, QTableWidgetItem(student_name))
            self.table.setItem(row, 2, QTableWidgetItem(course))
            self.table.setItem(row, 3, QTableWidgetItem(time))
            self.table.setItem(row, 4, QTableWidgetItem(request_date))
            
            row += 1
        
        # Show message if no pending requests
        if row == 0:
            self.table.insertRow(0)
            item = QTableWidgetItem("No pending registration requests")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, 2, item)
            self.table.setSpan(0, 0, 1, 5)
    
    def get_selected_registrations(self):
        """Get list of selected registration IDs."""
        selected = []
        for row in range(self.table.rowCount()):
            cell_widget = self.table.cellWidget(row, 0)
            if cell_widget:
                checkbox = cell_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    reg_id = checkbox.property("reg_id")
                    selected.append(reg_id)
        return selected
    
    def approve_selected(self):
        """Approve selected registrations."""
        selected = self.get_selected_registrations()
        
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select at least one request to approve.")
            return
        
        reply = QMessageBox.question(
            self,
            'Confirm Approval',
            f'Are you sure you want to approve {len(selected)} registration(s)?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            db = QSqlDatabase.database("main_connection")
            
            success_count = 0
            for reg_id in selected:
                query = QSqlQuery(db)
                query.prepare("""
                    UPDATE STUDENTS_REGISTRATIONS
                    SET Status = 'Approved',
                        Approval_Date = datetime('now')
,
                        Approved_By = ?
                    WHERE Reg_Id = ?
                """)
                query.addBindValue(self.prof_id)
                query.addBindValue(reg_id)
                
                if query.exec_():
                    success_count += 1
            
            QMessageBox.information(self, "Success", f"{success_count} registration(s) approved successfully!")
            self.load_requests()  # Refresh
    
    def reject_selected(self):
        """Reject selected registrations."""
        selected = self.get_selected_registrations()
        
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select at least one request to reject.")
            return
        
        reply = QMessageBox.question(
            self,
            'Confirm Rejection',
            f'Are you sure you want to reject {len(selected)} registration(s)?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            db = QSqlDatabase.database("main_connection")
            
            success_count = 0
            for reg_id in selected:
                query = QSqlQuery(db)
                query.prepare("""
                    UPDATE STUDENTS_REGISTRATIONS
                    SET Status = 'Denied',
                        Approval_Date = datetime('now')
,
                        Approved_By = ?
                    WHERE Reg_Id = ?
                """)
                query.addBindValue(self.prof_id)
                query.addBindValue(reg_id)
                
                if query.exec_():
                    success_count += 1
            
            QMessageBox.information(self, "Success", f"{success_count} registration(s) rejected.")
            self.load_requests()  # Refresh