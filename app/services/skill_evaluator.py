from typing import List, Dict, Optional
import re
from collections import Counter


# ============================================================================
# SKILL EVALUATOR - Đánh giá kỹ năng tiếng Anh
# ============================================================================

class SkillEvaluator:
    """
    Đánh giá kỹ năng tiếng Anh dựa trên:
    1. Grammar accuracy (từ SentenceAnalyzer)
    2. Vocabulary diversity
    3. Readability
    4. Sentence complexity
    """
    
    def __init__(self, sentence_analyzer: Optional['SentenceAnalyzer'] = None):
        """
        Khởi tạo evaluator
        
        Args:
            sentence_analyzer: Instance của SentenceAnalyzer để phân tích lỗi
        """
        self.sentence_analyzer = sentence_analyzer
    
    # ========================================================================
    # PUBLIC METHODS
    # ========================================================================
    
    def evaluate(self, sentences: List[str]) -> Dict:
        """
        Đánh giá toàn diện kỹ năng viết
        
        Args:
            sentences: List các câu cần đánh giá
            
        Returns:
            Dict chứa các chỉ số đánh giá
        """
        if not sentences:
            return self._empty_result()
        
        # 1. Phân tích lỗi ngữ pháp
        grammar_analysis = self._analyze_grammar(sentences)
        
        # 2. Phân tích từ vựng
        vocabulary_analysis = self._analyze_vocabulary(sentences)
        
        # 3. Phân tích độ phức tạp câu
        complexity_analysis = self._analyze_complexity(sentences)
        
        # 4. Phân tích độ dễ đọc
        readability_analysis = self._analyze_readability(sentences)
        
        # 5. Tính điểm tổng hợp
        overall_score = self._calculate_overall_score(
            grammar_analysis["score"],
            vocabulary_analysis["score"],
            complexity_analysis["score"],
            readability_analysis["score"]
        )
        
        # 6. Ước lượng trình độ CEFR
        estimated_cefr = self._estimate_cefr(
            grammar_analysis["score"],
            vocabulary_analysis["score"],
            complexity_analysis["score"],
            overall_score
        )
        
        return {
            # Thống kê cơ bản
            "basic_stats": {
                "total_sentences": len(sentences),
                "total_words": vocabulary_analysis["total_words"],
                "unique_words": vocabulary_analysis["unique_words"],
                "avg_sentence_length": complexity_analysis["avg_sentence_length"]
            },
            
            # Phân tích ngữ pháp
            "grammar": grammar_analysis,
            
            # Phân tích từ vựng
            "vocabulary": vocabulary_analysis,
            
            # Phân tích độ phức tạp
            "complexity": complexity_analysis,
            
            # Phân tích độ dễ đọc
            "readability": readability_analysis,
            
            # Điểm tổng hợp
            "overall": {
                "score": overall_score,
                "grade": self._get_grade(overall_score),
                "estimated_cefr": estimated_cefr,
                "level_description": self._get_cefr_description(estimated_cefr)
            },
            
            # Gợi ý cải thiện
            "recommendations": self._generate_recommendations(
                grammar_analysis,
                vocabulary_analysis,
                complexity_analysis,
                readability_analysis
            )
        }
    
    def evaluate_simple(self, sentences: List[str]) -> Dict:
        """
        Đánh giá đơn giản (nhanh hơn, ít chi tiết hơn)
        Tương thích với code cũ
        
        Args:
            sentences: List các câu
            
        Returns:
            Dict với format tương tự code cũ
        """
        if not sentences:
            return {
                "total_sentences": 0,
                "error_counts": {},
                "grammar_error_rate": 0,
                "grammar_score": 0,
                "vocabulary_score": 0,
                "estimated_cefr": "A1"
            }
        
        # Phân tích lỗi
        grammar_analysis = self._analyze_grammar(sentences)
        
        # Tính vocabulary score đơn giản
        words = set()
        for s in sentences:
            for w in re.findall(r'\b\w+\b', s.lower()):
                words.add(w)
        vocabulary_score = min(100, len(words) * 4)
        
        # CEFR estimation
        avg = (grammar_analysis["score"] + vocabulary_score) // 2
        if avg < 40:
            cefr = "A1"
        elif avg < 60:
            cefr = "A2"
        elif avg < 75:
            cefr = "B1"
        else:
            cefr = "B2"
        
        return {
            "total_sentences": len(sentences),
            "error_counts": grammar_analysis["error_counts"],
            "grammar_error_rate": grammar_analysis["error_rate"],
            "grammar_score": grammar_analysis["score"],
            "vocabulary_score": vocabulary_score,
            "estimated_cefr": cefr
        }
    
    # ========================================================================
    # GRAMMAR ANALYSIS
    # ========================================================================
    
    def _analyze_grammar(self, sentences: List[str]) -> Dict:
        """Phân tích ngữ pháp sử dụng SentenceAnalyzer"""
        if self.sentence_analyzer is None:
            # Fallback: tạo analyzer tạm thời
            from app.services.sentence_analyzer import SentenceAnalyzer
            analyzer = SentenceAnalyzer(use_ai=False)
            analyses = analyzer.analyze(sentences)
        else:
            analyses = self.sentence_analyzer.analyze(sentences)
        
        # Đếm lỗi
        total_errors = 0
        error_counts = {}
        error_severity_counts = {"low": 0, "medium": 0, "high": 0}
        
        for analysis in analyses:
            total_errors += len(analysis.errors)
            for error in analysis.errors:
                error_type = error.type
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
                
                severity = error.severity
                if severity in error_severity_counts:
                    error_severity_counts[severity] += 1
        
        # Tính error rate
        total_sentences = len(sentences)
        error_rate = total_errors / total_sentences if total_sentences > 0 else 0
        
        # Tính grammar score (0-100)
        # Công thức: bắt đầu từ 100, trừ đi theo error rate
        # Error rate = 0 → score = 100
        # Error rate = 1 (1 lỗi/câu) → score = 50
        # Error rate = 2+ → score giảm nhanh
        grammar_score = max(0, int(100 - (error_rate * 50)))
        
        # Điều chỉnh theo severity
        severity_penalty = (
            error_severity_counts["high"] * 3 +
            error_severity_counts["medium"] * 1.5 +
            error_severity_counts["low"] * 0.5
        )
        grammar_score = max(0, grammar_score - int(severity_penalty))
        
        return {
            "total_errors": total_errors,
            "error_counts": error_counts,
            "error_severity": error_severity_counts,
            "error_rate": round(error_rate, 2),
            "score": grammar_score,
            "accuracy": round((1 - min(1, error_rate)) * 100, 1)
        }
    
    # ========================================================================
    # VOCABULARY ANALYSIS
    # ========================================================================
    
    def _analyze_vocabulary(self, sentences: List[str]) -> Dict:
        """Phân tích từ vựng"""
        text = " ".join(sentences)
        words = re.findall(r'\b\w+\b', text.lower())
        
        total_words = len(words)
        unique_words = len(set(words))
        
        # Type-Token Ratio (TTR)
        ttr = unique_words / total_words if total_words > 0 else 0
        
        # Word frequency distribution
        word_freq = Counter(words)
        most_common = word_freq.most_common(10)
        
        # Ước lượng vocabulary level
        # TTR cao = từ vựng đa dạng
        # Unique words nhiều = vốn từ phong phú
        vocab_score = int(min(100, (ttr * 100 + unique_words * 2) / 2))
        
        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "type_token_ratio": round(ttr, 3),
            "most_common_words": most_common,
            "score": vocab_score
        }
    
    # ========================================================================
    # COMPLEXITY ANALYSIS
    # ========================================================================
    
    def _analyze_complexity(self, sentences: List[str]) -> Dict:
        """Phân tích độ phức tạp câu"""
        total_sentences = len(sentences)
        text = " ".join(sentences)
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)
        
        # Average sentence length
        avg_length = total_words / total_sentences if total_sentences > 0 else 0
        
        # Sentence length distribution
        lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
        min_length = min(lengths) if lengths else 0
        max_length = max(lengths) if lengths else 0
        
        # Complexity score
        # Optimal length: 15-20 words
        # Too short (<10) or too long (>30) reduces score
        if 15 <= avg_length <= 20:
            complexity_score = 100
        elif avg_length < 15:
            complexity_score = int((avg_length / 15) * 100)
        else:
            complexity_score = max(0, int(100 - (avg_length - 20) * 3))
        
        return {
            "avg_sentence_length": round(avg_length, 1),
            "min_sentence_length": min_length,
            "max_sentence_length": max_length,
            "score": complexity_score
        }
    
    # ========================================================================
    # READABILITY ANALYSIS
    # ========================================================================
    
    def _analyze_readability(self, sentences: List[str]) -> Dict:
        """Phân tích độ dễ đọc"""
        total_sentences = len(sentences)
        text = " ".join(sentences)
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)
        
        # Count syllables (simplified)
        total_syllables = sum(self._count_syllables(w) for w in words)
        
        # Flesch Reading Ease
        if total_sentences > 0 and total_words > 0:
            flesch = (
                206.835
                - 1.015 * (total_words / total_sentences)
                - 84.6 * (total_syllables / total_words)
            )
        else:
            flesch = 0
        
        # Flesch-Kincaid Grade Level
        if total_sentences > 0 and total_words > 0:
            fk_grade = (
                0.39 * (total_words / total_sentences)
                + 11.8 * (total_syllables / total_words)
                - 15.59
            )
        else:
            fk_grade = 0
        
        # Readability score (0-100)
        # Flesch 60-70 = optimal (score 100)
        if 60 <= flesch <= 70:
            readability_score = 100
        elif flesch < 60:
            readability_score = max(0, int(flesch / 60 * 100))
        else:
            readability_score = max(0, int(100 - (flesch - 70) * 2))
        
        return {
            "flesch_reading_ease": round(flesch, 1),
            "flesch_kincaid_grade": round(fk_grade, 1),
            "readability_level": self._get_readability_level(flesch),
            "score": readability_score
        }
    
    def _count_syllables(self, word: str) -> int:
        """Đếm số âm tiết (simplified)"""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
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
    
    # ========================================================================
    # OVERALL SCORING
    # ========================================================================
    
    def _calculate_overall_score(
        self,
        grammar_score: int,
        vocabulary_score: int,
        complexity_score: int,
        readability_score: int
    ) -> int:
        """Tính điểm tổng hợp"""
        # Trọng số cho từng tiêu chí
        weights = {
            "grammar": 0.4,      # 40% - quan trọng nhất
            "vocabulary": 0.25,  # 25%
            "complexity": 0.2,   # 20%
            "readability": 0.15  # 15%
        }
        
        overall = int(
            grammar_score * weights["grammar"] +
            vocabulary_score * weights["vocabulary"] +
            complexity_score * weights["complexity"] +
            readability_score * weights["readability"]
        )
        
        return overall
    
    def _get_grade(self, score: int) -> str:
        """Chuyển điểm số thành xếp loại"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "C+"
        elif score >= 65:
            return "C"
        elif score >= 60:
            return "D+"
        elif score >= 55:
            return "D"
        else:
            return "F"
    
    # ========================================================================
    # CEFR ESTIMATION
    # ========================================================================
    
    def _estimate_cefr(
        self,
        grammar_score: int,
        vocabulary_score: int,
        complexity_score: int,
        overall_score: int
    ) -> str:
        """
        Ước lượng trình độ CEFR
        
        CEFR levels:
        - A1: Beginner
        - A2: Elementary
        - B1: Intermediate
        - B2: Upper Intermediate
        - C1: Advanced
        - C2: Proficient
        """
        # Ưu tiên overall score, nhưng có thể điều chỉnh theo grammar
        # vì grammar là nền tảng quan trọng
        
        if overall_score >= 95 and grammar_score >= 95:
            return "C2"
        elif overall_score >= 85 and grammar_score >= 85:
            return "C1"
        elif overall_score >= 75 and grammar_score >= 70:
            return "B2"
        elif overall_score >= 60 and grammar_score >= 55:
            return "B1"
        elif overall_score >= 45 and grammar_score >= 40:
            return "A2"
        else:
            return "A1"
    
    def _get_cefr_description(self, cefr_level: str) -> str:
        """Mô tả trình độ CEFR"""
        descriptions = {
            "A1": "Beginner - Can understand and use basic phrases",
            "A2": "Elementary - Can communicate in simple routine tasks",
            "B1": "Intermediate - Can handle most situations while traveling",
            "B2": "Upper Intermediate - Can interact with native speakers fluently",
            "C1": "Advanced - Can use language flexibly and effectively",
            "C2": "Proficient - Can understand virtually everything with ease"
        }
        return descriptions.get(cefr_level, "Unknown level")
    
    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================
    
    def _generate_recommendations(
        self,
        grammar_analysis: Dict,
        vocabulary_analysis: Dict,
        complexity_analysis: Dict,
        readability_analysis: Dict
    ) -> List[str]:
        """Tạo gợi ý cải thiện"""
        recommendations = []
        
        # Grammar recommendations
        if grammar_analysis["score"] < 70:
            recommendations.append(
                "📚 Grammar: Focus on improving grammar accuracy. "
                f"Current error rate: {grammar_analysis['error_rate']} errors per sentence. "
                "Review basic grammar rules and practice more."
            )
            
            # Specific error recommendations
            error_counts = grammar_analysis["error_counts"]
            if error_counts:
                top_errors = sorted(
                    error_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                
                error_types_str = ", ".join([e[0] for e in top_errors])
                recommendations.append(
                    f"⚠️ Most common errors: {error_types_str}. "
                    "Focus on these areas for quick improvement."
                )
        
        # Vocabulary recommendations
        if vocabulary_analysis["score"] < 70:
            recommendations.append(
                f"📖 Vocabulary: Expand your vocabulary. "
                f"Current diversity: {vocabulary_analysis['type_token_ratio']:.2f}. "
                "Try using more varied words and expressions."
            )
        
        # Complexity recommendations
        avg_length = complexity_analysis["avg_sentence_length"]
        if avg_length < 10:
            recommendations.append(
                "📝 Sentence Structure: Your sentences are too short. "
                "Try combining ideas to create more complex sentences."
            )
        elif avg_length > 25:
            recommendations.append(
                "📝 Sentence Structure: Your sentences are too long. "
                "Break them into shorter, clearer sentences."
            )
        
        # Readability recommendations
        if readability_analysis["score"] < 60:
            recommendations.append(
                "👁️ Readability: Work on making your writing clearer. "
                f"Current level: {readability_analysis['readability_level']}. "
                "Use simpler words and vary sentence length."
            )
        
        # Positive feedback
        if not recommendations:
            recommendations.append(
                "✨ Great work! Your writing shows good proficiency. "
                "Keep practicing to maintain and improve your skills."
            )
        
        return recommendations
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _empty_result(self) -> Dict:
        """Kết quả rỗng khi không có dữ liệu"""
        return {
            "basic_stats": {
                "total_sentences": 0,
                "total_words": 0,
                "unique_words": 0,
                "avg_sentence_length": 0
            },
            "grammar": {"score": 0, "error_counts": {}},
            "vocabulary": {"score": 0},
            "complexity": {"score": 0},
            "readability": {"score": 0},
            "overall": {
                "score": 0,
                "grade": "F",
                "estimated_cefr": "A1",
                "level_description": "Beginner"
            },
            "recommendations": ["No data to analyze"]
        }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    from app.services.sentence_analyzer import SentenceAnalyzer
    
    # Setup
    analyzer = SentenceAnalyzer(use_ai=False)
    evaluator = SkillEvaluator(sentence_analyzer=analyzer)
    
    # Test data
    test_sentences = [
        "Yesterday I go to the store and buy some bread.",
        "I have learn English for three years now.",
        "She don't like coffee very much.",
        "Can you explain me how to solve this problem?",
        "The weather is beautiful today and I feel boring at home."
    ]
    
    print("=" * 70)
    print("FULL EVALUATION")
    print("=" * 70)
    
    result = evaluator.evaluate(test_sentences)
    
    print(f"\n📊 Basic Stats:")
    print(f"  Sentences: {result['basic_stats']['total_sentences']}")
    print(f"  Words: {result['basic_stats']['total_words']}")
    print(f"  Unique words: {result['basic_stats']['unique_words']}")
    
    print(f"\n📝 Grammar:")
    print(f"  Score: {result['grammar']['score']}/100")
    print(f"  Error rate: {result['grammar']['error_rate']} per sentence")
    print(f"  Errors: {result['grammar']['error_counts']}")
    
    print(f"\n📚 Vocabulary:")
    print(f"  Score: {result['vocabulary']['score']}/100")
    print(f"  Diversity: {result['vocabulary']['type_token_ratio']}")
    
    print(f"\n🎯 Overall:")
    print(f"  Score: {result['overall']['score']}/100")
    print(f"  Grade: {result['overall']['grade']}")
    print(f"  CEFR: {result['overall']['estimated_cefr']}")
    print(f"  Level: {result['overall']['level_description']}")
    
    print(f"\n💡 Recommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    
    print("\n" + "=" * 70)
    print("SIMPLE EVALUATION (backward compatible)")
    print("=" * 70)
    
    simple_result = evaluator.evaluate_simple(test_sentences)
    print(f"\nTotal sentences: {simple_result['total_sentences']}")
    print(f"Grammar score: {simple_result['grammar_score']}/100")
    print(f"Vocabulary score: {simple_result['vocabulary_score']}/100")
    print(f"CEFR level: {simple_result['estimated_cefr']}")
    print(f"Error counts: {simple_result['error_counts']}")