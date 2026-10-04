from PyQt5.QtWidgets import QWidget, QLabel, QTableView,QVBoxLayout,QPushButton, QHBoxLayout,QTableWidget, QTableWidgetItem, QHeaderView , QMessageBox
from PyQt5.QtGui import QFont
from AdminActor.Student.AddStudent import AddStu
from AdminActor.Student.EditStudent import EditStudents
from PyQt5.QtCore import Qt

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQuery


class ManageStu(QWidget):
    def __init__(self,dp):
        super().__init__()
        self.dp=dp

      

        self.model = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model.setTable("STUDENTS")  
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


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.setContentsMargins(30, 30, 30, 30)
        self.btn_layout.setSpacing(30)


        self.title = QLabel("Manage STUDENTS" , self)  
        self.title.setFont(QFont("Arial",24,QFont.Bold))
        self.title.setStyleSheet("color :#0B3C5D;")



        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.view)



        

        button_style = """
                QPushButton {
                    background-color: #0B3C5D;
                    color: white;
                    font-size: 18px;
                    border-radius: 6px;
                    padding: 5px;
                }

                QPushButton:hover {
                     background-color: #0d4f7d;
                }
            """

        self.AddBtn = QPushButton("Add",self)
        self.AddBtn.setStyleSheet(button_style)
        self.AddBtn.clicked.connect(self.OpenAdd)
        self.btn_layout.addWidget(self.AddBtn)


        self.EditBtn = QPushButton("Edit",self)
        self.EditBtn.setStyleSheet(button_style)
        self.EditBtn.clicked.connect(lambda: self.OpenEdit(self.view.currentIndex()))
        self.btn_layout.addWidget(self.EditBtn)



        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)




    def OpenAdd(self):
      self.add_form = AddStu(self.dp,self.model)   
      self.add_form.show()

        
    def OpenEdit(self,index):
        SelectedRow = index.row()
        if SelectedRow == -1:
            QMessageBox.warning(self,"Error","No row selected!")
            return 
        self.add_form = EditStudents(self.dp,self.model,SelectedRow)   
        self.add_form.exec_()


    def delete_row(self, index):
        row = index.row()
        record_id = self.model.index(row, 0).data()

        confirm = QMessageBox.question(
            self,
            "Delete Student",
            f"Are you sure you want to delete student ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            query = QSqlQuery()
            ok = query.exec_(f"DELETE FROM STUDENTS WHERE Student_Id = {record_id}")

            if not ok:
                QMessageBox.warning(
                    self,
                    "Delete Error",
                    "Cannot delete this student.\nHe has related records (registrations, grades, etc)."
                )
            else:
                QMessageBox.information(
                    self,
                    "Success",
                    "Student deleted successfully."
                )

            self.model.select()
