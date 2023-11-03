import random

FIRST_PERSON_SING = "mu"
SECOND_PERSON_SING = "gi"
THIRD_PERSON_SING = "ya"
FIRST_PERSON_PLU = "anyi"
SECOND_PERSON_PLU = "unu"
THIRD_PERSON_PLU = "ha"


class Pronoun:
    def __init__(self):
        self.chosen = ""
        self.__pronouns = [FIRST_PERSON_SING, SECOND_PERSON_SING, THIRD_PERSON_SING,
                         FIRST_PERSON_PLU, SECOND_PERSON_PLU, THIRD_PERSON_PLU]

    def pick_pronoun(self):
        self.chosen = random.choice(self.__pronouns)
        return self.chosen

    def get_answer(self, tense):  # Answer has to be checked before a new question is asked.
        pass
