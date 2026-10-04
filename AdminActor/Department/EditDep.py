from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox

class EditDep(QDialog):
    def __init__(self, dp, model, row):
        super().__init__()
        self.dp = dp
        self.model = model
        self.row = row
        self.id = self.model.index(self.row, 0).data()

        self.setWindowTitle("Edit DEPARTMENT")
        self.setGeometry(450, 250, 400, 450)

        self.Namelbl = QLabel("DEPARTMENT Name", self)
        self.Namelbl.setGeometry(20, 100, 200, 30)

        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 135, 350, 30)

        self.hidlbl = QLabel("Head Instructor Id", self)
        self.hidlbl.setGeometry(20, 180, 200, 30)

        self.head_combo = QComboBox(self)
        self.head_combo.addItem("None", None)

        sql = "SELECT Instructor_Id, Instructor_Name FROM INSTRUCTORS"
        query = self.dp._exec(sql)
        while query.next():
            inst_id = query.value(0)
            inst_name = query.value(1)
            self.head_combo.addItem(inst_name, inst_id)

        self.head_combo.setGeometry(20, 215, 350, 30)

        self.Savebtn = QPushButton("Edit", self)
        self.Savebtn.setGeometry(120, 350, 150, 40)
        self.Savebtn.setStyleSheet("background-color:#0B3C5D; color:white; font-size:18px;")
        self.Savebtn.clicked.connect(self.register_action)

        self.load_department_data()

    def load_department_data(self):
        query = self.dp.query(
            "SELECT Department_Name, Head_Instructor_Id FROM DEPARTMENTS WHERE Department_Id = ?",
            (self.id,),
        )

        if query.next():
            self.Nametxt.setText(query.value(0))

            head_id = query.value(1)
            if head_id is None:
                self.head_combo.setCurrentIndex(0)
            else:
                index = self.head_combo.findData(head_id)
                if index >= 0:
                    self.head_combo.setCurrentIndex(index)

    def register_action(self):
        name = self.Nametxt.text()
        head = self.head_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return


        try:
            self.dp.query(
                "UPDATE DEPARTMENTS SET Department_Name = ?, Head_Instructor_Id = ? WHERE Department_Id = ?",
                (name, head, self.id),  # head is None when no head is selected -> NULL
            )
            self.model.select()
            QMessageBox.information(self, "Success", "Department updated successfully!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
