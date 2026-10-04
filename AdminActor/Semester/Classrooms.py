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


class ManageClass(QWidget):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp
        self.SelectedRow = -1  # Initialize SelectedRow

        self.model = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model.setTable("CLASSROOMS")  
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model) 
        self.view.setShowGrid(True)   # إظهار الخطوط بين الخلايا
        self.view.setGridStyle(Qt.DashLine)  # خط متصل
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.clicked.connect(self.select_row)
        self.view.doubleClicked.connect(self.delete_row)

        self.setup_ui()

    def setup_ui(self):
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 10, 50, 10)
        self.main_layout.setSpacing(20)
        
        self.lbl_title = QLabel("Manage CLASSROOMS")
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
        
        self.lbl_bul = QLabel("Building:")
        self.lbl_bul.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_bul = QLineEdit()
        self.txt_bul.setStyleSheet(self.input_style())

        self.lbl_r = QLabel("Room_Number:")
        self.lbl_r.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_r = QLineEdit()  
        self.txt_r.setStyleSheet(self.input_style())

        self.form_layout.addRow(self.lbl_bul, self.txt_bul)
        self.form_layout2.addRow(self.lbl_r, self.txt_r)
        
        self.lbl_cap = QLabel("Capacity:")
        self.lbl_cap.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_cap = QLineEdit()
        self.txt_cap.setStyleSheet(self.input_style())

        # Type combobox
        self.lbl_type = QLabel("Type:")
        self.lbl_type.setStyleSheet("font-size: 16px; color: #555;")
        self.combo_type = QComboBox()
        self.combo_type.addItems(["Lecture Room", "Computer Lab", "Exam Hall"])
        self.combo_type.setStyleSheet(self.input_style())
        
        self.form_layout.addRow(self.lbl_cap, self.txt_cap)
        self.form_layout2.addRow(self.lbl_type, self.combo_type)
        
        self.form_layout.addRow(QLabel("Current CLASSROOMS:"),self.lbl_info)
        
        
        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)

        self.main_layout.addLayout(self.cards_layout)
        
        # Table view
        # self.main_layout.add(QLabel("Current CLASSROOMS:"))
        self.main_layout.addWidget(self.view)
        # self.main_layout.addWidget(self.lbl_info)

        # Add button
        self.btn_submit = QPushButton("Add CLASSROOM")
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

        # Edit button
        self.btn_edit = QPushButton("Edit CLASSROOM")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.setStyleSheet("""
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
        self.btn_edit.clicked.connect(self.update)
        self.main_layout.addWidget(self.btn_edit)

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
        if not self.txt_bul.text() or not self.txt_r.text() or not self.txt_cap.text() or not self.combo_type.currentText():
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            bluding = self.txt_bul.text()
            room = self.txt_r.text()
            cap = self.txt_cap.text()
            rtype = self.combo_type.currentText()

            
            # Insert new classroom
            sql = f"""
            INSERT INTO CLASSROOMS (Building, Room_Number, Capacity, Type)
            VALUES ('{bluding}', '{room}', '{cap}', '{rtype}')
            """

            self.dp._exec(sql)
            self.model.select()  # Refresh table
            QMessageBox.information(self, "Success", "Classroom registered successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_row(self, index):
        self.SelectedRow = index.row()
        record_id = self.model.index(self.SelectedRow, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete Classroom",
            f"Are you sure you want to delete Room ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            query = QSqlQuery()
            ok = query.exec_(f"DELETE FROM CLASSROOMS WHERE Room_Id = {record_id}")

            if not ok:
                QMessageBox.warning(
                    self,
                    "Delete Error",
                    "Cannot delete this classroom.\nIt may be linked to sections."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Classroom deleted successfully."
                )
                self.model.select()
                self.clear_form()
                self.SelectedRow = -1





    def clear_form(self):
        self.txt_bul.clear()
        self.txt_r.clear()
        self.txt_cap.clear()
        self.combo_type.setCurrentIndex(0)

    def select_row(self, index):
        self.SelectedRow = index.row()
        
        if self.SelectedRow == -1:
            return 
        
        self.id = self.model.index(self.SelectedRow, 0).data()
        
        sql = f"SELECT Building, Room_Number, Capacity, Type FROM CLASSROOMS WHERE Room_Id = {self.id}"
        query = self.dp._exec(sql)
        if query.next():
            self.txt_bul.setText(query.value(0))
            self.txt_r.setText(query.value(1))
            self.txt_cap.setText(str(query.value(2)))
            self.combo_type.setCurrentText(str(query.value(3)))

    def update(self):
        # Check if a row has been selected
        if self.SelectedRow == -1:
            QMessageBox.warning(self, "Error", "No row selected! Please select a row from the table first.")
            return
        
        # Get values from form
        bluding = self.txt_bul.text()
        room = self.txt_r.text()
        cap = self.txt_cap.text()
        rtype = self.combo_type.currentText()
        
        if not bluding or not room or not cap:
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return
        

        sql = f"""
            UPDATE CLASSROOMS 
            SET Building = '{bluding}', 
                Room_Number = '{room}', 
                Capacity = '{cap}', 
                Type = '{rtype}'   
            WHERE Room_Id = {self.id}
            """

        self.dp._exec(sql)
    
        self.model.select()  
        QMessageBox.information(self, "Success", "Classroom updated successfully!")
            
        self.clear_form()
        self.SelectedRow = -1


