from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
from StudentActor.Transcript import ManageTranscript

class StudentMain(QWidget):
    def __init__(self, dp, id):
        super().__init__()
        




                
        self.dp = dp
        self.stuID = id
        
        self.name = ""
        self.number = ""
        self.email = ""
        self.tc = ""
        self.majorid = ""
        self.advisorid = ""
        self.major_name = ""
        self.adv_name = ""
        self.adv_email = ""
        
        self.transcript = ManageTranscript(self.dp, self.stuID)
        self.gpa = self.transcript.gpa
        self.credits = self.transcript.cridets
        self.stu_class = self.transcript.stu_class
        self.path=self.getimage()
        

        
        self.database()
        
        self.setWindowTitle("Student Dashboard")
        self.setGeometry(350, 0, 894, 700)
        self.setFixedSize(894, 700)

        self.build_ui()

    def make_card(self, icon, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #a8c1d8;
                border-radius: 8px;
            }
        """)
        card.setFixedSize(260, 110)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        ic = QLabel()
        ic_pic = QPixmap(f"assets/{icon}").scaled(
            32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        ic.setPixmap(ic_pic)
        ic.setAlignment(Qt.AlignCenter)
        ic.setFixedWidth(50)

        txt = QVBoxLayout()
        txt.setSpacing(3)

        t_title = QLabel(title)
        t_title.setFont(QFont("Arial", 11))
        t_title.setStyleSheet("color: #1a4b73;")

        t_val = QLabel(value)
        t_val.setFont(QFont("Arial", 16, QFont.Bold))
        t_val.setStyleSheet("color: #0d3c75;")

        txt.addWidget(t_title)
        txt.addWidget(t_val)

        layout.addWidget(ic)
        layout.addLayout(txt)

        return card

    def build_ui(self): 
      
        main = QHBoxLayout(self)
        left = QVBoxLayout()

        img = QLabel()
        pix = QPixmap(f"{self.path}").scaled(120, 120, Qt.KeepAspectRatio)
        img.setPixmap(pix)
        img.setAlignment(Qt.AlignCenter)
        left.addWidget(img)

        info_box = QFrame()
        info_box.setStyleSheet("""
            background-color: #f3f6fc;
            border: 1px solid #0B3C5D;
            border-radius: 4px;
        """)
        info_layout = QVBoxLayout(info_box)

        def make_row(label, value):
            row = QHBoxLayout()

            lbl = QLabel(label)
            lbl.setFont(QFont("Arial", 13, QFont.Bold))
            lbl.setStyleSheet("color: #0B3C5D;")

            val = QLabel(value)
            val.setFont(QFont("Arial", 13))
            val.setStyleSheet("color:#0B3C5D;")

            row.addWidget(lbl)
            row.addWidget(val)
            return row
        
        r1 = make_row("Student Name:", f"{self.name}")
        info_layout.addLayout(r1)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line1)

        r2 = make_row("TC Kimlik No:", f"{self.tc}")
        info_layout.addLayout(r2)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line2)

        r3 = make_row("Major:", f"{self.major_name}")
        info_layout.addLayout(r3)

        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line3)

        r4 = make_row("Student Number:", f"{self.number}")
        info_layout.addLayout(r4)

        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line4)

        r5 = make_row("E-Posta:", f"{self.email}")
        info_layout.addLayout(r5)

        line5 = QFrame()
        line5.setFrameShape(QFrame.HLine)
        line5.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line5)

        r6 = make_row("Advisor Name:", f"{self.adv_name}")
        info_layout.addLayout(r6)

        line6 = QFrame()
        line6.setFrameShape(QFrame.HLine)
        line6.setStyleSheet("color:#0B3C5D;")
        info_layout.addWidget(line6)

        r7 = make_row("Advisor E-Posta:", f"{self.adv_email}")
        info_layout.addLayout(r7)

        left.addWidget(info_box)
        
        left.addSpacing(20)
        
        gpa_row = QHBoxLayout()
        
        gpa2 = self.make_card("tgpa.png", "Total GPA", str(self.gpa))
        
        gpa2.setFixedSize(250, 110)
        
        gpa_row.addWidget(gpa2)
        
        left.addLayout(gpa_row)
        
        left.addStretch(1)

        right = QVBoxLayout()
        right.setContentsMargins(0, 120, 0, 0)
        
        card1 = self.make_card("academic.png", "Year information", self.stu_class)
        right.addWidget(card1)

        

        card3 = self.make_card("totall.png", "Total Credits", f"{self.credits}/250")
        right.addWidget(card3)

        right.addStretch(1)

        main.addLayout(left)
        main.addLayout(right)
        
    def database(self):
        # Fix: SELECT instead of SELECTE
        sql = f"""SELECT Student_Name,Student_Number,Student_Email, TC_Kimlik, Major_Id, Advisor_Id 
                  FROM STUDENTS 
                  WHERE Student_Id = '{self.stuID}'"""
        
        query = self.dp._exec(sql)
        
        # You need to move to the first result
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
            

    def getimage (self):
      sql =f"""SELECT Photo_Path from Profile WHERE Student_Id = {self.stuID}""" 
      query = self.dp._exec(sql)
      if query.next() :
        return str(query.value(0))
      
      return "assets/working.png"  
