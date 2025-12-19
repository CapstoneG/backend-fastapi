from app.repositories.exam_repository import ExamRepository
from app.schemas.request.submit_exam_request import SubmitExamRequest
from app.utils.calculate_toeic_score import calculate_toeic_score
from bson import ObjectId
from fastapi import HTTPException
from app.schemas.question_result_response import QuestionResultResponse
from app.schemas.exam_submit_response import ExamSubmitResponse

class SubmitExamService:
    def __init__(self):
        self.repository = ExamRepository()

    def submit_exam(self, request: SubmitExamRequest):            
        try:
            exam = self.repository.find_by_id(request.exam_id)
        except:
            raise HTTPException(status_code=404, detail="Exam not found")

        FULL_PARTS_SET = {"Part1", "Part2", "Part3", "Part4", "Part5", "Part6", "Part7"}
        
        user_parts = set(request.parts)
        
        if "All" in user_parts:
            parts_to_grade = FULL_PARTS_SET 
            is_full_test = True
        else:
            parts_to_grade = user_parts
            is_full_test = FULL_PARTS_SET.issubset(parts_to_grade)

        answer_key_map = {}
        total_questions_scope = 0
        
        for part_name, groups in exam.get("parts", {}).items():
            if part_name in parts_to_grade:
                for group in groups:
                    for question in group.get("questions", []):
                        q_id = str(question.get("question_id"))
                        total_questions_scope += 1
                        
                        answer_key_map[q_id] = {
                            "correct": question.get("correct_answer"),
                            "number": question.get("question_number"),
                            "part": part_name,
                            "answer_text": question.get("answer_text"),
                            "question_text": question.get("question_text"),
                            "transcript": question.get("transcript"),
                            "transcript_clean": question.get("transcript_clean"),
                            "explanation": question.get("explanation"),
                            "explanation_clean": question.get("explanation_clean")
                        }

        results = []
        correct_count = 0
        wrong_count = 0
        listening_correct = 0 
        reading_correct = 0   

        for q_id, info in answer_key_map.items():
            user_ans = request.answers.get(q_id)

            is_correct = False
            if user_ans and user_ans.upper() == info["correct"].upper():
                is_correct = True
                correct_count += 1
                
                # Phân loại để tính điểm 
                if info["part"] in ["Part1", "Part2", "Part3", "Part4"]:
                    listening_correct += 1
                elif info["part"] in ["Part5", "Part6", "Part7"]:
                    reading_correct += 1
            elif user_ans and user_ans.upper() != info["correct"].upper():
                wrong_count += 1

            # Lưu kết quả chi tiết
            results.append(QuestionResultResponse(
                question_id=q_id,
                question_number=info["number"],
                question_text=info["question_text"],
                answer_text=info["answer_text"],
                user_answer=user_ans if user_ans else "",
                correct_answer=info["correct"],
                is_correct=is_correct,
                explanation=info["explanation"],
                explanation_clean=info["explanation_clean"],
                transcript=info["transcript"],
                transcript_clean=info["transcript_clean"]
            ))

        final_scores = {"total": 0, "listening": 0, "reading": 0}
        
        if is_full_test:
            final_scores = calculate_toeic_score(listening_correct, reading_correct)
        
        return ExamSubmitResponse(
            is_full_test=is_full_test,
            total_correct=correct_count,
            total_wrong=wrong_count,
            total_skipped=total_questions_scope - (correct_count + wrong_count),
            total_questions=total_questions_scope,
            
            score=final_scores["total"],
            listening_score=final_scores["listening"],
            reading_score=final_scores["reading"],
            
            details=results
        )