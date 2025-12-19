def calculate_toeic_score(listening_correct: int, reading_correct: int) -> dict:
    def convert_score(correct, section_type):
        if correct <= 0: return 5
        if correct >= 100: return 495
        
        base = 5
        multiplier = 4.95 if section_type == 'listening' else 4.85 
        
        score = int(base + (correct * multiplier))
        return min(round(score / 5) * 5, 495)

    l_score = convert_score(listening_correct, 'listening')
    r_score = convert_score(reading_correct, 'reading')
    
    return {
        "listening": l_score,
        "reading": r_score,
        "total": l_score + r_score
    }