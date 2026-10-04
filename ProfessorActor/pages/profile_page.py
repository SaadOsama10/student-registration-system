from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout
)
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os

class ProfilePage(QWidget):
    def __init__(self, prof_id):
        super().__init__()
        self.prof_id = prof_id

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)

        # Title
        title = QLabel("My Profile")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #0B3C5D; margin-bottom: 10px;")
        self.main_layout.addWidget(title)

        # Main Profile Card
        profile_card = QFrame()
        profile_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)

        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(40, 40, 40, 40)
        profile_layout.setSpacing(40)

        # Left Side - Profile Picture
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        left_layout.setSpacing(15)

        # Profile Picture
        self.profile_pic = QLabel()
        self.profile_pic.setFixedSize(180, 180)
        self.profile_pic.setAlignment(Qt.AlignCenter)

        if os.path.exists("assets/profile.png"):
            pixmap = QPixmap("assets/profile.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.profile_pic.setPixmap(pixmap)
            self.profile_pic.setStyleSheet("border-radius: 90px; border: 4px solid #0B3C5D;")
        else:
            self.profile_pic.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0B3C5D, stop:1 #196297);
                border-radius: 90px;
                color: white;
                font-size: 72px;
                font-weight: bold;
                border: 4px solid #0B3C5D;
            """)
            self.profile_pic.setText("👤")

        left_layout.addWidget(self.profile_pic)

        # Name under picture
        self.lbl_name = QLabel("")
        self.lbl_name.setFont(QFont("Arial", 20, QFont.Bold))
        self.lbl_name.setStyleSheet("color: #0B3C5D;")
        self.lbl_name.setAlignment(Qt.AlignCenter)
        self.lbl_name.setWordWrap(True)

        self.lbl_role = QLabel("Professor")
        self.lbl_role.setFont(QFont("Arial", 14))
        self.lbl_role.setStyleSheet("color: #666; margin-top: 5px;")
        self.lbl_role.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(self.lbl_name)
        left_layout.addWidget(self.lbl_role)
        left_layout.addStretch()

        # Right Side - Information Grid
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setSpacing(20)

        # Info section title
        info_title = QLabel("Contact Information")
        info_title.setFont(QFont("Arial", 16, QFont.Bold))
        info_title.setStyleSheet("color: #0B3C5D; margin-bottom: 10px;")
        right_layout.addWidget(info_title)

        # Info Grid
        info_grid = QGridLayout()
        info_grid.setSpacing(20)
        info_grid.setColumnStretch(1, 1)

        # Email
        email_icon = QLabel("✉️")
        email_icon.setFont(QFont("Arial", 18))
        email_icon.setFixedWidth(40)

        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Arial", 12, QFont.Bold))
        email_label.setStyleSheet("color: #555;")

        self.email_value = QLabel("")
        self.email_value.setFont(QFont("Arial", 12))
        self.email_value.setStyleSheet("""
            color: #333;
            padding: 10px 12px;
            background-color: #f8f9fa;
            border-radius: 5px;
        """)
        self.email_value.setMinimumHeight(36)

        info_grid.addWidget(email_icon, 0, 0)
        info_grid.addWidget(email_label, 0, 1)
        info_grid.addWidget(self.email_value, 1, 1)

        # Department
        dept_icon = QLabel("🏢")
        dept_icon.setFont(QFont("Arial", 18))
        dept_icon.setFixedWidth(40)

        dept_label = QLabel("Department")
        dept_label.setFont(QFont("Arial", 12, QFont.Bold))
        dept_label.setStyleSheet("color: #555;")

        self.dept_value = QLabel("")
        self.dept_value.setFont(QFont("Arial", 12))
        self.dept_value.setStyleSheet("""
            color: #333;
            padding: 10px 12px;
            background-color: #f8f9fa;
            border-radius: 5px;
        """)
        self.dept_value.setMinimumHeight(36)

        info_grid.addWidget(dept_icon, 2, 0)
        info_grid.addWidget(dept_label, 2, 1)
        info_grid.addWidget(self.dept_value, 3, 1)

        right_layout.addLayout(info_grid)
        right_layout.addSpacing(20)

        # Statistics section
        stats_title = QLabel("Teaching Overview")
        stats_title.setFont(QFont("Arial", 16, QFont.Bold))
        stats_title.setStyleSheet("color: #0B3C5D; margin-top: 10px; margin-bottom: 10px;")
        right_layout.addWidget(stats_title)

        # Stats Cards Container
        stats_container = QHBoxLayout()
        stats_container.setSpacing(15)

        # Cards
        self.sections_card = self.create_stat_card("📚", "0", "Active Sections", "#27AE60")
        self.advisees_card = self.create_stat_card("👥", "0", "Students Advised", "#3498DB")
        self.pending_card = self.create_stat_card("⏳", "0", "Pending Approvals", "#F39C12")

        stats_container.addWidget(self.sections_card)
        stats_container.addWidget(self.advisees_card)
        stats_container.addWidget(self.pending_card)

        right_layout.addLayout(stats_container)
        right_layout.addStretch()

        # Add sections to main card
        profile_layout.addWidget(left_container, 1)
        profile_layout.addWidget(right_container, 2)

        self.main_layout.addWidget(profile_card)

        # Load data
        self.load_profile()

    def create_stat_card(self, icon, value, label, color):
        """Create a statistics card."""
        card = QFrame()
        card.setFixedHeight(135)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                border-left: 5px solid {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(4)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        icon_label.setAlignment(Qt.AlignLeft)

        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 28, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignLeft)

        # Label
        text_label = QLabel(label)
        text_label.setFont(QFont("Arial", 10))
        text_label.setStyleSheet("color: #666;")
        text_label.setAlignment(Qt.AlignLeft)

        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(text_label)

        # Store reference to update later
        card.value_label = value_label

        return card

    def load_profile(self):
        """Load professor profile information."""
        db = QSqlDatabase.database("main_connection")

        # Basic info
        query = QSqlQuery(db)
        query.prepare("""
            SELECT 
                i.Instructor_Name, 
                i.Instructor_Email,
                d.Department_Name
            FROM INSTRUCTORS i
            JOIN DEPARTMENTS d ON d.Department_Id = i.Department_Id
            WHERE i.Instructor_Id = ?
        """)
        query.addBindValue(self.prof_id)

        if query.exec_() and query.next():
            self.lbl_name.setText(query.value(0))
            self.email_value.setText(query.value(1))
            self.dept_value.setText(query.value(2) + " Department")

        # Sections count
        sections_query = QSqlQuery(db)
        sections_query.prepare("SELECT COUNT(*) FROM SECTIONS WHERE Instructor_Id = ?")
        sections_query.addBindValue(self.prof_id)

        if sections_query.exec_() and sections_query.next():
            self.sections_card.value_label.setText(str(sections_query.value(0)))

        # Advisees count
        advisees_query = QSqlQuery(db)
        advisees_query.prepare("SELECT COUNT(*) FROM STUDENTS WHERE Advisor_Id = ?")
        advisees_query.addBindValue(self.prof_id)

        if advisees_query.exec_() and advisees_query.next():
            self.advisees_card.value_label.setText(str(advisees_query.value(0)))

        # Pending approvals count
        pending_query = QSqlQuery(db)
        pending_query.prepare("""
            SELECT COUNT(*) 
            FROM STUDENTS_REGISTRATIONS sr
            JOIN STUDENTS s ON sr.Student_Id = s.Student_Id
            WHERE s.Advisor_Id = ? AND sr.Status = 'Pending'
        """)
        pending_query.addBindValue(self.prof_id)

        if pending_query.exec_() and pending_query.next():
            self.pending_card.value_label.setText(str(pending_query.value(0)))
