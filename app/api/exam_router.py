from app.services.exam_service import ExamService
from fastapi import APIRouter, HTTPException
from app.schemas.exam_response import ExamResponse
from app.services.submit_exam_service import SubmitExamService
from app.schemas.exam_submit_response import ExamSubmitResponse
from app.schemas.request.submit_exam_request import SubmitExamRequest

router = APIRouter(prefix="/exams", tags=["Exams"])
exam_service = ExamService()
submit_exam_service = SubmitExamService()

@router.get("/", response_model=list)
def get_all_exams():
    return exam_service.get_all_exams()

@router.get("/title/{title}", response_model=dict)
def get_exam_by_title(title: str):
    exam = exam_service.get_exam_by_title(title)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam_by_id(exam_id: str):
    exam = exam_service.get_exam_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

@router.get("/part/{part_name}", response_model=list)
def get_exams_by_part(part_name: str):
    return exam_service.get_exams_by_part(part_name)

@router.post("/")
def create_exam(exam_data: dict):
    return exam_service.create_exam(exam_data)

@router.post("/submit", response_model=ExamSubmitResponse)
def submit_exam(exam_submit: SubmitExamRequest):
    return submit_exam_service.submit_exam(exam_submit)
