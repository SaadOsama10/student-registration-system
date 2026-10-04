from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

class EditStudents(QDialog):
    def __init__(self, dp, model, row):
        super().__init__()
        self.dp = dp
        self.model = model
        self.row = row
        self.id = self.model.index(self.row, 0).data()

        self.setWindowTitle("Edit Student")
        self.setGeometry(450, 250, 400, 700)

        self.Namelbl = QLabel("Student Name", self)
        self.Namelbl.setGeometry(20, 20, 200, 30)
        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 55, 350, 30)

        self.Numberlbl = QLabel("Student Number", self)
        self.Numberlbl.setGeometry(20, 100, 200, 30)
        self.Numbertxt = QLineEdit(self)
        self.Numbertxt.setGeometry(20, 135, 350, 30)

        self.Emaillbl = QLabel("Student Email", self)
        self.Emaillbl.setGeometry(20, 180, 200, 30)
        self.Emailtxt = QLineEdit(self)
        self.Emailtxt.setGeometry(20, 215, 350, 30)

        self.TClbl = QLabel("TC_Kimlik", self)
        self.TClbl.setGeometry(20, 260, 200, 30)
        self.TCtxt = QLineEdit(self)
        self.TCtxt.setGeometry(20, 295, 350, 30)

        self.Userlbl = QLabel("User Account", self)
        self.Userlbl.setGeometry(20, 340, 200, 30)
        self.Usercombo = QComboBox(self)
        self.Usercombo.setGeometry(20, 375, 350, 30)

        sql = "SELECT User_Id, Username FROM USERS WHERE Role = 'Student'"
        query = self.dp._exec(sql)
        while query.next():
            self.Usercombo.addItem(query.value(1), query.value(0))

        self.Majorlbl = QLabel("Major", self)
        self.Majorlbl.setGeometry(20, 420, 200, 30)
        self.Majorcombo = QComboBox(self)
        self.Majorcombo.setGeometry(20, 455, 350, 30)

        sql = "SELECT Major_Id, Major_Name FROM MAJORS"
        query = self.dp._exec(sql)
        while query.next():
            self.Majorcombo.addItem(query.value(1), query.value(0))

        self.Advisorlbl = QLabel("Advisor", self)
        self.Advisorlbl.setGeometry(20, 500, 200, 30)
        self.Advisorcombo = QComboBox(self)
        self.Advisorcombo.setGeometry(20, 535, 350, 30)

        sql = "SELECT Instructor_Id, Instructor_Name FROM INSTRUCTORS"
        query = self.dp._exec(sql)
        while query.next():
            self.Advisorcombo.addItem(query.value(1), query.value(0))

        self.Savebtn = QPushButton("Edit", self)
        self.Savebtn.setGeometry(120, 590, 150, 40)
        self.Savebtn.setStyleSheet("background-color:#0B3C5D; color:white; font-size:18px;")
        self.Savebtn.clicked.connect(self.register_action)

        self.load_student_data()

    def load_student_data(self):
        query = self.dp.query(
            "SELECT Student_Name, Student_Number, Student_Email, TC_Kimlik, User_Id, Major_Id, Advisor_Id "
            "FROM STUDENTS WHERE Student_Id = ?",
            (self.id,),
        )

        if query.next():
            self.Nametxt.setText(query.value(0))
            self.Numbertxt.setText(query.value(1))
            self.Emailtxt.setText(query.value(2))
            self.TCtxt.setText(str(query.value(3)))

            user_id = query.value(4)
            major_id = query.value(5)
            advisor_id = query.value(6)

            ui = self.Usercombo.findData(user_id)
            if ui >= 0:
                self.Usercombo.setCurrentIndex(ui)

            mi = self.Majorcombo.findData(major_id)
            if mi >= 0:
                self.Majorcombo.setCurrentIndex(mi)

            ai = self.Advisorcombo.findData(advisor_id)
            if ai >= 0:
                self.Advisorcombo.setCurrentIndex(ai)

    def register_action(self):
        name = self.Nametxt.text()
        number = self.Numbertxt.text()
        email = self.Emailtxt.text()
        tc = self.TCtxt.text()
        user_id = self.Usercombo.currentData()
        major_id = self.Majorcombo.currentData()
        advisor_id = self.Advisorcombo.currentData()

        if not name or not number or not email or not tc:
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            self.dp.query(
                "UPDATE STUDENTS SET Student_Name = ?, Student_Number = ?, Student_Email = ?, TC_Kimlik = ?, "
                "User_Id = ?, Major_Id = ?, Advisor_Id = ? WHERE Student_Id = ?",
                (name, number, email, tc, user_id, major_id, advisor_id, self.id),
            )
            self.model.select()
            QMessageBox.information(self, "Success", "Student updated successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
