from PyQt5.QtWidgets import QDialog , QLabel , QLineEdit , QPushButton,QMessageBox,QComboBox

class AddDep(QDialog):
    def __init__(self,dp,model):
        super().__init__()
        self.dp=dp
        self.model = model 

        self.setWindowTitle("Add DEPARTMENTS")
        self.setGeometry(450, 250, 400, 450)

        
        self.Namelbl = QLabel("DEPARTMENTS Name" , self)
        self.Namelbl.setGeometry(20, 100, 200, 30)

        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 135, 350, 30)

        self.hidlbl = QLabel("Head Instructor Id" , self)
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

        self.Savebtn = QPushButton("Add", self)
        self.Savebtn.setGeometry(120, 350, 150, 40)
        self.Savebtn.setStyleSheet("background-color:#0B3C5D; color:white; font-size:18px;")
        self.Savebtn.clicked.connect(self.register_action)

    def register_action(self):
        

        if  not self.Nametxt.text() :
            QMessageBox.warning(self, "Warning", "Please fill all fields")
            return

        try:
              name = self.Nametxt.text()
              hid = self.head_combo.currentData()
              
              if hid is None:
                    hid = "NULL"      # SQL null (no quotes)
              
              


              sql = f"""
              INSERT INTO DEPARTMENTS (Department_Name , Head_Instructor_Id)
              VALUES ('{name}', {hid})
              """

              self.dp._exec(sql)

              self.model.select() 

              QMessageBox.information(self, "Success", "New Department registered successfully!")
              self.close()

        except Exception as e:
              QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    