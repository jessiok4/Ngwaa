from accents import *


class Verb:
    def __init__(self, infinitive):
        self.infinitive = infinitive
        self.e_group = self.__check_group()  # boolean
        self.imperative = self.__create_imperative()
        self.past = self.__create_past()
        self.future = self.__create_future()
        self.present = self.__create_present()

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
        imperative = self.infinitive[1:]
        if len(imperative) <= 2:
            if self.e_group:
                imperative = imperative + 'e'
            elif imperative[1] == 'u' or imperative[1] == 'o':
                imperative = imperative + 'o'
            elif imperative[1] == U_ACCENT or imperative[1] == O_ACCENT:
                imperative = imperative + O_ACCENT
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
    into the future tense. This works for most but not all verbs.
    """
    def __create_future(self):
        future = self.infinitive[1:]
        if self.e_group:
            future = 'e' + future
        else:
            future = 'a' + future
        future = "ga " + future
        return future

    """ The function below transforms the Igbo infinitive verb 
    into the present tense. This works for most but not all verbs.
    """
    def __create_present(self):
        present = self.infinitive[1:]
        if self.e_group:
            present = 'e' + present
        else:
            present = 'a' + present
        present = "na " + present
        return present
