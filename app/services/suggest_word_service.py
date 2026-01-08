import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', '')
from app.core.ai_provider import get_gemini_provider

class SuggestWordService:
    def __init__(self):
        self.client = get_gemini_provider(GEMINI_API_KEY, GEMINI_MODEL)

    def suggest_words(self, word: str) -> str:
        prompt = f"""
            You are a JSON API.

            Return ONLY a valid JSON object.
            Do NOT include markdown, code blocks, comments, or any extra text.
            Only 3 synonyms are needed.
            The JSON schema MUST be:
            {{
            "synonyms": string[],
            "explanation": string
            }}

            Rules:
            - Output must start with '{{' and end with '}}'
            - Use double quotes only
            - No trailing commas
            - No additional keys

            Word: "{word}"
        """
        return self.client.generate_text(prompt)
    
    def translate_word(self, word: str) -> str:
        prompt = f"""
            You are a JSON API.

            Return ONLY a valid JSON object.
            Do NOT include markdown, code blocks, comments, or any extra text.
            The JSON schema MUST be:
            {{
                "translation": string,
            }}

            Rules:
            - Output must start with '{{' and end with '}}'
            - Use double quotes only
            - No trailing commas
            - No additional keys

            Translate the word "{word}" into Vietnamese.
        """
        return self.client.generate_text(prompt)

    def generate_flashcards_prompt(self, texts: list[str]) -> str:
        joined_texts = "\n".join(f"- {t}" for t in texts)

        prompt = f"""
        You are a vocabulary extraction API.

        Your task is to extract important English vocabulary from a LIST of input texts.
        Select words that are useful for English learners.
        Avoid very basic or common words.

        Return ONLY valid JSON.
        No markdown, no explanations, no extra text.

        JSON schema (must match exactly):
        {{
        "flashcards": [
            {{
            "term": "string",
            "phonetic": "string",
            "definition": "string",
            "partOfSpeech": "string",
            "exampleSentence": "string"
            }}
        ]
        }}

        Rules:
        - Use double quotes only
        - Output must start with "{{" and end with "}}"
        - Provide 5–10 flashcards TOTAL (not per text)
        - Do not duplicate terms
        - Phonetic must be in IPA format (e.g. /ˈkɒn.sept/)
        - Definition must be in simple English
        - Example sentence must be clear and natural
        - Vocabulary can be extracted from ANY text in the list

        Input texts:
        \"\"\"
        {joined_texts}
        \"\"\"
        """.strip()

        print("Flashcard Prompt:\n", prompt)  # Debug log
        return self.client.generate_text(prompt)

    def score_writing_prompt(self, title: str, description: str, content: str) -> str:
        prompt = f"""
        You are an English writing assessment API.

        Evaluate the writing based on the title, description, and content.
        Check relevance, clarity, coherence, grammar, and vocabulary.

        Return ONLY a valid JSON object.
        Do NOT include markdown, explanations, or extra text.

        JSON schema:
        {{
            "grammarScore": number,
            "grammarFeedback": string,
            "vocabularyScore": number,
            "vocabularyFeedback": string,
            "coherenceScore": number,
            "coherenceFeedback": string,
            "contentScore": number,
            "contentFeedback": string,
            "overallScore": number,
            "improvements": string[]
        }}

        Scoring rules:
        - All scores must be between 0 and 9
        - overallScore must be the average of all scores, rounded to 1 decimal
        - Feedback must be concise and actionable
        - Improvements must contain 2–5 clear suggestions

        Writing input:

        Title:
        \"\"\"
        {title}
        \"\"\"

        Description:
        \"\"\"
        {description}
        \"\"\"

        Content:
        \"\"\"
        {content}
        \"\"\"
        """
        return self.client.generate_text(prompt)
