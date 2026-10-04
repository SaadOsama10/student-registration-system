import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from deb_con import DatabaseConnect
from security import hash_password

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QLabel, QLineEdit, 
                             QTableView, QPushButton, QFormLayout, QFrame, QMessageBox,QHBoxLayout,QHeaderView,QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQuery


class ManageUsers(QWidget):
    def __init__(self,dp):
        super().__init__()
        self.dp=dp

      

        self.model = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model.setTable("USERS")  
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model) 
        # Never show (or allow in-place edits of) password hashes
        self.view.setColumnHidden(self.model.fieldIndex("Password"), True)
        self.view.setShowGrid(True)   # إظهار الخطوط بين الخلايا
        self.view.setGridStyle(Qt.DashLine)  # خط متصل
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.doubleClicked.connect(self.delete_row)


        self.setup_ui()


      
      

    def setup_ui(self):
        self.setStyleSheet("background-color: #ffffff;")

        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(20)
        
      
        
        self.lbl_title = QLabel("Manage Users")
        self.lbl_title.setStyleSheet("color: #0B3C5D; font-size: 30px; font-weight: bold;")
        self.lbl_title.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.lbl_title)
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("background-color: #dcdde1;")
        self.main_layout.addWidget(self.line)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setContentsMargins(30, 30, 30, 30)
        self.cards_layout.setSpacing(30)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.form_layout2 = QFormLayout()
        self.form_layout2.setSpacing(15)
        


        # ////////////////////////////////////////////////////////////////////////////////////////////////////////
        

        self.lbl_name = QLabel("UserName:")
        self.lbl_name.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_name = QLineEdit()
        self.txt_name.setStyleSheet(self.input_style())

        self.lbl_p = QLabel("Password:")
        self.lbl_p.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_p = QLineEdit()  
        self.txt_p.setStyleSheet(self.input_style())

        self.form_layout.addRow(self.lbl_name, self.txt_name)
        self.form_layout2.addRow(self.lbl_p, self.txt_p)
        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)
        
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////


        
        self.lbl_role = QLabel("Role:")
        self.lbl_role.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_role = QComboBox()
        self.combo_role.addItems(["Admin", "Student", "Instructor"])
        self.form_layout2.addRow(self.lbl_role, self.combo_role)


        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)

        self.main_layout.addLayout(self.cards_layout)
        

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////


        self.main_layout.addWidget(QLabel("Current Users:"))
        self.main_layout.addWidget(self.view)

        self.btn_submit = QPushButton("Register User")
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #0B3C5D;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #1e5a85;
            }
        """)
        self.btn_submit.clicked.connect(self.register_action)
        self.main_layout.addWidget(self.btn_submit)

        self.btn_refresh = QPushButton("Refresh Table")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
        """)
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.main_layout.addWidget(self.btn_refresh)

        self.setLayout(self.main_layout)

    def input_style(self):
        return """
            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
                background-color: #fcfcfc;
            }
            QLineEdit:focus {
                border: 2px solid #0B3C5D;
            }
        """

    def register_action(self):
        

        if  not self.txt_name.text()or not self.txt_p.text()or not self.combo_role.currentText() :
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
              username = self.txt_name.text()
              password = self.txt_p.text()
              role = self.combo_role.currentText()

              self.dp.query(
                  "INSERT INTO USERS (Username, Password, Role) VALUES (?, ?, ?)",
                  (username, hash_password(password), role),
              )

              self.model.select()  # Refresh table

              QMessageBox.information(self, "Success", "User registered successfully!")
              self.clear_form()

        except Exception as e:
              QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_row(self, index):
        row = index.row()
        record_id = self.model.index(row, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete User",
            f"Are you sure you want to delete User ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            ok = self.dp.run("DELETE FROM USERS WHERE User_Id = ?", (record_id,))

            if not ok:
                QMessageBox.warning(
                    self,
                    "Delete Error",
                    "Cannot delete this user.\nHe is linked to a student or instructor account."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "User deleted successfully."
                )

            self.model.select()

    def clear_form(self):
        self.txt_name.clear()
        self.txt_p.clear()

    def refresh_table(self):
        self.model.select()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ManageUsers()
#     window.setWindowTitle("Course Management System")
#     window.resize(900, 700)
#     window.show()
#     sys.exit(app.exec_())