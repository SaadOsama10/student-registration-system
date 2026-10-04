from PyQt5.QtWidgets import (
    QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
    QApplication, QTableWidget, QTableWidgetItem,QMessageBox,QTableView
)
from PyQt5.QtGui import QPixmap, QFont,QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel,QSqlQueryModel


import sys


class ManageTranscript(QWidget):
    def __init__(self,dp,id):
        super().__init__()
        
        self.dp = dp
        self.stuID=id
        
        
        self.name = ""
        self.number = ""
        self.email = ""
        self.tc = ""
        self.majorid = ""
        self.advisorid = ""
        self.major_name = ""
        self.adv_name = ""
        self.adv_email = ""
        self.cridets = 0
        self.path = self.getimage()
        
        


        self.setWindowTitle("Transcript")
        self.setGeometry(350, 0, 894, 700)
        self.setFixedSize(894, 700)
        self.setWindowIcon(QIcon("assets/icon.png"))

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.database()
        self.gpa=self.calculate_gpa()
        self.stu_class=self.get_student_class(self.cridets)
        
  



        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        logo = QLabel()
        pix = QPixmap("assets/image.png").scaled(
            110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(pix)
        

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)

        title1 = QLabel("FATİH SULTAN MEHMET VAKIF ÜNİVERSİTESİ")
        title1.setFont(QFont("Arial", 15, QFont.Bold))
        title1.setAlignment(Qt.AlignCenter)

        title2 = QLabel("Database Systems Course Project")
        title2.setFont(QFont("Arial", 12))
        title2.setAlignment(Qt.AlignCenter)

        center_layout.addWidget(title1)
        center_layout.addWidget(title2)

        header_layout.addWidget(logo, alignment=Qt.AlignLeft | Qt.AlignTop)
        header_layout.addWidget(center_widget, alignment=Qt.AlignCenter)
        header_layout.addWidget(QLabel()) 

        layout.addWidget(header_widget)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: black; margin-top: 4px; margin-bottom: 4px;")
        layout.addWidget(line)

        doc_title = QLabel("STUDENT TRANSCRIPT")
        doc_title.setFont(QFont("Arial", 14, QFont.Bold))
        doc_title.setAlignment(Qt.AlignCenter)
        doc_title.setStyleSheet("background-color: #E5E5E5; padding: 4px;")
        layout.addWidget(doc_title)

        
        info_frame = QFrame()
        info_frame.setStyleSheet("border: 1px solid #888; padding: 4px;")
        info_frame.setFixedHeight(150)

        info_layout = QHBoxLayout(info_frame)
        info_layout.setSpacing(10)

        # LEFT INFO
        left_info = QVBoxLayout()
        left_info.setSpacing(2)

        left_info.addLayout(self.make_info_row("Student Name:", f"{self.name}"))
        left_info.addLayout(self.make_info_row("TC Kimlik No:", f"{self.tc}"))
        left_info.addLayout(self.make_info_row("DepStudent No:", f"{self.number}"))
        left_info.addLayout(self.make_info_row("Major:", f"{self.major_name}"))
        left_info.addLayout(self.make_info_row("Class:",f"{self.stu_class}" ))

        # RIGHT INFO
        right_info = QVBoxLayout()
        right_info.setSpacing(2)

        right_info.addLayout(self.make_info_row("GPA:", "3.5"))
        right_info.addLayout(self.make_info_row("Student State:", "Active"))
        right_info.addLayout(self.make_info_row("Program Type:", "Bachelor's"))
        right_info.addLayout(self.make_info_row("Preparatory Success Status:", "Sucess"))

        photo = QLabel()
        pp = QPixmap(f"{self.path}").scaled(
            70, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        photo.setPixmap(pp)

        info_layout.addLayout(left_info)
        info_layout.addLayout(right_info)
        info_layout.addWidget(photo)

        layout.addWidget(info_frame)
        
        self.model = QSqlQueryModel()

        sql = f"""
                SELECT
                    
                    C.Course_Code,
                    C.Course_Name,
                    C.Course_Type,
                    sem.Year,
                    sem.Term,
                    C.Course_Credits,
                    G.Grade_Letter            
                FROM SECTIONS S
                JOIN COURSES C ON S.Course_Id = C.Course_Id
                JOIN SEMESTERS sem ON sem.Sem_Id = S.Sem_Id
                JOIN STUDENTS_REGISTRATIONS R ON R.Section_Id = S.Section_Id
                LEFT JOIN GRADES G ON R.Reg_Id = G.Reg_Id
                WHERE R.Student_Id= '{self.stuID}' And G.Grade_Letter IS NOT NULL
                ORDER BY S.Sem_Id ASC
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
        layout.addWidget(self.view)


       
       
        
        summary = QVBoxLayout()
        summary.setSpacing(2)

        s1 = QLabel(f"Total Credits : {self.cridets}/ 240")
        s1.setFont(QFont("Arial", 11))

        

        s3 = QLabel(f"A.G.N.O : {str(self.gpa)}")
        s3.setFont(QFont("Arial", 11))

        summary.addWidget(s1)
        summary.addWidget(s3)

        layout.addLayout(summary)

    def make_info_row(self, label, value):
        row = QHBoxLayout()

        lbl = QLabel(label)
        lbl.setFont(QFont("Arial", 10, QFont.Bold))
        lbl.setFixedWidth(150)

        val = QLabel(value)
        val.setFont(QFont("Arial", 10))

        row.addWidget(lbl)
        row.addWidget(val)
        row.addStretch()

        return row
    def database(self):
        sql = f"""SELECT Student_Name,Student_Number,Student_Email, TC_Kimlik, Major_Id, Advisor_Id 
                  FROM STUDENTS 
                  WHERE Student_Id = '{self.stuID}'"""
        
        query = self.dp._exec(sql)
        
        if query.next():
            self.name = query.value(0)
            self.number = query.value(1)
            self.email = query.value(2)
            self.tc = query.value(3)  # Convert to string for display
            self.majorid = query.value(4)
            self.advisorid = query.value(5)
        else:
            print("No student found with ID:", self.stuID)
            return
        
        # Fix: SELECT instead of SELECTE
        sql = f"""SELECT Major_Name
                  FROM MAJORS 
                  WHERE Major_Id = '{self.majorid}'"""
        
        query = self.dp._exec(sql)
        if query.next():
            self.major_name = query.value(0)
        else:
            self.major_name = "Unknown"
        # Fix: SELECT instead of SELECTE
        sql = f"""SELECT COALESCE(SUM(C.Course_Credits), 0)
                  FROM COURSES C
                  JOIN SECTIONS S
                  ON   S.Course_Id = C.Course_Id
                  JOIN STUDENTS_REGISTRATIONS R
                  ON   R.Section_Id=S.Section_Id
                  WHERE Student_Id = '{self.stuID}'
                  AND Status = 'Approved'
                  """
        
        query = self.dp._exec(sql)
        query.next()
        self.cridets = int(query.value(0))
        
        sql = f"""SELECT Instructor_Name,Instructor_Email
                  FROM INSTRUCTORS 
                  WHERE Instructor_Id = '{self.advisorid}'"""
        
        query = self.dp._exec(sql)
        if query.next():
            self.adv_name = query.value(0)
            self.adv_email = query.value(1)
        else:
            self.adv_name = "Unknown"
            self.adv_email = "Unknown"



    def get_student_class(self, credits):
      if credits < 60:
          return "1. class"
      elif credits < 120:
          return "2. class"
      elif credits < 180:
          return "3. class"
      else:
          return "4. class"
    def calculate_gpa(self):
      grade_points = {
          "AA": 4.0,
          "BA": 3.5,
          "BB": 3.0,
          "CB": 2.5,
          "CC": 2.0,
          "DC": 1.5,
          "DD": 1.0,
          "FD": 0.5,
          "FF": 0.0
      }

      sql = f"""
      SELECT C.Course_Credits, G.Grade_Letter
      FROM COURSES C
      JOIN SECTIONS S ON S.Course_Id = C.Course_Id
      JOIN STUDENTS_REGISTRATIONS R ON R.Section_Id = S.Section_Id
      LEFT JOIN GRADES G ON R.Reg_Id = G.Reg_Id
      WHERE R.Student_Id = '{self.stuID}'
      AND R.Status = 'Approved'
      """

      query = self.dp._exec(sql)

      total_points = 0.0
      total_credits = 0

      while query.next():
          credits = query.value(0)
          latter =str( query.value(1))

          if latter in grade_points:
              total_points += grade_points[latter] * credits
              total_credits += credits

      if total_credits == 0:
          return 0.00

      return round(total_points / total_credits, 2)
    def getimage (self):
      sql =f"""SELECT Photo_Path from Profile WHERE Student_Id = {self.stuID}""" 
      query = self.dp._exec(sql)
      if query.next() :
        return str(query.value(0))
      
      return "assets/working.png"  

      