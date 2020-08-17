"""
    FACT:
        question can be anything;
        answer is None

    SIMPLE:
        question can be anything;
        there are many correct answers for the question;
        answer cannot be None

    GAPS:
        question has to contain one or many '___' as an answer field;
        there is only one correct answer for the type_in question

    MULTIPLE_CHOICE:
        question can be anything;
        there can be any number of correct answers

    RADIOBUTTON:
        question can be anything;
        there is exactly one correct answer and others are incorrect
"""

FACT = 0
SIMPLE = 1
GAPS = 2
MULTIPLE_CHOICE = 3
RADIOBUTTON = 4
