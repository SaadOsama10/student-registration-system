import sys, os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from deb_con import DatabaseConnect
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget,
    QHBoxLayout, QFrame, QLineEdit, QPushButton )
from PyQt5.QtWidgets import QApplication , QMainWindow ,QLabel ,QWidget, QHBoxLayout,QFrame,QLineEdit,QPushButton,QMessageBox
from PyQt5.QtGui import QIcon,QFont,QPixmap
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from ProfessorActor.PDashboard import ProfessorDashboard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.dp = DatabaseConnect()
        self.dp.initialize()


        self.setWindowTitle("Log in page")
        self.setGeometry(350, 200, 1200, 680)
        self.setWindowIcon(QIcon("assets/icon.png"))

        # Logo
        self.lblimage = QLabel(self)
        self.lblimage.setGeometry(450, 50, 280, 120)
        pix = QPixmap("assets/image.png")
        self.lblimage.setPixmap(pix)
        self.lblimage.setScaledContents(True)

        self.createDivider("Professor", 100, 200, 1000)

        # Username + password fields
        self.lblsn = QLabel("Professor Username", self)
        self.lesn = QLineEdit(self)

        self.lblp = QLabel("Password", self)
        self.lep = QLineEdit(self)
        self.lep.setEchoMode(QLineEdit.Password)

        self.blogin = QPushButton("Log in", self)
        self.back = QPushButton(self)
        self.back.setIcon(QIcon("assets/back.png"))
        self.back.setIconSize(QSize(30, 30))

        self.blogin.clicked.connect(self.login)
        self.back.clicked.connect(self.reback)


        self.initUI()


    # ------------ LOGIN FUNCTION ------------
    def login(self):
        username = self.lesn.text().strip()
        password = self.lep.text().strip()

        if not username or not password:  
            QMessageBox.warning(self,"Login Failed","Please enter both username and password.")
            return


        try:
            user_id = self.dp.authenticate(username, password, "Instructor")

            if user_id is None:
                QMessageBox.warning(self, "Login Failed", 
                                  "Invalid username, password, or role.\nPlease try again.")
                return
            else:
                query = self.dp.query(
                    "SELECT Instructor_Id FROM INSTRUCTORS WHERE User_Id = ?",
                    (user_id,),
                )
                query.next()
                instructor_id = query.value(0) 
                QMessageBox.information(self, "Success","Login successful.")
                self.dashboard_window = ProfessorDashboard(instructor_id,self.dp)
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

    # ------------ GUI LAYOUT ------------
    def initUI(self):
        self.lblsn.setFont(QFont("Arial", 20, QFont.Bold))
        self.lblp.setFont(QFont("Arial", 20, QFont.Bold))

        self.lblsn.setGeometry(350, 250, 500, 100)
        self.lesn.setGeometry(350, 350, 500, 40)

        self.lblp.setGeometry(350, 400, 500, 100)
        self.lep.setGeometry(350, 500, 500, 40)

        self.blogin.setGeometry(1000, 550, 150, 100)
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


    def mousePressEvent(self, event):
        print("Clicked at:", event.x(), event.y())

    def createDivider(self, text, x, y, width):
        container = QWidget(self)
        container.setGeometry(x, y, width, 40)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        lineLeft = QFrame()
        lineLeft.setFrameShape(QFrame.HLine)
        lineLeft.setStyleSheet("color: lightgray;")

        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 14))
        lbl.setStyleSheet("color: #196297; padding: 150px;")

        lineRight = QFrame()
        lineRight.setFrameShape(QFrame.HLine)
        lineRight.setStyleSheet("color: lightgray;")

        layout.addWidget(lineLeft)
        layout.addWidget(lbl)
        layout.addWidget(lineRight)

        return container


# ------------ PROGRAM ENTRY POINT ------------
def main():
    db = DatabaseConnect()
    if not db.initialize():
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
