from tense import *


class Verb:
    def __init__(self, infinitive):
        self.infinitive = infinitive
        self.__e_group = self.__check_group()  # boolean
        self.imperative = self.__create_imperative()
        self.past = self.__create_past()
        self.pres_n_fut = self.__create_pres_n_fut()

    """ The function below checks the first letter of the infinitive verb
    to determine whether the verb is apart of the 'e' group or 'a' group. 
    If the word starts with an i, then it's apart of the 'e' group.
    """
    def __check_group(self):
        return self.infinitive[0] == 'i'

    """ The function below transforms the Igbo infinitive verb 
    into the imperative tense.
    """
    def __create_imperative(self):
        imperative = self.infinitive[1:]  # Need to handle root ending in u or o
        if len(imperative) <= 2:
            if self.__e_group:
                imperative = imperative + 'e'
            else:
                imperative = imperative + 'a'
        return imperative

    """ The function below transforms the Igbo infinitive verb 
    into the past tense. This works for most but not all verbs.
    """
    def __create_past(self):
        past = self.infinitive[1:]
        second_to_last = past[-2:-1]
        if second_to_last != 'r' or len(past) <= 2:
            suffix = "r" + past[-1]
            past = past + suffix
        return past

    """ The function below transforms the Igbo infinitive verb 
    into the base for present & future tense. This works for most 
    but not all verbs.
    """
    def __create_pres_n_fut(self):
        future = self.infinitive[1:]
        if self.__e_group:
            future = 'e' + future
        else:
            future = 'a' + future
        return future

    """ The function below returns the second half of the solution to the
    prompted question.
    """
    def get_answer(self, tense):
        if tense == PRESENT or tense == FUTURE:
            return self.pres_n_fut
        elif tense == PAST:
            return self.past
        else:
            return self.imperative
