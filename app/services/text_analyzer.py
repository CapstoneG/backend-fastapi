from typing import List, Dict
from collections import Counter
import re
from app.services.sentence_analyzer import SentenceAnalyzer

class TextQualityAnalyzer:
    def __init__(self, sentence_analyzer: SentenceAnalyzer):
        self.sentence_analyzer = sentence_analyzer
    
    def count_syllables(self, word: str) -> int:
        """Đếm số âm tiết đơn giản"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        return max(1, syllable_count)
    
    def analyze_text(self, sentences: List[str]) -> Dict:
        """Phân tích toàn diện văn bản"""
        
        # 1. Phân tích lỗi ngữ pháp
        errors = self.sentence_analyzer.analyze(sentences)
        error_types = [e.value for e in errors]
        error_counter = Counter(error_types)
        
        # 2. Đếm từ và câu
        total_sentences = len(sentences)
        text = " ".join(sentences)
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        unique_words = len(set(words))
        
        # 3. Đếm syllables
        total_syllables = sum(self.count_syllables(w) for w in words)
        
        # 4. Tính các chỉ số
        if total_words == 0:
            return {"error": "No words found"}
        
        # Grammar Accuracy
        grammar_accuracy = (total_sentences - len(errors)) / total_sentences * 100 if total_sentences > 0 else 0
        
        # Error Density (per 100 words)
        error_density = (len(errors) / total_words) * 100
        
        # Vocabulary Diversity (TTR)
        vocabulary_diversity = unique_words / total_words
        
        # Average Sentence Length
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        
        # Flesch Reading Ease
        if total_sentences > 0:
            flesch_reading_ease = (
                206.835 
                - 1.015 * (total_words / total_sentences)
                - 84.6 * (total_syllables / total_words)
            )
        else:
            flesch_reading_ease = 0
        
        # Flesch-Kincaid Grade Level
        if total_sentences > 0:
            flesch_kincaid_grade = (
                0.39 * (total_words / total_sentences)
                + 11.8 * (total_syllables / total_words)
                - 15.59
            )
        else:
            flesch_kincaid_grade = 0
        
        # 5. Đánh giá tổng quan
        overall_score = self._calculate_overall_score(
            grammar_accuracy, error_density, vocabulary_diversity, 
            avg_sentence_length, flesch_reading_ease
        )
        
        return {
            # Thống kê cơ bản
            "basic_stats": {
                "total_sentences": total_sentences,
                "total_words": total_words,
                "unique_words": unique_words,
                "total_syllables": total_syllables,
                "avg_sentence_length": round(avg_sentence_length, 2)
            },
            
            # Lỗi ngữ pháp
            "grammar": {
                "total_errors": len(errors),
                "error_types": dict(error_counter),
                "grammar_accuracy": round(grammar_accuracy, 2),
                "error_density": round(error_density, 2)
            },
            
            # Từ vựng
            "vocabulary": {
                "diversity_score": round(vocabulary_diversity, 3),
                "unique_word_count": unique_words
            },
            
            # Độ dễ đọc
            "readability": {
                "flesch_reading_ease": round(flesch_reading_ease, 2),
                "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
                "readability_level": self._get_readability_level(flesch_reading_ease)
            },
            
            # Điểm tổng quan
            "overall": {
                "score": round(overall_score, 2),
                "level": self._get_proficiency_level(overall_score)
            }
        }
    
    def _calculate_overall_score(self, grammar_acc, error_dens, vocab_div, 
                                   avg_sent_len, flesch) -> float:
        """Tính điểm tổng (0-100)"""
        # Trọng số cho từng tiêu chí
        weights = {
            "grammar": 0.4,      # 40%
            "vocabulary": 0.2,   # 20%
            "readability": 0.2,  # 20%
            "sentence": 0.2      # 20%
        }
        
        # Chuẩn hóa các chỉ số về thang 0-100
        grammar_score = grammar_acc
        
        # Error density (0 error = 100 điểm, >10 errors/100 words = 0 điểm)
        error_score = max(0, 100 - error_dens * 10)
        
        # Vocabulary diversity (TTR 0.5-0.7 là tốt)
        vocab_score = min(100, vocab_div * 200)
        
        # Sentence length (15-20 từ là optimal)
        if 15 <= avg_sent_len <= 20:
            sentence_score = 100
        elif avg_sent_len < 15:
            sentence_score = (avg_sent_len / 15) * 100
        else:
            sentence_score = max(0, 100 - (avg_sent_len - 20) * 5)
        
        # Flesch score (60-70 là standard)
        if 60 <= flesch <= 70:
            readability_score = 100
        elif flesch < 60:
            readability_score = max(0, flesch / 60 * 100)
        else:
            readability_score = max(0, 100 - (flesch - 70) * 2)
        
        # Tổng hợp
        total = (
            grammar_score * weights["grammar"] +
            vocab_score * weights["vocabulary"] +
            readability_score * weights["readability"] +
            sentence_score * weights["sentence"]
        )
        
        return total
    
    def _get_readability_level(self, flesch_score: float) -> str:
        """Phân loại độ dễ đọc"""
        if flesch_score >= 90:
            return "Very Easy (5th grade)"
        elif flesch_score >= 80:
            return "Easy (6th grade)"
        elif flesch_score >= 70:
            return "Fairly Easy (7th grade)"
        elif flesch_score >= 60:
            return "Standard (8th-9th grade)"
        elif flesch_score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif flesch_score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College graduate)"
    
    def _get_proficiency_level(self, score: float) -> str:
        """Xếp loại trình độ"""
        if score >= 90:
            return "Excellent (C2)"
        elif score >= 80:
            return "Very Good (C1)"
        elif score >= 70:
            return "Good (B2)"
        elif score >= 60:
            return "Intermediate (B1)"
        elif score >= 50:
            return "Pre-intermediate (A2)"
        else:
            return "Beginner (A1)"