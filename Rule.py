from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QApplication, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont,QIcon
from PyQt5.QtCore import Qt
import sys
from AdminActor.ALogin import MainWindow as AdminLoginWindow
from ProfessorActor.PLogin import MainWindow as ProfLoginWindow
from StudentActor.SLogin import MainWindow as StudentLoginWindow





class MainLoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FSMVU Login")
        self.setGeometry(350, 200,1200 , 680)
        self.setFixedSize(900, 600)
        self.setWindowIcon(QIcon("assets/icon.png"))


        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20)

        logo = QLabel()
        pix = QPixmap("assets/image.png").scaled(
            160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(pix)
        logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo)

        title = QLabel("FATİH SULTAN MEHMET VAKIF UNIVERSITY")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Student Information System")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        button_box = QVBoxLayout()
        button_box.setSpacing(15)

        btn_admin = self.make_button("Admin Login")
        btn_doctor = self.make_button("Staff Login")
        btn_student = self.make_button("Student Login")

        button_box.addWidget(btn_admin)
        button_box.addWidget(btn_doctor)
        button_box.addWidget(btn_student)

        main_layout.addLayout(button_box)

        btn_admin.clicked.connect(self.open_admin_login)

        btn_doctor.clicked.connect(self.open_instructor_login)
        btn_student.clicked.connect(self.open_student_login)

    def make_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(55)
        btn.setFont(QFont("Arial", 13, QFont.Bold))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1B4F72;
            }
        """)
        return btn

    def open_admin_login(self):
        self.admin_window = AdminLoginWindow()
        self.admin_window.show()
        self.close()

    def open_instructor_login(self):
        self.Staff_window = ProfLoginWindow()
        self.Staff_window.show()
        self.close()

    def open_student_login(self):
        self.Student_window = StudentLoginWindow()
        self.Student_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainLoginScreen()
    w.show()
    sys.exit(app.exec_())
