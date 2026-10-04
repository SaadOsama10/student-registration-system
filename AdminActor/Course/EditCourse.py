from PyQt5.QtWidgets import QDialog , QLabel , QLineEdit , QPushButton, QMessageBox, QComboBox

class EditCourses(QDialog):
    def __init__(self, dp, model, row):
        super().__init__()
        self.dp = dp
        self.model = model
        self.row = row
        self.id = self.model.index(self.row, 0).data()

        self.setWindowTitle("Edit Course")
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

        self.Savebtn = QPushButton("Edit", self)
        self.Savebtn.setGeometry(120, 420, 150, 40)
        self.Savebtn.clicked.connect(self.register_action)

        self.load_course_data()

    def load_course_data(self):
        query = self.dp.query(
            "SELECT Course_Code, Course_Name, Course_Credits, Course_Type FROM COURSES WHERE Course_Id = ?",
            (self.id,),
        )

        if query.next():
            self.Instxt.setText(query.value(0))
            self.Nametxt.setText(query.value(1))
            self.Cdttxt.setText(str(query.value(2)))
            course_type = query.value(3)
            index = self.txt_t.findText(course_type)
            if index >= 0:
                self.txt_t.setCurrentIndex(index)

    def register_action(self):
        code = self.Instxt.text()
        name = self.Nametxt.text()
        credit = self.Cdttxt.text()
        ctype = self.txt_t.currentText()

        if not code or not name or not credit:
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
            self.dp.query(
                "UPDATE COURSES SET Course_Code = ?, Course_Name = ?, Course_Credits = ?, Course_Type = ? "
                "WHERE Course_Id = ?",
                (code, name, credit, ctype, self.id),
            )
            self.model.select()
            QMessageBox.information(self, "Success", "Course edited successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
