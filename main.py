from pronoun import *
from verb import Verb
from question import Question
from tense import *
import random
import datetime

# Still need to add basic error handling.
# Need to make user interface that also lets you select what verb tenses you want to practice.
# Get code to parse through igbo alphabet
# not sure if this is the correct way to set timer LOL


def parse_verbs(verb_list):
    file = open('sample_verbs.txt', 'r')
    lines = file.readlines()

    for line in lines:
        curr_verb = Verb(line.strip())
        verb_list.append(curr_verb)


def set_time():
    time = input("How long would you like to play? (in Minutes) ")  # no error handling
    return int(time)


def choose_tenses():
    pass


def select_question(verb_list):
    chosen_verb = random.choice(verb_list)
    chosen_tense = random.choice(TENSES)
    if chosen_tense == IMPERATIVE:
        chosen_pronoun = random.choice(IMPERATIVE_PRONOUNS)
    else:
        chosen_pronoun = random.choice(ALL_PRONOUNS)
    curr_question = Question(chosen_verb, chosen_tense, chosen_pronoun)
    curr_question.create_answer()
    return curr_question


def check_answer(question, answer):
    count = 0
    while answer not in question.answer_list:
        count += 1
        answer = input("Sorry the correct answer is " + ask.answer_list[0] + ". Please try again. ")
        answer = answer.lower()
    return count


def closing_statement(questions, correct):
    accuracy = 100 * float(correct)/float(questions)
    print("All done! You scored ", correct, " out of ", questions, ". Accuracy: ", accuracy, "%")


if __name__ == '__main__':
    verbs = []
    num_questions = 0
    num_correct = 0

    parse_verbs(verbs)
    timer = set_time()
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=timer)
    while datetime.datetime.now() < end_time:
        ask = select_question(verbs)
        response = input(ask.prompt)
        num_questions += check_answer(ask, response.lower())
        num_questions += 1
        num_correct += 1
    closing_statement(num_questions, num_correct)
