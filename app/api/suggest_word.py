from fastapi import FastAPI
from pydantic import BaseModel
import json
from fastapi import APIRouter
from app.services.suggest_word_service import SuggestWordService

class WordRequest(BaseModel):
    word: str

class WordResponse(BaseModel):
    synonyms: list[str]
    explanation: str

class WordTranslateRequest(BaseModel):
    word: str

class WordTranslateResponse(BaseModel):
    translated_word: str

class FlashcardRequest(BaseModel):
    word: str

class FlashcardResponse(BaseModel):
    term: str
    phonetic: str
    definition: str
    partOfSpeech: str
    exampleSentence: str

class ScoreWritingRequest(BaseModel):
    title: str
    description: str
    content: str

class ScoreWritingResponse(BaseModel):
    grammarScore: float
    grammarFeedback: str
    vocabularyScore: float
    vocabularyFeedback: str
    coherenceScore: float
    coherenceFeedback: str
    contentScore: float
    contentFeedback: str
    overallScore: float
    improvements: list[str]

route = APIRouter(prefix="/api", tags=["Suggest Word"])
suggest_word_service = SuggestWordService()

@route.post("/suggest-words", response_model=WordResponse)
def suggest_words(request: WordRequest):
    raw_content = suggest_word_service.suggest_words(request.word)
    print("Raw content from AI:", raw_content)  # Debug log
    try:
        json_content = json.loads(raw_content)
        return WordResponse(
            synonyms=json_content.get("synonyms", []),
            explanation=json_content.get("explanation", "")
        )
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)  # Debug log
        raise ValueError("Failed to parse AI response as JSON")
    
@route.post("/translate-word", response_model=WordTranslateResponse)
def translate_word(request: WordTranslateRequest):
    translated_word = suggest_word_service.translate_word(request.word)
    try:
        translated_word = json.loads(translated_word)
        return WordTranslateResponse(translated_word=translated_word.get("translation", "Error"))
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)  # Debug log
        raise ValueError("Failed to parse AI response as JSON")
    
@route.post("/generate-flashcards", response_model=list[FlashcardResponse])
def generate_flashcards(request: FlashcardRequest):
    raw_content = suggest_word_service.generate_flashcards_prompt(request.word)
    print("Raw content from AI:", raw_content)  # Debug log
    raw_content = strip_markdown_json(raw_content)
    try:
        json_content = json.loads(raw_content)
        flashcards = [
            FlashcardResponse(
                term=card.get("term", ""),
                phonetic=card.get("phonetic", ""),
                definition=card.get("definition", ""),
                partOfSpeech=card.get("partOfSpeech", ""),
                exampleSentence=card.get("exampleSentence", "")
            ) for card in json_content.get("flashcards", [])
        ]
        return flashcards
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)  # Debug log
        raise ValueError("Failed to parse AI response as JSON")

@route.post("/score-writing", response_model=ScoreWritingResponse)
def score_writing(request: ScoreWritingRequest):
    raw_content = suggest_word_service.score_writing_prompt(
        title=request.title,
        description=request.description,
        content=request.content
    )
    print("Raw content from AI:", raw_content)  # Debug log
    raw_content = strip_markdown_json(raw_content)
    try:
        json_content = json.loads(raw_content)
        return ScoreWritingResponse(
            grammarScore=json_content.get("grammarScore", 0),
            grammarFeedback=json_content.get("grammarFeedback", ""),
            vocabularyScore=json_content.get("vocabularyScore", 0),
            vocabularyFeedback=json_content.get("vocabularyFeedback", ""),
            coherenceScore=json_content.get("coherenceScore", 0),
            coherenceFeedback=json_content.get("coherenceFeedback", ""),
            contentScore=json_content.get("contentScore", 0),
            contentFeedback=json_content.get("contentFeedback", ""),
            overallScore=json_content.get("overallScore", 0),
            improvements=json_content.get("improvements", [])
        )
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)  # Debug log
        raise ValueError("Failed to parse AI response as JSON")    

def strip_markdown_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        lines = lines[1:-1]  # bỏ ```json và ```
        return "\n".join(lines)

    return text