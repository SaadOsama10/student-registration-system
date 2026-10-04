# class StudentAcademicCalculator:

#     def __init__(self, dp, student_id):
#         self.dp = dp
#         self.student_id = student_id

#     def get_current_semester(self):
#         sql = f"""
#         SELECT Sem_Id 
#         FROM TRANSCRIPT
#         WHERE Student_Id = {self.student_id}
#         ORDER BY Sem_Id DESC
#         """
#         q = self.dp._exec(sql)
#         return q.value(0) if q.next() else None

#     def calculate_year(self):
#         sql = f"""
#         SELECT COUNT(*) 
#         FROM TRANSCRIPT
#         WHERE Student_Id = {self.student_id}
#         """
#         q = self.dp._exec(sql)
#         semesters = q.value(0) if q.next() else 0
#         year = (semesters + 1) // 2
#         return year

#     def calculate_term_credits(self, sem_id):
#         sql = f"""
#         SELECT SUM(TD.Credits)
#         FROM TRANSCRIPT_DETAILS TD
#         JOIN TRANSCRIPT T ON TD.Transcript_Id = T.Transcript_Id
#         WHERE T.Student_Id = {self.student_id}
#           AND T.Sem_Id = {sem_id}
#         """
#         q = self.dp._exec(sql)
#         return q.value(0) if q.next() else 0

#     def calculate_total_credits(self):
#         sql = f"""
#         SELECT SUM(TD.Credits)
#         FROM TRANSCRIPT_DETAILS TD
#         JOIN TRANSCRIPT T ON TD.Transcript_Id = T.Transcript_Id
#         WHERE T.Student_Id = {self.student_id}
#         """
#         q = self.dp._exec(sql)
#         return q.value(0) if q.next() else 0

#     def calculate_term_gpa(self, sem_id):
#         sql = f"""
#         SELECT SUM(TD.Grade_Points * TD.Credits),
#                SUM(TD.Credits)
#         FROM TRANSCRIPT_DETAILS TD
#         JOIN TRANSCRIPT T ON TD.Transcript_Id = T.Transcript_Id
#         WHERE T.Student_Id = {self.student_id}
#           AND T.Sem_Id = {sem_id}
#         """
#         q = self.dp._exec(sql)
#         if q.next():
#             total_points = q.value(0) or 0
#             credits = q.value(1) or 0
#             return round(total_points / credits, 2) if credits > 0 else 0
#         return 0

#     def calculate_total_gpa(self):
#         sql = f"""
#         SELECT SUM(TD.Grade_Points * TD.Credits),
#                SUM(TD.Credits)
#         FROM TRANSCRIPT_DETAILS TD
#         JOIN TRANSCRIPT T ON TD.Transcript_Id = T.Transcript_Id
#         WHERE T.Student_Id = {self.student_id}
#         """
#         q = self.dp._exec(sql)
#         if q.next():
#             total_points = q.value(0) or 0
#             credits = q.value(1) or 0
#             return round(total_points / credits, 2) if credits > 0 else 0
#         return 0
