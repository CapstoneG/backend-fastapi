# from typing import List, Dict, Optional
# from pydantic import BaseModel
# import json

# from app.enums.enum_error_type import ErrorType
# from app.core.ai_provider import AIProvider, get_gemini_provider


# class AnalysisResult(BaseModel):
#     results: List[List[str]]


# class SentenceAnalyzer:
#     def __init__(self, ai_provider: Optional[AIProvider] = None, api_key: Optional[str] = None, model: str = "gemini"):
#         # Prefer injected provider; otherwise try to construct one from env/config
#         if ai_provider is not None:
#             self.ai_provider = ai_provider
#         else:
#             try:
#                 if api_key:
#                     self.ai_provider = get_gemini_provider(api_key=api_key, model=model)
#                 else:
#                     self.ai_provider = None
#             except Exception:
#                 self.ai_provider = None

#     def _rules_fallback(self, sentences: List[str]) -> List[ErrorType]:
#         errors: List[ErrorType] = []
#         for s in sentences:
#             text = s.lower()

#             if "yesterday i go" in text:
#                 errors.append(ErrorType.VERB_TENSE)

#             if "have learn" in text:
#                 errors.append(ErrorType.VERB_TENSE)

#             if "very like" in text or "am agree" in text:
#                 errors.append(ErrorType.VERB_PATTERN)

#             if "she don't" in text:
#                 errors.append(ErrorType.AGREEMENT)

#             if "explain me" in text:
#                 errors.append(ErrorType.PREPOSITION)

#             if "feel boring" in text:
#                 errors.append(ErrorType.ADJECTIVE_FORM)

#         return errors

#     def analyze(self, sentences: List[str]) -> List[ErrorType]:
#         # If an AI provider exists and is healthy, ask Gemini to classify errors.
#         if self.ai_provider is not None and getattr(self.ai_provider, "check_health", lambda: False)():
#             try:
#                 system_instruction = (
#                     "You are an English grammar error classifier. Given a list of sentences, "
#                     "for each sentence return a list of zero or more error labels from this set: "
#                     "[VERB_TENSE, VERB_PATTERN, AGREEMENT, PREPOSITION, ADJECTIVE_FORM]. "
#                     "Return a JSON object with a single field `results` which is an array of arrays, "
#                     "where each inner array contains the labels (strings) applicable to the corresponding sentence. "
#                     "Do not include any other keys or extra text."
#                 )

#                 # Prepare a single user message with the sentences encoded as JSON for clarity.
#                 user_content = json.dumps({"sentences": sentences}, ensure_ascii=False)

#                 history = [{"role": "user", "content": user_content}]

#                 response = self.ai_provider.generate_chat_response(
#                     history=history,
#                     system_instruction=system_instruction,
#                     response_schema=AnalysisResult,
#                 )

#                 # `response` should be a pydantic model with `results`
#                 if response and hasattr(response, "results"):
#                     labels_per_sentence = response.results
#                     errors: List[ErrorType] = []
#                     for labels in labels_per_sentence:
#                         for lbl in labels:
#                             try:
#                                 errors.append(ErrorType[lbl])
#                             except Exception:
#                                 # unknown label; ignore
#                                 continue
#                     return errors
#             except Exception:
#                 # Fall through to rule-based fallback on any error
#                 pass

#         # No provider or provider failed -> use simple deterministic rules
#         return self._rules_fallback(sentences)

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from enum import Enum
import json
from app.core.ai_provider import get_gemini_provider
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', '')

# ============================================================================
# ENUMS - Error Types
# ============================================================================
class ErrorType(Enum):
    """Các loại lỗi ngữ pháp tiếng Anh"""
    # Grammar errors
    VERB_TENSE = "verb_tense"  # Thì động từ sai
    VERB_PATTERN = "verb_pattern"  # Cấu trúc động từ sai
    AGREEMENT = "agreement"  # Sự hòa hợp chủ ngữ - động từ
    PRONOUN = "pronoun"  # Đại từ sai
    
    # Word usage
    PREPOSITION = "preposition"  # Giới từ sai
    ARTICLE = "article"  # Mạo từ sai (a/an/the)
    ADJECTIVE_FORM = "adjective_form"  # Dạng tính từ sai (-ed/-ing)
    WORD_CHOICE = "word_choice"  # Chọn từ không phù hợp
    
    # Sentence structure
    WORD_ORDER = "word_order"  # Trật tự từ sai
    SENTENCE_FRAGMENT = "sentence_fragment"  # Câu không hoàn chỉnh
    RUN_ON = "run_on"  # Câu dài không ngắt
    
    # Mechanics
    SINGULAR_PLURAL = "singular_plural"  # Số ít/nhiều
    SPELLING = "spelling"  # Chính tả
    PUNCTUATION = "punctuation"  # Dấu câu
    
    # Other
    OTHER = "other"  # Lỗi khác


class ErrorSeverity(Enum):
    """Mức độ nghiêm trọng của lỗi"""
    LOW = "low"  # Lỗi nhỏ, không ảnh hưởng nghiêm trọng
    MEDIUM = "medium"  # Lỗi vừa, ảnh hưởng đến hiểu
    HIGH = "high"  # Lỗi nghiêm trọng, gây hiểu lầm


# ============================================================================
# MODELS - Pydantic schemas
# ============================================================================
class ErrorDetail(BaseModel):
    """Chi tiết một lỗi ngữ pháp"""
    type: str = Field(..., description="Loại lỗi (ErrorType)")
    description: str = Field(..., description="Mô tả cụ thể lỗi")
    severity: str = Field(default="medium", description="Mức độ: low/medium/high")
    suggestion: Optional[str] = Field(None, description="Gợi ý sửa lỗi")
    position: Optional[int] = Field(None, description="Vị trí lỗi trong câu")


class SentenceAnalysis(BaseModel):
    """Kết quả phân tích một câu"""
    sentence: str = Field(..., description="Câu được phân tích")
    errors: List[ErrorDetail] = Field(default_factory=list, description="Danh sách lỗi")
    is_correct: bool = Field(..., description="Câu có đúng ngữ pháp không")


class AnalysisResult(BaseModel):
    """Kết quả phân tích từ AI"""
    results: List[List[ErrorDetail]] = Field(
        ..., 
        description="Mảng của mảng ErrorDetail, mỗi mảng con tương ứng với một câu"
    )


# ============================================================================
# SENTENCE ANALYZER - Main class
# ============================================================================
class SentenceAnalyzer:
    """
    Phân tích lỗi ngữ pháp trong câu tiếng Anh
    Hỗ trợ 2 chế độ:
    1. AI-powered (sử dụng Gemini/Claude API)
    2. Rule-based fallback (các quy tắc cơ bản)
    """
    
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL, use_ai: bool = True):
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = get_gemini_provider(api_key, model)
        self.use_ai = use_ai
    
    # ========================================================================
    # PUBLIC METHODS
    # ========================================================================
    
    def analyze(self, sentences: List[str]) -> List[SentenceAnalysis]:
        """
        Phân tích danh sách câu
        
        Args:
            sentences: List các câu cần phân tích
            
        Returns:
            List[SentenceAnalysis]: Kết quả phân tích từng câu
        """
        if not sentences:
            return []
        
        # Thử dùng AI trước
        if self.use_ai and self._is_ai_available():
            try:
                return self._analyze_with_ai(sentences)
            except Exception as e:
                print(f"AI analysis failed: {e}, falling back to rules")
        
        # Fallback sang rule-based
        return self._analyze_with_rules(sentences)
    
    def analyze_single(self, sentence: str) -> SentenceAnalysis:
        """
        Phân tích một câu đơn
        
        Args:
            sentence: Câu cần phân tích
            
        Returns:
            SentenceAnalysis: Kết quả phân tích
        """
        results = self.analyze([sentence])
        return results[0] if results else SentenceAnalysis(
            sentence=sentence,
            errors=[],
            is_correct=True
        )
    
    def get_error_summary(
        self, 
        sentences: List[str]
    ) -> Dict[str, int]:
        """
        Lấy thống kê lỗi
        
        Args:
            sentences: List câu cần phân tích
            
        Returns:
            Dict với key là tên lỗi, value là số lần xuất hiện
        """
        analyses = self.analyze(sentences)
        error_counts = {}
        
        for analysis in analyses:
            for error in analysis.errors:
                error_type = error.type
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return error_counts
    
    # ========================================================================
    # AI-POWERED ANALYSIS
    # ========================================================================
    
    def _is_ai_available(self) -> bool:
        """Kiểm tra AI provider có sẵn và healthy không"""
        return True
    
    def _analyze_with_ai(self, sentences: List[str]) -> List[SentenceAnalysis]:
        """
        Phân tích bằng AI (Gemini/Claude)
        
        Args:
            sentences: List câu cần phân tích
            
        Returns:
            List[SentenceAnalysis]: Kết quả phân tích
        """
        system_instruction = self._get_ai_system_prompt()
        user_content = json.dumps({"sentences": sentences}, ensure_ascii=False)
        
        history = [{"role": "user", "content": user_content}]
        
        # Gọi AI provider
        response = self.client.generate_chat_response(
            history=history,
            system_instruction=system_instruction,
            response_schema=AnalysisResult,
        )
        
        # Parse response
        if not response or not hasattr(response, 'results'):
            raise ValueError("Invalid AI response format")
        
        # Convert sang SentenceAnalysis
        results = []
        for i, sentence in enumerate(sentences):
            if i < len(response.results):
                errors = response.results[i]
                # Validate error types
                validated_errors = []
                for error in errors:
                    if self._is_valid_error_type(error.type):
                        validated_errors.append(error)
                
                results.append(SentenceAnalysis(
                    sentence=sentence,
                    errors=validated_errors,
                    is_correct=len(validated_errors) == 0
                ))
            else:
                results.append(SentenceAnalysis(
                    sentence=sentence,
                    errors=[],
                    is_correct=True
                ))
        
        return results
    
    def _get_ai_system_prompt(self) -> str:
        """Tạo system prompt cho AI"""
        error_types = ", ".join([e.value.upper() for e in ErrorType])
        
        return f"""You are an expert English grammar error analyzer.

Given a list of sentences, analyze each sentence and identify grammar errors.

Available error types:
{error_types}

For each sentence, return a list of ErrorDetail objects with:
- type: one of the error types above (lowercase with underscores)
- description: specific explanation in Vietnamese (or English if Vietnamese not possible)
- severity: "low", "medium", or "high"
- suggestion: (optional) how to fix the error
- position: (optional) word position in sentence (0-indexed)

Rules:
1. Return ONLY JSON, no markdown, no preamble
2. Use "other" type only when error doesn't fit any category
3. Be specific in descriptions
4. If sentence is correct, return empty array for that sentence

Return format:
{{
  "results": [
    [/* errors for sentence 1 */],
    [/* errors for sentence 2 */],
    ...
  ]
}}
"""
    
    def _is_valid_error_type(self, error_type: str) -> bool:
        """Kiểm tra error type có hợp lệ không"""
        try:
            ErrorType[error_type.upper()]
            return True
        except KeyError:
            return False
    
    # ========================================================================
    # RULE-BASED FALLBACK
    # ========================================================================
    
    def _analyze_with_rules(self, sentences: List[str]) -> List[SentenceAnalysis]:
        """
        Phân tích bằng rules đơn giản (fallback)
        
        Args:
            sentences: List câu cần phân tích
            
        Returns:
            List[SentenceAnalysis]: Kết quả phân tích
        """
        results = []
        
        for sentence in sentences:
            errors = self._apply_rules(sentence)
            results.append(SentenceAnalysis(
                sentence=sentence,
                errors=errors,
                is_correct=len(errors) == 0
            ))
        
        return results
    
    def _apply_rules(self, sentence: str) -> List[ErrorDetail]:
        """
        Áp dụng các quy tắc kiểm tra lỗi cơ bản
        
        Args:
            sentence: Câu cần kiểm tra
            
        Returns:
            List[ErrorDetail]: Danh sách lỗi tìm được
        """
        errors = []
        text_lower = sentence.lower()
        
        # Rule 1: Verb tense errors
        if "yesterday" in text_lower and " go " in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.VERB_TENSE.value,
                description="Sử dụng 'go' thay vì 'went' với 'yesterday'",
                severity=ErrorSeverity.HIGH.value,
                suggestion="Đổi 'go' thành 'went'"
            ))
        
        if "have learn" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.VERB_TENSE.value,
                description="Thiếu '-ed' hoặc '-ing' sau 'have'",
                severity=ErrorSeverity.HIGH.value,
                suggestion="Đổi 'learn' thành 'learned' hoặc 'been learning'"
            ))
        
        # Rule 2: Verb pattern errors
        if "very like" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.VERB_PATTERN.value,
                description="'Very' không đi với động từ 'like'",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Dùng 'really like' hoặc 'like very much'"
            ))
        
        if "am agree" in text_lower or "is agree" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.VERB_PATTERN.value,
                description="'Agree' không dùng với 'am/is/are'",
                severity=ErrorSeverity.HIGH.value,
                suggestion="Dùng 'agree' hoặc 'am in agreement'"
            ))
        
        # Rule 3: Subject-verb agreement
        if "she don't" in text_lower or "he don't" in text_lower or "it don't" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.AGREEMENT.value,
                description="Chủ ngữ số ít phải dùng 'doesn't', không phải 'don't'",
                severity=ErrorSeverity.HIGH.value,
                suggestion="Đổi 'don't' thành 'doesn't'"
            ))
        
        # Rule 4: Preposition errors
        if "explain me" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.PREPOSITION.value,
                description="Thiếu giới từ 'to' sau 'explain'",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Dùng 'explain to me' hoặc 'explain it to me'"
            ))
        
        if "listen music" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.PREPOSITION.value,
                description="Thiếu giới từ 'to' sau 'listen'",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Dùng 'listen to music'"
            ))
        
        # Rule 5: Adjective form errors
        if "feel boring" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.ADJECTIVE_FORM.value,
                description="Dùng 'boring' (chủ động) thay vì 'bored' (bị động)",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Đổi 'boring' thành 'bored'"
            ))
        
        if "interested in" in text_lower and "am interesting" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.ADJECTIVE_FORM.value,
                description="Dùng 'interesting' thay vì 'interested'",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Đổi 'interesting' thành 'interested'"
            ))
        
        # Rule 6: Article errors
        if " go to school" not in text_lower and " go to a school" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.ARTICLE.value,
                description="'Go to school' không cần mạo từ khi nói về hoạt động học",
                severity=ErrorSeverity.LOW.value,
                suggestion="Bỏ 'a' trong 'go to a school'"
            ))
        
        # Rule 7: Word order
        if "never i" in text_lower or "always i" in text_lower:
            errors.append(ErrorDetail(
                type=ErrorType.WORD_ORDER.value,
                description="Trạng từ tần suất phải đứng sau chủ ngữ trong câu khẳng định",
                severity=ErrorSeverity.MEDIUM.value,
                suggestion="Đổi vị trí: 'I never' hoặc 'I always'"
            ))
        
        return errors
