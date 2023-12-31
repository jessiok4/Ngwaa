from tense import *
from pronoun import *
from accents import *


class Question:
    def __init__(self, verb, tense, pronoun):
        self.verb = verb
        self.tense = tense
        self.pronoun = pronoun
        self.prompt = "Conjugate '" + self.pronoun + ' ' + self.verb.infinitive + "' in " + self.tense + " tense. "
        self.answer_list = []

    def first_person_conj(self, conjugation, answer):
        if self.verb.e_group and self.tense == PAST:
            solution = "e " + conjugation + " m"
            answer.append(solution)
            solution = "e " + conjugation + 'm'
            answer.append(solution)
            solution = 'e' + conjugation + 'm'
            answer.append(solution)
        else:
            solution = "a " + conjugation + " m"
            answer.append(solution)
            solution = "a " + conjugation + 'm'
            answer.append(solution)
            solution = 'a' + conjugation + 'm'
            answer.append(solution)

    def second_person_conj(self, conjugation, answer):
        if self.verb.e_group:
            solution = "i " + conjugation
        else:
            solution = f"{I_ACCENT} {conjugation}"
        answer.append(solution)

    def third_person_conj(self, conjugation, answer):
        if self.verb.e_group:
            solution = "o " + conjugation
        else:
            solution = f"{O_ACCENT} {conjugation}"
        answer.append(solution)

    def get_past(self):
        answer = []
        if self.pronoun == FIRST_PERSON_SING:
            self.first_person_conj(self.verb.past, answer)
        elif self.pronoun == SECOND_PERSON_SING:
            self.second_person_conj(self.verb.past, answer)
        elif self.pronoun == THIRD_PERSON_SING:
            self.third_person_conj(self.verb.past, answer)
        else:
            solution = self.pronoun + ' ' + self.verb.past
            answer.append(solution)
        return answer

    def get_pres_fut(self, tense):
        answer = []
        if self.pronoun == FIRST_PERSON_SING:
            self.first_person_conj(tense[:2], answer)
            answer = [conjugation + tense[2:] for conjugation in answer]
        elif self.pronoun == SECOND_PERSON_SING:
            self.second_person_conj(tense, answer)
        elif self.pronoun == THIRD_PERSON_SING:
            self.third_person_conj(tense, answer)
        else:
            solution = self.pronoun + ' ' + tense
            answer.append(solution)
        return answer

    def get_imperative(self):
        answer = []
        solution = self.verb.imperative + ' ' + self.pronoun
        answer.append(solution)
        if self.pronoun == FIRST_PERSON_SING:
            solution = self.verb.imperative + 'm'
            answer.append(solution)
            solution = self.verb.imperative + ' m'
            answer.append(solution)
        return answer

    def create_answer(self):  # Answer has to be checked before new question is asked
        if self.tense == PAST:
            answer_list = self.get_past()

        elif self.tense == PRESENT:
            answer_list = self.get_pres_fut(self.verb.present)

        elif self.tense == FUTURE:
            answer_list = self.get_pres_fut(self.verb.future)

        else:
            answer_list = self.get_imperative()
        self.answer_list = answer_list
