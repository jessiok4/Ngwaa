from pronoun import Pronoun
from verb import Verb
from tense import *
import random

# Still need to add error handling.


def parse_verbs(verb_list):
    file = open('sample_verbs.txt', 'r')
    lines = file.readlines()

    for line in lines:
        curr_verb = Verb(line.strip())
        verb_list.append(curr_verb)


def set_time():
    time = input("How long would you like to play? (in Minutes)")  # no error handling
    return int(time)


def choose_tenses():
    pass


def select_question(verb_list, pro):
    chosen_verb = random.choice(verb_list)
    pro.pick_pronoun()
    chosen_tense = random.choice(TENSES)
    question = "Conjugate " + pro.chosen + ' ' + chosen_verb.infinitive + " in " + chosen_tense + " tense."
    return question


def check_answer():
    pass


if __name__ == '__main__':
    verbs = []
    pronouns = Pronoun()
    num_questions = 0
    num_correct = 0

    parse_verbs(verbs)
    timer = set_time()
    curr_prompt = select_question(verbs, pronouns)
    response = input(curr_prompt)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
