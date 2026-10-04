from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import sys

app = QApplication(sys.argv)

# Connect to SQL Server
db = QSqlDatabase.addDatabase("QODBC")
db.setDatabaseName("Driver={SQL Server};Server=(local)\\SQLEXPRESS;Database=Students_Management;Trusted_Connection=yes;")

if not db.open():
    print("Failed to connect!")
    sys.exit(1)

# Load model
model = QSqlTableModel()
model.setTable("Students")
model.select()

# View
view = QTableView()
view.setModel(model)
view.show()

sys.exit(app.exec_())
