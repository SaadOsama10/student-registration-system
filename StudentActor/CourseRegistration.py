import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableView, QPushButton,QMessageBox,QFormLayout
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQueryModel
from PyQt5.QtCore import QDate



class ManageCourse(QWidget):
    def __init__(self, dp,id):
        super().__init__()
        self.dp = dp
        self.stuID=id

        self.model = QSqlQueryModel()

        sql = """
        SELECT 
    C.Course_Code,
    C.Course_Name,
    C.Course_Type,
    R.Room_Number,
    S.Time
FROM SECTIONS S
JOIN COURSES C ON S.Course_Id = C.Course_Id
JOIN CLASSROOMS R ON R.Room_Id = S.Room_Id
JOIN INSTRUCTORS I ON I.Instructor_Id = S.Instructor_Id
WHERE S.Sem_Id = (
    SELECT Sem_Id 
    FROM SEMESTERS 
    ORDER BY Start_Date DESC 
    LIMIT 1
)

        
                """
      
            
        self.model.setQuery(sql, QSqlDatabase.database("main_connection"))
        if not self.model.query().isActive():
            error = self.model.lastError().text()
            QMessageBox.critical(self, "Query Error", f"Failed to execute query:\n{error}")


        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setShowGrid(True)
        self.view.setGridStyle(Qt.DashLine)
        self.view.resizeColumnsToContents()
        self.view.setSortingEnabled(True)
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.clicked.connect(self.regist)

        self.model2 = QSqlTableModel(None, QSqlDatabase.database("main_connection"))
        self.model2.setTable("STUDENTS_REGISTRATIONS")
        self.model2.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model2.select()

        self.view2 = QTableView()
        self.view2.setModel(self.model2)
        self.view2.setShowGrid(True)
        self.view2.setGridStyle(Qt.DashLine)
        self.view2.setSortingEnabled(True)
        self.view2.horizontalHeader().setStretchLastSection(True)
        # setFilter() cannot bind values; int() guarantees a plain numeric id
        self.model2.setFilter(f"Student_Id = {int(self.stuID)}")
        self.view2.doubleClicked.connect(self.delete_row)


        self.setup_ui()

    def on_cell_clicked(self, index):
        pass

    def setup_ui(self):

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(20)
        
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.lbl_title = QLabel("Course Registration")
        self.lbl_title.setStyleSheet("color: #0B3C5D; font-size: 30px; font-weight: bold;")
        self.lbl_title.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.lbl_title)

        
        self.help_icon = QLabel()
        self.help_icon.setPixmap(QIcon("assets/note.png").pixmap(18, 18))
        self.help_text = QLabel(
            "Single-click a course to register • Double-click a registered course to remove"
        )
        self.help_text.setFont(QFont("Arial", 11))
        self.help_text.setStyleSheet("color: #0B3C5D;")
        self.form_layout.addRow(self.help_icon,self.help_text)
        self.main_layout.addLayout(self.form_layout)



        self.main_layout.addWidget(QLabel("Available Sections:"))
        self.main_layout.addWidget(self.view)

        self.main_layout.addWidget(QLabel("Student Registrations:"))
        self.main_layout.addWidget(self.view2)
        self.setLayout(self.main_layout)


        

    def regist(self,index):
      row = index.row()
      code = self.model.index(row, 0).data()
      cname = self.model.index(row, 1).data()
      
      reply = QMessageBox.question(
          self, 
          "Register Course",
        f"Are you sure you want to register for:\n\n"
        f"Course: {cname}\n"
        f"Code: {code}\n\n"
        f"Status will be: Pending",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No  # Default to "No" for safety

      )
      
      if reply == QMessageBox.No:
          return
      
      try:
          

          query = self.dp.query("""
             SELECT S.Section_Id
FROM SECTIONS S
JOIN COURSES C ON S.Course_Id = C.Course_Id
JOIN PAYMENTS P 
    ON S.Sem_Id = P.Sem_Id
    AND P.Student_Id = ?
    AND P.Status = 'Paid'
WHERE C.Course_Code = ?
AND S.Sem_Id = (
    SELECT Sem_Id FROM SEMESTERS
    ORDER BY Start_Date DESC
    LIMIT 1
)
          """, (self.stuID, code))
          if not query.next():
            QMessageBox.warning(self, "Error", "Section not found!\n You haven't pain your course!\n Contact with the admins")
            return    
          section_id = query.value(0)
          cdate = QDate.currentDate().toString("yyyy-MM-dd")
          
          check = self.dp.query(
              "SELECT Reg_Id FROM STUDENTS_REGISTRATIONS WHERE Student_Id = ? AND Section_Id = ?",
              (self.stuID, section_id),
          )

          if check.next():
              QMessageBox.warning(self, "Warning", "You already registered this course!")
              return
            
            
          insert_result = self.dp.run(
              "INSERT INTO STUDENTS_REGISTRATIONS (Student_Id, Section_Id, Status, Request_Date) "
              "VALUES (?, ?, 'Pending', ?)",
              (self.stuID, section_id, cdate),
          )
          
          if insert_result:
              QMessageBox.information(
                  self, 
                  "Success", 
                  f"Registered successfully!\n{cname}"
              )
              self.model2.select()
          else:
              QMessageBox.critical(self, "Error", "Registration failed!")
              
      except Exception as e:
          QMessageBox.critical(self, "Error", str(e))
        


    def delete_row(self, index):
        row = index.row()

        record_id = self.model2.index(row, 0).data()


        confirm = QMessageBox.question(
            self,
            "Delete Row",
            f"Are you sure you want to delete record ID: {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            
            # Students can only withdraw their own registrations
            self.dp.query(
                "DELETE FROM STUDENTS_REGISTRATIONS WHERE Reg_Id = ? AND Student_Id = ?",
                (record_id, self.stuID),
            )
            

            self.model2.select()  