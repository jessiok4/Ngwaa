from tense import *
from pronoun import *


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
            solution = "\u1ECB " + conjugation
        answer.append(solution)

    def third_person_conj(self, conjugation, answer):
        if self.verb.e_group:
            solution = "o " + conjugation
        else:
            solution = "\u1ECD " + conjugation
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

    def get_present(self):
        answer = []
        if self.pronoun == FIRST_PERSON_SING:
            self.first_person_conj(self.verb.present[:2], answer)
            answer = [conjugation + self.verb.present[2:] for conjugation in answer]
        elif self.pronoun == SECOND_PERSON_SING:
            self.second_person_conj(self.verb.present, answer)
        elif self.pronoun == THIRD_PERSON_SING:
            self.third_person_conj(self.verb.present, answer)
        else:
            solution = self.pronoun + ' ' + self.verb.present
            answer.append(solution)
        return answer

    def get_future(self):
        answer = []
        if self.pronoun == FIRST_PERSON_SING:
            self.first_person_conj(self.verb.future[:2], answer)
            answer = [conjugation + self.verb.future[2:] for conjugation in answer]
        elif self.pronoun == SECOND_PERSON_SING:
            self.second_person_conj(self.verb.future, answer)
        elif self.pronoun == THIRD_PERSON_SING:
            self.third_person_conj(self.verb.future, answer)
        else:
            solution = self.pronoun + ' ' + self.verb.future
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
            answer_list = self.get_present()

        elif self.tense == FUTURE:
            answer_list = self.get_future()

        else:
            answer_list = self.get_imperative()
        self.answer_list = answer_list
