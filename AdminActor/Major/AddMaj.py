from PyQt5.QtWidgets import QDialog , QLabel , QLineEdit , QPushButton,QMessageBox,QComboBox

class AddMaj(QDialog):
    def __init__(self,dp,model):
        super().__init__()
        self.dp=dp
        self.model = model 

        self.setWindowTitle("Add MAJORS")
        self.setGeometry(450, 250, 400, 450)

        
        self.Namelbl = QLabel("MAJORS Name" , self)
        self.Namelbl.setGeometry(20, 100, 200, 30)

        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 135, 350, 30)

        self.idlbl = QLabel("Dept_Id" , self)
        self.idlbl.setGeometry(20, 180, 200, 30)

        self.combo = QComboBox(self)
        
        sql = "SELECT Department_Id , Department_Name FROM DEPARTMENTS"
        query = self.dp._exec(sql)

        while query.next():
            id = query.value(0)
            name = query.value(1)
            self.combo.addItem(name, id)
        self.combo.setGeometry(20, 215, 350, 30)


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
              id = self.combo.currentData()
              

              sql = f"""
              INSERT INTO MAJORS (Major_Name, Dept_Id)
              VALUES ('{name}', '{id}')
              """

              self.dp._exec(sql)

              self.model.select() 

              QMessageBox.information(self, "Success", "New Major registered successfully!")
              self.close()

        except Exception as e:
              QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

