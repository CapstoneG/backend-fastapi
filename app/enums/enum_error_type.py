from enum import Enum

class ErrorType(str, Enum):
    VERB_TENSE = "verb_tense"
    VERB_PATTERN = "verb_pattern"
    AGREEMENT = "agreement"
    PREPOSITION = "preposition"
    ADJECTIVE_FORM = "adjective_form"