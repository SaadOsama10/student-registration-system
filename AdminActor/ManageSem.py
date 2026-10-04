import sys

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QTextEdit, QSpinBox,
    QFrame, QPushButton, QVBoxLayout, QMainWindow, QStackedWidget, QCheckBox, QApplication, QHBoxLayout, QFormLayout
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSql import QSqlDatabase

from AdminActor.Semester.Classrooms import ManageClass
from Semester.Semesters import ManageSem as ManageSemesters 
from Semester.Payments import ManagePay
from Semester.sections import  ManageSection


class ManageSem(QFrame):
    def __init__(self, dp,right_frame):
        super().__init__()
        self.dp = dp
        self.right_frame=right_frame
        
        
        self.setFixedSize(944, 700)

        self.create_main_card(self, "Manage Classrooms", 150, 200)
        self.create_main_card(self, "Manage Payments", 150, 300)
        self.create_main_card(self, "Manage Sections", 150, 400)
        self.create_main_card(self, "Manage Semesters", 500, 200)

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
        btn.clicked.connect(lambda: self.handle_card_click(btn))
        btn.show()

    def handle_card_click(self, btn):
      
        text = btn.text().strip()
        
        if text == "Manage Classrooms":
            self.loadPage(ManageClass(self.dp))
            
        elif text == "Manage Semesters":
            self.loadPage(ManageSemesters(self.dp))
            
        elif text == "Manage Payments":
            self.loadPage(ManagePay(self.dp))

            
        elif text == "Manage Sections":
            self.loadPage(ManageSection(self.dp))
            
            

      
    def loadPage(self, widget):
        for child in self.right_frame.findChildren(QWidget):
            child.deleteLater()

        widget.setParent(self.right_frame)
        widget.setGeometry(0, 0, 944, 700)
        widget.show()      