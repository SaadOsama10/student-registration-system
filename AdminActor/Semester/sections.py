import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from deb_con import DatabaseConnect

from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QLabel, QLineEdit, 
                             QTableView, QPushButton, QFormLayout, QFrame, QMessageBox, QHBoxLayout, QHeaderView, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate



class ManageSection(QWidget):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp
        self.SelectedRow = -1  # Initialize SelectedRow
        
        self.model = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model.setTable("SECTIONS")  
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
        

        self.view = QTableView()
        self.view.setModel(self.model) 
        self.view.setShowGrid(True)   # إظهار الخطوط بين الخلايا
        self.view.setGridStyle(Qt.DashLine)  # خط متصل
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.doubleClicked.connect(self.delete_row)
                

        

        self.setup_ui()

    def setup_ui(self):
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 10, 50, 10)
        self.main_layout.setSpacing(20)
        
        self.lbl_title = QLabel("Manage Sections")
        self.lbl_title.setStyleSheet("color: #0B3C5D; font-size: 30px; font-weight: bold;")
        self.lbl_title.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.lbl_title)
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("background-color: #dcdde1;")
        self.main_layout.addWidget(self.line)

        self.cards_layout = QHBoxLayout()
        self.cards_layout.setContentsMargins(30, 10, 30, 10)
        self.cards_layout.setSpacing(30)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.form_layout2 = QFormLayout()
        self.form_layout2.setSpacing(15)
        
        self.lbl_info = QLabel()
        self.lbl_info.setPixmap(QIcon("assets/note.png").pixmap(24, 24))
        self.lbl_info.setToolTip("Double-click on any row to delete it")
        self.lbl_info.setStyleSheet("font-size: 20px; color: #0B3C5D;")

        
        self.lbl_rid = QLabel("Room_Id:")
        self.lbl_rid.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_rid = QComboBox()
        self.combo_rid.setStyleSheet(self.input_style())

        sql = "SELECT Room_Id, Room_Number FROM CLASSROOMS "
        query = self.dp._exec(sql)


        while query.next():
            id = query.value(0)
            name = query.value(1)
            self.combo_rid.addItem(str(name), id)
        print("ddddddddddddddddddd")

        self.lbl_cid= QLabel("Course_Id:")
        self.lbl_cid.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_cid = QComboBox()
        self.combo_cid.setStyleSheet(self.input_style())
        sql = "SELECT Course_Id, Course_Name FROM COURSES "
        query = self.dp._exec(sql)

        while query.next():
            id = query.value(0)
            name = query.value(1)
            
            self.combo_cid.addItem(name, id)

        self.form_layout.addRow(self.lbl_rid, self.combo_rid)
        self.form_layout2.addRow(self.lbl_cid, self.combo_cid)
        
        self.lbl_iid = QLabel("Instructor_Id:")
        self.lbl_iid.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_iid= QComboBox()
        self.combo_iid.setStyleSheet(self.input_style())
        sql = "SELECT Instructor_Id, Instructor_Name FROM INSTRUCTORS "
        query = self.dp._exec(sql)

        while query.next():
            id = query.value(0)
            name = query.value(1)
            self.combo_iid.addItem(name, id)
            
        self.lbl_stu = QLabel("Sem_Id:")
        self.lbl_stu.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_stu = QComboBox()
        self.combo_stu.setStyleSheet(self.input_style())
        sql = "SELECT Sem_Id, Year , Term FROM SEMESTERS "
        query = self.dp._exec(sql)

        while query.next():
            id = query.value(0)
            year = query.value(1)
            term = query.value(2)
            self.combo_stu.addItem(f"{year} {term}", id)

      
        self.lbl_time = QLabel("Time:")
        self.lbl_time.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_time = QLineEdit()
        self.txt_time.setStyleSheet(self.input_style())

        
        self.form_layout.addRow(self.lbl_iid, self.combo_iid)
        self.form_layout2.addRow(self.lbl_stu, self.combo_stu)
        self.form_layout2.addRow(self.lbl_time, self.txt_time)

        self.form_layout.addRow(QLabel("Current Sections:"),self.lbl_info)
        

        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)

        self.main_layout.addLayout(self.cards_layout)
        
      
        self.main_layout.addWidget(self.view)

        # Add button
        self.btn_submit = QPushButton("Add Section")
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

      

        self.setLayout(self.main_layout)

    def input_style(self):
        return """
            QLineEdit, QComboBox {
                border: 2px solid #dcdde1;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
                background-color: #fcfcfc;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0B3C5D;
            }
        """

    def register_action(self):
        if not self.txt_time.text() :
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            rid = self.combo_rid.currentData()
            cid = self.combo_cid.currentData()
            iid = self.combo_iid.currentData()
            semester = self.combo_stu.currentData()
            time = self.txt_time.text()
            

            
            # Insert new classroom
            sql = f"""
            INSERT INTO SECTIONS (Room_Id, Course_Id, Instructor_Id, Sem_Id,Time)
            VALUES ('{rid}', '{cid}', '{iid}', '{semester}', '{time}')
            """

            self.dp._exec(sql)
            self.model.select()  # Refresh table
            QMessageBox.information(self, "Success", " Section registered successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_row(self, index):
        self.SelectedRow = index.row()
        record_id = self.model.index(self.SelectedRow, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete Section",
            f"Are you sure you want to delete Section ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            query = QSqlQuery()
            ok = query.exec_(f"DELETE FROM SECTIONS WHERE Section_Id = {record_id}")

            if not ok:
                QMessageBox.warning(
                    self,
                    "Delete Error",
                    "Cannot delete this section.\nIt is linked to registrations or grades."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Section deleted successfully."
                )
                self.model.select()
                self.clear_form()
                self.SelectedRow = -1





    def clear_form(self):
        
        self.txt_time.clear()
        self.combo_rid.setCurrentIndex(0)
        self.combo_cid.setCurrentIndex(0)
        self.combo_iid.setCurrentIndex(0)
        self.combo_stu.setCurrentIndex(0)

  


