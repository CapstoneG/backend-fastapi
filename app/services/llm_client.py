class LLMClient:

    def generate(self, prompt: str) -> dict:
        # MOCK RESPONSE
        return {
            "target_level": "B1",
            "top_weak_skills": ["verb_tense", "verb_pattern"],
            "learning_plan": [
                {
                    "day": 1,
                    "focus": "Past Simple",
                    "goal": "Talk about past events correctly",
                    "example": "I went to school yesterday.",
                    "exercise_type": "sentence_correction"
                },
                {
                    "day": 2,
                    "focus": "Present Perfect",
                    "goal": "Talk about experience",
                    "example": "I have learned English for 2 years.",
                    "exercise_type": "sentence_rewrite"
                }
            ]
        }
