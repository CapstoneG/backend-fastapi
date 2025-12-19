from app.repositories.exam_repository import ExamRepository
from app.schemas.simple_exam_response import SimpleExamResponse
from app.schemas.exam_response import ExamResponse

class ExamService:
    def __init__(self):
        self.exam_repository = ExamRepository()

    def get_all_exams(self):
        exams = self.exam_repository.find_all()
        return [self.to_simple_response(exam) for exam in exams]

    def get_exam_by_title(self, title: str):
        return self.exam_repository.find_by_title(title)

    def get_exam_by_id(self, exam_id: str):
        exam = self.exam_repository.find_by_id(exam_id)
        return self.to_exam_response(exam)

    def get_exams_by_part(self, part_name: str):
        return self.exam_repository.find_by_part(part_name)

    def create_exam(self, exam_data: dict):
        return self.exam_repository.save(exam_data)
    
    def to_simple_response(self, exam):
        return SimpleExamResponse(
            exam_id= str(exam.get("_id")),
            exam_title= exam.get("exam_title")
    )

    def to_exam_response(self, exam):
        return ExamResponse(
            id= str(exam.get("_id")),
            exam_title= exam.get("exam_title"),
            parts=exam.get('parts')
        )