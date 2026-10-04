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


class ManageSem(QWidget):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp
        self.SelectedRow = -1  
        
        

        self.model = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model.setTable("SEMESTERS")  
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model) 
        self.view.setShowGrid(True)  
        self.view.setGridStyle(Qt.DashLine)
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
        
        self.lbl_title = QLabel("Manage SEMESTERS")
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
        
        self.lbl_y = QLabel("Year:")
        self.lbl_y.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_y = QLineEdit()
        self.txt_y.setStyleSheet(self.input_style())

        self.lbl_t = QLabel("Term:")
        self.lbl_t.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_t = QComboBox() 
        self.txt_t.addItems(["Fall" , "Spring" , "Summer"])
        self.txt_t.setStyleSheet(self.input_style())

        self.form_layout.addRow(self.lbl_y, self.txt_y)
        self.form_layout2.addRow(self.lbl_t, self.txt_t)
        
        self.lbl_str = QLabel("Start Date:")
        self.lbl_str.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_str = QDateEdit()
        self.txt_str.setCalendarPopup(True)
        self.txt_str.setDisplayFormat("yyyy-MM-dd")
        self.txt_str.setDate(QDate.currentDate())


        self.lbl_end = QLabel("End Date:")
        self.lbl_end.setStyleSheet("font-size: 16px; color: #555;")
        self.txt_end = QDateEdit()
        self.txt_end.setCalendarPopup(True)
        self.txt_end.setDisplayFormat("yyyy-MM-dd")
        self.txt_end.setDate(QDate.currentDate().addMonths(4))
        
        self.form_layout.addRow(self.lbl_str, self.txt_str)
        self.form_layout2.addRow(self.lbl_end, self.txt_end)
        
        self.form_layout.addRow(QLabel("Current SEMESTERS:"),self.lbl_info)
        
        
        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)

        self.main_layout.addLayout(self.cards_layout)
        
    
        self.main_layout.addWidget(self.view)

        self.btn_submit = QPushButton("Add SEMESTER")
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

        self.btn_edit = QPushButton("Edit SEMESTER")
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
        if not self.txt_y.text()  or not self.txt_str.text() or not self.txt_end.text():
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            year = self.txt_y.text()
            term = self.txt_t.currentText()
            start = self.txt_str.date().toString("yyyy-MM-dd")
            end = self.txt_end.date().toString("yyyy-MM-dd")


          
            self.dp.query(
                "INSERT INTO SEMESTERS (Year, Term, Start_Date, End_Date) VALUES (?, ?, ?, ?)",
                (year, term, start, end),
            )
            self.model.select()  # Refresh table
            QMessageBox.information(self, "Success", " registered successfully!")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_row(self, index):
        self.SelectedRow = index.row()
        record_id = self.model.index(self.SelectedRow, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete Semester",
            f"Are you sure you want to delete Semester ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            ok = self.dp.run("DELETE FROM SEMESTERS WHERE Sem_Id = ?", (record_id,))

            if not ok:
                QMessageBox.warning(
                    self,
                    "Delete Error",
                    "Cannot delete this semester.\nIt is linked to sections, registrations, or payments."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Semester deleted successfully."
                )
                self.model.select()
                self.clear_form()
                self.SelectedRow = -1




    def clear_form(self):
        self.txt_y.clear()
        self.txt_t.setCurrentIndex(0)
        self.txt_str.setDate(QDate.currentDate())
        self.txt_end.setDate(QDate.currentDate().addMonths(4))


    def select_row(self, index):
        self.SelectedRow = index.row()
        if self.SelectedRow == -1:
            return 
        
        self.id = self.model.index(self.SelectedRow, 0).data()
        query = self.dp.query(
            "SELECT Year, Term, Start_Date, End_Date FROM SEMESTERS WHERE Sem_Id = ?",
            (self.id,),
        )
        
        if query.next():
            self.txt_y.setText(str(query.value(0)))
            self.txt_t.setCurrentText(query.value(1))
            start = query.value(2)
            end = query.value(3)
            
            # self.txt_str.setDate(start)
            # self.txt_end.setDate(end)



    def update(self):
        if self.SelectedRow == -1:
            QMessageBox.warning(self, "Error", "No row selected! Please select a row from the table first.")
            return
        
        year = self.txt_y.text()
        term = self.txt_t.currentText()
        start = self.txt_str.date().toString("yyyy-MM-dd")
        end = self.txt_end.date().toString("yyyy-MM-dd")

        
        if not year or not term or not start or not end:
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return
        

        self.dp.query(
            "UPDATE SEMESTERS SET Year = ?, Term = ?, Start_Date = ?, End_Date = ? WHERE Sem_Id = ?",
            (year, term, start, end, self.id),
        )
    
        self.model.select()  
        QMessageBox.information(self, "Success", "updated successfully!")
            
        self.clear_form()
        self.SelectedRow = -1


