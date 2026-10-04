import sys

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QTextEdit, QSpinBox,
    QFrame, QPushButton, QVBoxLayout, QMainWindow, QStackedWidget, QCheckBox, QApplication, QHBoxLayout, QFormLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from AdminActor.Student.ManageStudent import ManageStu
from AdminActor.Staff.ManageStaff import ManageStaff
from AdminActor.Course.ManageCourse import ManageCourses
from AdminActor.Department.ManageDep import ManageDep
from .Users import ManageUsers
from .ManageSem import ManageSem
from AdminActor.Major.ManageMaj import ManageMaj
from PyQt5.QtSql import QSqlDatabase


class Dashboard(QMainWindow):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp

        self.setFixedSize(1244, 700)
        self.setWindowTitle("Dashboard")
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.setup_form()

    def setup_form(self):

        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(300, 0, 944, 700)
        self.right_frame.setStyleSheet("background-color: #f1f2f6;")

        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(0, 0, 300, 700)
        self.left_frame.setStyleSheet("background-color: #0B3C5D;")


        self.label = QLabel(self.left_frame)
        pixmap = QPixmap("assets/image.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(55, 40, pixmap.width(), pixmap.height())

        button_style = """
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
        
        self.create_card("Main", 250)
        self.create_card("Manage Semester", 310)


        self.btn_signout = QPushButton(" Sign out", self.left_frame)
        self.btn_signout.setGeometry(0, 640, 300, 50)
        self.btn_signout.setStyleSheet(button_style)
        self.btn_signout.setIcon(QIcon("assets/signout.png"))
        self.btn_signout.setIconSize(QSize(22, 22))
        self.btn_signout.clicked.connect(self.handle_signout)

        self.show_main_page()

    def create_card(self, title, y):
      
        card = QFrame(self.left_frame)
        card.setGeometry(0, y, 300, 55)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 5, 10, 5)
        layout.setAlignment(Qt.AlignLeft)

        btn = QPushButton(title, card)
        btn.setFixedSize(300, 50)
        btn.setStyleSheet("""
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
        """)

        layout.addWidget(btn)
        btn.clicked.connect(lambda: self.handle_card(btn))

    def show_main_page(self):
      
        for child in self.right_frame.findChildren(QWidget):
            child.deleteLater()

        container = QWidget(self.right_frame)
        container.setGeometry(0, 0, 944, 700)

        self.create_main_card(container, "Manage Students", 150, 200)
        self.create_main_card(container, "Manage Staff", 150, 300)
        self.create_main_card(container, "Manage Course", 150, 400)
        self.create_main_card(container, "Manage Users", 500, 200)
        self.create_main_card(container, "Manage Department", 500, 300)
        self.create_main_card(container, "Manage MAJORS", 500, 400)

        container.show()

    def create_main_card(self, parent, title, x, y):
      
        btn = QPushButton(title, parent)
        btn.setGeometry(x, y, 300, 70)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0B3C5D;
                color: white;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #145077;
            }
        """)
        btn.clicked.connect(lambda: self.handle_card(btn))
        btn.show()

        

    def handle_card(self, btn):
        text = btn.text().strip()

        if text == "Main":
            self.show_main_page()

        elif text == "Manage Semester":
            self.loadPage(ManageSem(self.dp,self.right_frame))
        elif text == "Manage Course":
            self.loadPage(ManageCourses(self.dp))

        elif text == "Manage Students":
            self.loadPage(ManageStu(self.dp))

        elif text == "Manage Staff":
            self.loadPage(ManageStaff(self.dp))

        elif text == "Manage Users":
            self.loadPage(ManageUsers(self.dp))

        elif text == "Manage Department":
            self.loadPage(ManageDep(self.dp))
        elif text == "Manage MAJORS":
            self.loadPage(ManageMaj(self.dp))

    def handle_signout(self):
        from AdminActor.ALogin import MainWindow
        
        self.login_window = MainWindow()
        self.login_window.show()
        self.close()

    def loadPage(self, widget):
        for child in self.right_frame.findChildren(QWidget):
            child.deleteLater()

        widget.setParent(self.right_frame)
        widget.setGeometry(0, 0, 944, 700)
        widget.show()