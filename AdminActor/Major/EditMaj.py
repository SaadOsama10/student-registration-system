from PyQt5.QtWidgets import QDialog , QLabel , QLineEdit , QPushButton,QMessageBox,QComboBox

class EditMaj(QDialog):
    def __init__(self ,dp,model,row):
        super().__init__()
        self.dp=dp
        self.model = model 
        self.row=row
        self.id = self.model.index(self.row, 0).data()
        print("Selected ID =", self.id)



        self.setWindowTitle("Edit Major")
        self.setGeometry(450, 250, 400, 450)

        
        

        self.Namelbl = QLabel("Major Name" , self)
        self.Namelbl.setGeometry(20, 100, 200, 30)

        self.Nametxt = QLineEdit(self)
        self.Nametxt.setGeometry(20, 135, 350, 30)

        self.combo = QComboBox(self)
        
        sql = "SELECT Department_Id , Department_Name FROM DEPARTMENTS"
        query = self.dp._exec(sql)

        while query.next():
            id = query.value(0)
            name = query.value(1)
            self.combo.addItem(name, id)
        self.combo.setGeometry(20, 215, 350, 30)

        self.Savebtn = QPushButton("Edit", self)
        self.Savebtn.setGeometry(120, 350, 150, 40)
        self.Savebtn.setStyleSheet("background-color:#0B3C5D; color:white; font-size:18px;")
        self.Savebtn.clicked.connect(self.register_action)
        self.load_course_data()
        
    def load_course_data(self):
      
        query = self.dp.query(
            "SELECT Major_Name, Dept_Id FROM MAJORS WHERE Major_Id = ?",
            (self.id,),
        )
        if query.next():
          self.Nametxt.setText(query.value(0))
          self.combo.setCurrentText(str(query.value(1)))
    

    def register_action(self):
      
        name = self.Nametxt.text()
        id = self.combo.currentData()
        if not name :
          QMessageBox.warning(self, "Warning", "Please fill all fields")
          return



        
        try:
              

              self.dp.query(
                  "UPDATE MAJORS SET Major_Name = ?, Dept_Id = ? WHERE Major_Id = ?",
                  (name, id, self.id),
              )

              self.model.select() 

              QMessageBox.information(self, "Success", "Major edited successfully!")
              self.close()


        except Exception as e:
              QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

  