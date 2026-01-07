import json

class PromptBuilder:

    def build(self, skill_summary: dict) -> str:
        prompt = {
            "role": "english_learning_coach",
            "task": "generate_learning_plan",
            "constraints": {
                "duration_days": 7,
                "style": "conversation_first",
                "output_format": "JSON_ONLY"
            },
            "user_profile": {
                "current_level": skill_summary["estimated_cefr"],
                "target_level": "B1",
                "grammar_score": skill_summary["grammar_score"],
                "vocabulary_score": skill_summary["vocabulary_score"],
                "top_weak_skills": list(skill_summary["error_counts"].keys())
            },
            "schema": {
                "learning_plan": [
                    {
                        "day": "int",
                        "focus": "string",
                        "goal": "string",
                        "example": "string",
                        "exercise_type": "string"
                    }
                ]
            }
        }
        return json.dumps(prompt, indent=2)
