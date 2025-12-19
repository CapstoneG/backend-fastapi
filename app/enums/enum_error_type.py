from enum import Enum

class ErrorType(str, Enum):
    GRAMMAR = "grammar"
    TENSE = "tense"
    ARTICLE = "article"
    PREPOSITION = "preposition"
    VOCABULARY = "vocabulary"
    SPELLING = "spelling"
    WORD_CHOICE = "word_choice"