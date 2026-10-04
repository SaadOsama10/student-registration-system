from PyQt5.QtWidgets import QDialog , QLabel , QLineEdit , QPushButton, QMessageBox, QComboBox

class AddCourses(QDialog):
    def __init__(self, dp, model):
        super().__init__()
        self.dp = dp
        self.model = model

        self.setWindowTitle("Add Course")
        self.setGeometry(450, 250, 400, 450)

        self.Namelbl = QLabel("Course Name", self)
        self.Namelbl.setGeometry(20, 100, 200, 30)

        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 135, 350, 30)

        self.Cdtlbl = QLabel("Credits", self)
        self.Cdtlbl.setGeometry(20, 180, 200, 30)

        self.Cdttxt = QLineEdit(self)
        self.Cdttxt.setGeometry(20, 215, 350, 30)

        self.Inslbl = QLabel("Course Code", self)
        self.Inslbl.setGeometry(20, 260, 200, 30)

        self.Instxt = QLineEdit(self)
        self.Instxt.setGeometry(20, 295, 350, 30)

        self.typelbl = QLabel("Course Type", self)
        self.typelbl.setGeometry(20, 340, 200, 30)

        self.txt_t = QComboBox(self)
        self.txt_t.setGeometry(20, 375, 350, 30)
        self.txt_t.addItems(['Mandatory', 'Elective', 'Lab'])

        self.Savebtn = QPushButton("Add", self)
        self.Savebtn.setGeometry(120, 420, 150, 40)
        self.Savebtn.clicked.connect(self.register_action)

    def register_action(self):
        if not self.Instxt.text() or not self.Nametxt.text() or not self.Cdttxt.text():
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            code = self.Instxt.text()
            name = self.Nametxt.text()
            credit = self.Cdttxt.text()
            ctype = self.txt_t.currentText()

            self.dp.query(
                "INSERT INTO COURSES (Course_Code, Course_Name, Course_Credits, Course_Type) "
                "VALUES (?, ?, ?, ?)",
                (code, name, credit, ctype),
            )
            self.model.select()
            QMessageBox.information(self, "Success", "New Course registered successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_form(self):
        self.Cdttxt.clear()
        self.Nametxt.clear()
        self.Instxt.clear()
