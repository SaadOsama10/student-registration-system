from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QFileDialog, QMessageBox, QDateEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDate, QLocale


class StudentProfileGUI(QWidget):
    def __init__(self, dp, id):
        super().__init__()

        self.dp = dp
        self.stuID = id

        self.createProfile()

        self.setWindowTitle("Student Profile")
        self.setGeometry(350, 0, 894, 700)
        self.setFixedSize(894, 700)

        self.build_ui()
        self.load_profile()

    # ================= UI =================
    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(15)

        title = QLabel("Student Profile")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(60)
        main_layout.addLayout(middle_layout)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)
        middle_layout.addLayout(form_layout, stretch=3)

        self.input_phone = self.make_field(form_layout, "Phone:")
        self.input_address = self.make_field(form_layout, "Address:")
        self.input_birth = self.make_date_field(form_layout, "Birth Date:")
        self.input_gender = self.make_field(form_layout, "Gender:")
        self.input_nationality = self.make_field(form_layout, "Nationality:")
        self.input_photo = self.make_field(form_layout, "Photo Path:")

        photo_layout = QVBoxLayout()
        photo_layout.setAlignment(Qt.AlignTop)
        middle_layout.addLayout(photo_layout, stretch=2)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(220, 260)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            border: 2px solid #888;
            background: #f2f2f2;
        """)
        photo_layout.addWidget(self.photo_label)

        btn_choose = QPushButton("Choose Photo")
        btn_choose.setFixedSize(220, 40)
        btn_choose.clicked.connect(self.choose_photo)
        photo_layout.addWidget(btn_choose)

        bottom_layout = QHBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        btn_add = QPushButton("Add Profile")
        btn_add.setFont(QFont("Arial", 16, QFont.Bold))
        btn_add.setFixedHeight(60)
        btn_add.clicked.connect(self.add_profile)

        btn_delete = QPushButton("Delete")
        btn_delete.setFont(QFont("Arial", 16, QFont.Bold))
        btn_delete.setFixedHeight(60)
        btn_delete.clicked.connect(self.delete_profile)

        bottom_layout.addWidget(btn_add)
        bottom_layout.addWidget(btn_delete)

    def make_field(self, layout, text):
        row = QHBoxLayout()

        label = QLabel(text)
        label.setFixedWidth(180)
        label.setFont(QFont("Arial", 12, QFont.Bold))

        field = QLineEdit()
        field.setFixedHeight(34)

        row.addWidget(label)
        row.addWidget(field)
        layout.addLayout(row)
        return field

    def make_date_field(self, layout, text):
        row = QHBoxLayout()

        label = QLabel(text)
        label.setFixedWidth(180)
        label.setFont(QFont("Arial", 12, QFont.Bold))

        field = QDateEdit()
        field.setCalendarPopup(True)
        field.setDisplayFormat("yyyy-MM-dd")
        field.setLocale(QLocale(QLocale.English))
        field.setDate(QDate(2000, 1, 1))
        field.setMinimumDate(QDate(1900, 1, 1))
        field.setMaximumDate(QDate.currentDate())
        field.setFixedHeight(34)

        row.addWidget(label)
        row.addWidget(field)
        layout.addLayout(row)
        return field

    # ================= Actions =================
    def choose_photo(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Choose Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file:
            pix = QPixmap(file)
            if not pix.isNull():
                self.photo_label.setPixmap(
                    pix.scaled(220, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.input_photo.setText(file)

    def add_profile(self):
        phone = self.input_phone.text().strip()
        address = self.input_address.text().strip()
        birth = self.input_birth.date().toString("yyyy-MM-dd")
        gender = self.input_gender.text().strip()
        nationality = self.input_nationality.text().strip()
        photo = self.input_photo.text().strip()

        if not phone or not address:
            QMessageBox.warning(self, "Warning", "Phone and Address are required")
            return

        check = self.dp.query("SELECT 1 FROM PROFILE WHERE Student_Id = ?", (self.stuID,))
        if check.next():
            QMessageBox.warning(self, "Warning", "Profile already exists!")
            return

        try:
            self.dp.query(
                "INSERT INTO PROFILE (Student_Id, Phone, Address, Birth_Date, Gender, Nationality, Photo_Path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.stuID, phone, address, birth, gender, nationality, photo),
            )
            QMessageBox.information(self, "Success", "Profile added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))

    def delete_profile(self):
        reply = QMessageBox.question(
            self, "Confirm",
            "Delete this profile?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.dp.query("DELETE FROM PROFILE WHERE Student_Id = ?", (self.stuID,))
                QMessageBox.information(self, "Success", "Profile deleted")
                self.clear_fields()
            except Exception as e:
                QMessageBox.critical(self, "DB Error", str(e))

    def load_profile(self):
        query = self.dp.query(
            "SELECT Phone, Address, Birth_Date, Gender, Nationality, Photo_Path FROM PROFILE WHERE Student_Id = ?",
            (self.stuID,),
        )

        if query.next():
            self.input_phone.setText(str(query.value(0)))
            self.input_address.setText(str(query.value(1)))

            birth = query.value(2)
            if birth:
                self.input_birth.setDate(
                    QDate.fromString(str(birth), "yyyy-MM-dd")
                )

            self.input_gender.setText(str(query.value(3)))
            self.input_nationality.setText(str(query.value(4)))

            photo = str(query.value(5))
            self.input_photo.setText(photo)

            if photo:
                pix = QPixmap(photo)
                if not pix.isNull():
                    self.photo_label.setPixmap(
                        pix.scaled(220, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    )

    def clear_fields(self):
        self.input_phone.clear()
        self.input_address.clear()
        self.input_birth.setDate(QDate(2000, 1, 1))
        self.input_gender.clear()
        self.input_nationality.clear()
        self.input_photo.clear()
        self.photo_label.clear()

    # ================= DB =================
    def createProfile(self):
        self.dp._exec("""
        CREATE TABLE IF NOT EXISTS PROFILE (
    Student_Id  INTEGER PRIMARY KEY,
    Phone       TEXT,
    Address     TEXT,
    Birth_Date  TEXT,
    Gender      TEXT,
    Nationality TEXT,
    Photo_Path  TEXT,
    FOREIGN KEY (Student_Id) REFERENCES STUDENTS(Student_Id)
);

        """)
