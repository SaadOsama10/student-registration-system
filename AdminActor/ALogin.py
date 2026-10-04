import sys 
from PyQt5.QtWidgets import QApplication , QMainWindow ,QLabel ,QWidget, QHBoxLayout,QFrame,QLineEdit,QPushButton,QMessageBox
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtCore import Qt,QSize

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from AdminActor.ADashboard import Dashboard

sys.path.append(str(Path(__file__).parent.parent))
from deb_con import DatabaseConnect
from PyQt5.QtSql import QSqlQuery, QSqlDatabase


class MainWindow(QMainWindow) :
  def __init__(self):
    super().__init__()
    
    self.dp = DatabaseConnect()
    self.dp.initialize()

    self.setWindowTitle("Log in page")
    self.setGeometry(350, 200,1200 , 680)
    self.setWindowIcon(QIcon("assets/icon.png"))


    self.lblimage = QLabel(self)
    self.lblimage.setGeometry(450, 50,280,120)
    self.image=QPixmap("assets/image.png")
    self.lblimage.setPixmap(self.image)
    self.lblimage.setScaledContents(True)

    self.createDivider("Admin", 100, 200, 1000)
    self.lblsn = QLabel("Admin Username",self)
    self.lesn = QLineEdit(self)
    self.lblp = QLabel("Password",self)    
    self.lep = QLineEdit(self)    
    self.blogin = QPushButton("Log in",self)
    self.back = QPushButton(self)
    self.back.setIcon(QIcon("assets/back.png"))
    self.back.setIconSize(QSize(30, 30))


    
    self.blogin.clicked.connect(self.login)
    self.back.clicked.connect(self.reback)
    self.initUI()

  def login (self):
        username = self.lesn.text().strip()
        password = self.lep.text().strip()

        if not username or not password:  
            QMessageBox.warning(self,"Login Failed","Please enter both username and password.")
            return


        try:
            query = self.dp._exec(f"""
                SELECT User_Id
                FROM USERS
                WHERE Username = '{username}' AND Password = '{password}' AND role = 'Admin'
            """)

            if not query.next():
                QMessageBox.warning(self, "Login Failed", 
                                  "Invalid username, password, or role.\nPlease try again.")
                return
            else:
                user_id = query.value(0)
                
                QMessageBox.information(self, "Success","Login successful.")
                self.dashboard_window = Dashboard(self.dp)
                self.dashboard_window.show()
                self.close()
                
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error: {str(e)}")
            print(f"Database error: {e}")
            return

   
  def reback (self):
      from Rule import MainLoginScreen
      self.rule = MainLoginScreen()
      self.rule.show()
      self.close()
       
  def open_dashboard(self):
    
        self.dashboard_window = Dashboard(self.dp)
        self.dashboard_window.show()
        self.close()
  
     

  def login_btn_clicked(self):
       self.open_dashboard()
       



  def initUI(self):
    self.lblp.setFont(QFont("Arial", 20, QFont.Bold)) 
    self.lblsn.setFont(QFont("Arial", 20, QFont.Bold))

    self.lblsn.setGeometry(350, 250,500,100)
    self.lesn.setGeometry(350, 350 ,500,40)
    self.lblp.setGeometry(350, 400,500,100)
    self.lep.setGeometry(350, 500 ,500,40)
    self.blogin.setGeometry(1000, 550,150,100)
    self.back.setGeometry(20, 10,100,100)


    self.lblsn.setStyleSheet("color: #196297; font-size: 30px; font-weight: bold;")
    self.lesn.setStyleSheet("font-size: 25px;")
    self.lblp.setStyleSheet("color: #196297; font-size: 30px; font-weight: bold;")
    self.lep.setStyleSheet("font-size: 25px;")
    self.blogin.setStyleSheet(
    "font-size: 30px;"
    "font-family: Arial;"
    "padding: 5px 20px;"
    "margin: 10px;"
    "border: 3px solid #196297;"
    "border-radius: 15px;"
)
    self.back.setStyleSheet(
    "font-size: 20px;"
    "font-family: Arial;"
    "padding: 5px 20px;"
    "margin: 10px;"
    "color: white;"
    
    "background-color: transparent"    
)

     
    
  
  
  def createDivider(self, text, x, y, width):
        container = QWidget(self)
        container.setGeometry(x, y, width, 40)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left line
        lineLeft = QFrame()
        lineLeft.setFrameShape(QFrame.HLine)
        lineLeft.setFrameShadow(QFrame.Plain)
        lineLeft.setStyleSheet("color: lightgray;")

        # Title
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 14))
        lbl.setStyleSheet("color: #196297; padding: 150px;")

        # Right line
        lineRight = QFrame()
        lineRight.setFrameShape(QFrame.HLine)
        lineRight.setFrameShadow(QFrame.Plain)
        lineRight.setStyleSheet("color: lightgray;")

        layout.addWidget(lineLeft)
        layout.addWidget(lbl)
        layout.addWidget(lineRight)

        return container 





    
    

 


def main():
  app=QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
if __name__=="__main__":
  main()  
