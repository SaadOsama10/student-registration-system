import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from deb_con import DatabaseConnect

from PyQt5.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QLabel, QLineEdit,
    QTableView, QPushButton, QFormLayout, QFrame,
    QMessageBox, QHBoxLayout, QHeaderView, QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QDateEdit


class ManagePay(QWidget):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp
        self.SelectedRow = -1
        self.id = None

        self.db = QSqlDatabase.database("main_connection")

        self.model = QSqlTableModel(None, self.db)
        self.model.setTable("PAYMENTS")
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

        self.lbl_title = QLabel("Manage PAYMENTS")
        self.lbl_title.setStyleSheet("color: #0B3C5D; font-size: 30px; font-weight: bold;")
        self.main_layout.addWidget(self.lbl_title)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(self.line)

        self.cards_layout = QHBoxLayout()

        self.form_layout = QFormLayout()
        self.form_layout2 = QFormLayout()

        self.lbl_sta = QLabel("Status:")
        self.combo_sta = QComboBox()
        self.combo_sta.addItems(["Paid", "Unpaid"])

        self.lbl_sem = QLabel("Sem_Id:")
        self.combo_sem = QComboBox()
        q = QSqlQuery(self.db)
        q.exec_("SELECT Sem_Id, Year, Term FROM SEMESTERS")
        while q.next():
            self.combo_sem.addItem(f"{q.value(1)} {q.value(2)}", q.value(0))

        self.lbl_stu = QLabel("Student_Id:")
        self.combo_stu = QComboBox()
        q.exec_("SELECT Student_Id, Student_Name FROM STUDENTS")
        while q.next():
            self.combo_stu.addItem(q.value(1), q.value(0))

        self.lbl_date = QLabel("Date:")
        self.txt_date = QDateEdit()
        self.txt_date.setCalendarPopup(True)
        self.txt_date.setDisplayFormat("yyyy-MM-dd")
        self.txt_date.setDate(QDate.currentDate())

        self.lbl_amou = QLabel("Amount:")
        self.txt_amoun = QLineEdit()

        self.form_layout.addRow(self.lbl_sta, self.combo_sta)
        self.form_layout.addRow(self.lbl_stu, self.combo_stu)

        self.form_layout2.addRow(self.lbl_sem, self.combo_sem)
        self.form_layout2.addRow(self.lbl_date, self.txt_date)
        self.form_layout2.addRow(self.lbl_amou, self.txt_amoun)

        self.cards_layout.addLayout(self.form_layout)
        self.cards_layout.addLayout(self.form_layout2)

        self.main_layout.addLayout(self.cards_layout)
        self.main_layout.addWidget(self.view)

        self.btn_submit = QPushButton("Add Payment")
        self.btn_submit.clicked.connect(self.register_action)
        self.main_layout.addWidget(self.btn_submit)

        self.btn_edit = QPushButton("Edit")
        self.btn_edit.clicked.connect(self.update)
        self.main_layout.addWidget(self.btn_edit)

        self.setLayout(self.main_layout)

    # ---------------- LOGIC ----------------

    def register_action(self):
        if not self.txt_amoun.text():
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            amount = float(self.txt_amoun.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be numeric")
            return

        q = QSqlQuery(self.db)
        q.prepare("""
            INSERT INTO PAYMENTS
            (Status, Sem_Id, Student_Id, Pay_Date, Amount)
            VALUES (?, ?, ?, ?, ?)
        """)
        q.addBindValue(self.combo_sta.currentText())
        q.addBindValue(self.combo_sem.currentData())
        q.addBindValue(self.combo_stu.currentData())
        q.addBindValue(self.txt_date.date().toString("yyyy-MM-dd"))
        q.addBindValue(amount)

        if not q.exec_():
            QMessageBox.critical(self, "DB Error", q.lastError().text())
            return

        self.model.select()
        self.clear_form()
        QMessageBox.information(self, "Success", "Payment registered successfully!")

    def delete_row(self, index):
        row = index.row()
        pid = self.model.index(row, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete Payment",
            f"Are you sure you want to delete Payment ID: {pid}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            q = QSqlQuery(self.db)
            q.prepare("DELETE FROM PAYMENTS WHERE Payment_Id = ?")
            q.addBindValue(pid)
            if not q.exec_():
                QMessageBox.warning(self, "Error", q.lastError().text())
            else:
                self.model.select()
                self.clear_form()

    def select_row(self, index):
        self.SelectedRow = index.row()
        self.id = self.model.index(self.SelectedRow, 0).data()

        q = QSqlQuery(self.db)
        q.prepare("SELECT Status, Sem_Id, Student_Id, Pay_Date, Amount FROM PAYMENTS WHERE Payment_Id = ?")
        q.addBindValue(self.id)
        q.exec_()

        if q.next():
            self.combo_sta.setCurrentText(q.value(0))
            self.combo_sem.setCurrentIndex(self.combo_sem.findData(q.value(1)))
            self.combo_stu.setCurrentIndex(self.combo_stu.findData(q.value(2)))
            self.txt_date.setDate(QDate.fromString(q.value(3), "yyyy-MM-dd"))
            self.txt_amoun.setText(str(q.value(4)))

    def update(self):
        if self.id is None:
            QMessageBox.warning(self, "Error", "Select a row first")
            return

        try:
            amount = float(self.txt_amoun.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be numeric")
            return

        q = QSqlQuery(self.db)
        q.prepare("""
            UPDATE PAYMENTS SET
                Status = ?,
                Sem_Id = ?,
                Student_Id = ?,
                Pay_Date = ?,
                Amount = ?
            WHERE Payment_Id = ?
        """)
        q.addBindValue(self.combo_sta.currentText())
        q.addBindValue(self.combo_sem.currentData())
        q.addBindValue(self.combo_stu.currentData())
        q.addBindValue(self.txt_date.date().toString("yyyy-MM-dd"))
        q.addBindValue(amount)
        q.addBindValue(self.id)

        if not q.exec_():
            QMessageBox.critical(self, "DB Error", q.lastError().text())
            return

        self.model.select()
        self.clear_form()
        QMessageBox.information(self, "Success", "Updated successfully!")

    def clear_form(self):
        self.txt_amoun.clear()
        self.combo_sta.setCurrentIndex(0)
        self.combo_sem.setCurrentIndex(0)
        self.combo_stu.setCurrentIndex(0)
        self.id = None
        self.SelectedRow = -1
