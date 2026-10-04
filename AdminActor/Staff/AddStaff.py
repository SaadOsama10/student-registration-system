from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox

class AddStaff(QDialog):
    def __init__(self, dp, model):
        super().__init__()
        self.dp = dp
        self.model = model

        self.setWindowTitle("Add Instructor")
        self.setGeometry(450, 250, 400, 600)

        self.Namelbl = QLabel("Instructor Name", self)
        self.Namelbl.setGeometry(20, 60, 200, 30)
        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 90, 350, 30)

        self.Emaillbl = QLabel("Instructor Email", self)
        self.Emaillbl.setGeometry(20, 130, 200, 30)
        self.Emailtxt = QLineEdit(self)
        self.Emailtxt.setGeometry(20, 160, 350, 30)

        self.Didlbl = QLabel("Department", self)
        self.Didlbl.setGeometry(20, 200, 200, 30)
        self.Depcombo = QComboBox(self)
        self.Depcombo.setGeometry(20, 230, 350, 30)

        sql = "SELECT Department_Id, Department_Name FROM DEPARTMENTS"
        query = self.dp._exec(sql)
        while query.next():
            self.Depcombo.addItem(query.value(1), query.value(0))

        self.Uidlbl = QLabel("User Account", self)
        self.Uidlbl.setGeometry(20, 270, 200, 30)
        self.Usercombo = QComboBox(self)
        self.Usercombo.setGeometry(20, 300, 350, 30)

        sql = "SELECT User_Id, Username FROM USERS WHERE Role = 'Instructor'"
        query = self.dp._exec(sql)
        while query.next():
            self.Usercombo.addItem(query.value(1), query.value(0))

        self.Savebtn = QPushButton("Add", self)
        self.Savebtn.setGeometry(120, 500, 150, 40)
        self.Savebtn.setStyleSheet("background-color:#0B3C5D; color:white; font-size:18px;")
        self.Savebtn.clicked.connect(self.register_action)

    def register_action(self):
        if not self.Nametxt.text() or not self.Emailtxt.text():
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            name = self.Nametxt.text()
            email = self.Emailtxt.text()
            did = self.Depcombo.currentData()
            uid = self.Usercombo.currentData()

            self.dp.query(
                "INSERT INTO INSTRUCTORS (Instructor_Name, Instructor_Email, Department_Id, User_Id) "
                "VALUES (?, ?, ?, ?)",
                (name, email, did, uid),
            )
            self.model.select()
            QMessageBox.information(self, "Success", "New Instructor registered successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
