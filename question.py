

class Question:

    def __int__(self, verb, tense, pronoun):
        self.verb = verb
        self.tense = tense
        self.pronoun = pronoun
        self.prompt = "Conjugate " + self.pronoun + ' ' + self.verb.infinitive + " in " + self.pronoun + " tense."

    def get_answer(self):
        pass
