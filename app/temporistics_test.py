from typing import List, Dict
from collections import Counter

# Simple questionnaire used to infer a Temporistics type.
# Each question offers four options, each corresponding to a time aspect.
# The answer key associates option letters with aspects.
TEMPORISTICS_QUESTIONS: List[Dict[str, Dict[str, str]]] = [
    {
        "question": "When planning important decisions you are guided mostly by:",
        "options": {
            "A": {"aspect": "Past", "text": "Past experience"},
            "B": {"aspect": "Current", "text": "Present circumstances"},
            "C": {"aspect": "Future", "text": "Future possibilities"},
            "D": {"aspect": "Eternity", "text": "Timeless principles"},
        },
    },
    {
        "question": "Which perspective best matches your everyday thinking?",
        "options": {
            "A": {"aspect": "Past", "text": "Recollections"},
            "B": {"aspect": "Current", "text": "Here and now"},
            "C": {"aspect": "Future", "text": "Plans"},
            "D": {"aspect": "Eternity", "text": "Philosophical ideas"},
        },
    },
    {
        "question": "What motivates you most?",
        "options": {
            "A": {"aspect": "Past", "text": "Traditions"},
            "B": {"aspect": "Current", "text": "Immediate needs"},
            "C": {"aspect": "Future", "text": "Long‑term goals"},
            "D": {"aspect": "Eternity", "text": "Eternal values"},
        },
    },
    {
        "question": "Choose the statement that resonates with you:",
        "options": {
            "A": {"aspect": "Past", "text": "History repeats"},
            "B": {"aspect": "Current", "text": "Live for today"},
            "C": {"aspect": "Future", "text": "The best is ahead"},
            "D": {"aspect": "Eternity", "text": "Timeless truth"},
        },
    },
]

ASPECT_ORDER = ["Past", "Current", "Future", "Eternity"]

def calculate_temporistics_type(answers: List[str]) -> str:
    """Return a temporistics type from provided answers.

    Parameters
    ----------
    answers: List[str]
        List of option letters corresponding to ``TEMPORISTICS_QUESTIONS``.

    Returns
    -------
    str
        Comma-separated string of aspects ordered from most to least frequent.
    """
    if len(answers) != len(TEMPORISTICS_QUESTIONS):
        raise ValueError("Number of answers does not match questions")

    counts = Counter()
    for answer, question in zip(answers, TEMPORISTICS_QUESTIONS):
        option = question["options"].get(answer.upper())
        if not option:
            raise ValueError(f"Invalid answer: {answer}")
        counts[option["aspect"]] += 1

    # Sort aspects by frequency, falling back to predefined ASPECT_ORDER
    sorted_aspects = sorted(
        ASPECT_ORDER,
        key=lambda a: (-counts[a], ASPECT_ORDER.index(a))
    )
    return ", ".join(sorted_aspects)
