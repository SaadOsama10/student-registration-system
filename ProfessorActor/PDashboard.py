from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSql import QSqlQuery, QSqlDatabase  # ADD THIS IMPORT
import sys

# IMPORT YOUR PAGES (Classes from the pages folder)
from ProfessorActor.pages.home_page import HomePage
from ProfessorActor.pages.approve_page import ApproveCoursesPage
from ProfessorActor.pages.courses_page import MyCoursesPage
from ProfessorActor.pages.marks_page import MarksPage
from ProfessorActor.pages.profile_page import ProfilePage

# MAIN DASHBOARD
class ProfessorDashboard(QMainWindow):
    def __init__(self, prof_id,dp):
        super().__init__()

        self.prof_id = prof_id
        self.prof_name = self.get_professor_name()  # ADD THIS LINE
        
        self.setFixedSize(1244, 700)
        self.setWindowTitle("Professor Dashboard")
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.buildUI()
        
        # default load hp
        self.loadPage(HomePage(self.prof_id))

    def get_professor_name(self):
        """Fetch professor name from database using prof_id."""
        db = QSqlDatabase.database("main_connection")
        
        query = QSqlQuery(db)
        query.prepare("SELECT Instructor_Name FROM INSTRUCTORS WHERE Instructor_Id = ?")
        query.addBindValue(self.prof_id)
        
        if query.exec_() and query.next():
            return query.value(0)
        else:
            print("Failed to fetch professor name")
            return "Professor"  # Default fallback

    def buildUI(self):
        # right
        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(300, 0, 944, 700)
        self.right_frame.setStyleSheet("background-color: #f1f2f6;")

        # left
        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(0, 0, 300, 700)
        self.left_frame.setStyleSheet("background-color: #0B3C5D;")

        #Uni logo
        logo = QLabel(self.left_frame)
        pixmap = QPixmap("assets/image.png").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(pixmap)
        logo.setGeometry(50, 30, pixmap.width(), pixmap.height())

        # Prof label name (NOW ENABLED!)
        name_label = QLabel(f"Welcome, {self.prof_name}!", self.left_frame)
        name_label.setFont(QFont("Arial", 14))
        name_label.setStyleSheet("color: white;")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setGeometry(10, 220, 280, 30)

        # button custom
        self.menu_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                padding-left: 40px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.12);
                border-left: 5px solid #F39C12;
            }
        """

        # prof menu button
        self.btn_home = self.create_menu_button("Main", 280)
        self.btn_approve = self.create_menu_button("Approve Courses", 340)
        self.btn_courses = self.create_menu_button("My Courses", 400)
        self.btn_marks = self.create_menu_button("Students & Marks", 460)
        self.btn_profile = self.create_menu_button("Profile", 520)

        # SIGNOUT
        self.btn_signout = QPushButton(" Sign Out", self.left_frame)
        self.btn_signout.setGeometry(0, 600, 300, 50)
        self.btn_signout.setStyleSheet(self.menu_style)
        self.btn_signout.setIcon(QIcon("assets/signout.png"))
        self.btn_signout.setIconSize(QSize(22, 22))

        # SWITCH PAGE
        self.btn_home.clicked.connect(lambda: self.loadPage(HomePage(self.prof_id)))
        self.btn_approve.clicked.connect(lambda: self.loadPage(ApproveCoursesPage(self.prof_id)))
        self.btn_courses.clicked.connect(lambda: self.loadPage(MyCoursesPage(self.prof_id)))
        self.btn_marks.clicked.connect(lambda: self.loadPage(MarksPage(self.prof_id)))
        self.btn_profile.clicked.connect(lambda: self.loadPage(ProfilePage(self.prof_id)))
        
        # signout conn
        self.btn_signout.clicked.connect(self.sign_out)

    def create_menu_button(self, text, y):
        btn = QPushButton(text, self.left_frame)
        btn.setGeometry(0, y, 300, 50)
        btn.setStyleSheet(self.menu_style)
        return btn

    def loadPage(self, widget):
        for child in self.right_frame.findChildren(QWidget):
            child.deleteLater()
        
        widget.setParent(self.right_frame)
        widget.resize(944, 700)
        widget.show()

    def sign_out(self):
        # Import inside the function to avoid circular import error with PLogin.py
        from ProfessorActor.PLogin import MainWindow
        
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfessorDashboard(prof_id=1)
    window.show()
    sys.exit(app.exec_())