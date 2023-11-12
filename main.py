import threading
import codecs
from pronoun import *
from verb import Verb
from question import Question
from tense import *
import random
import time

# Need to make user interface that also lets you select what verb tenses you want to practice.
# not sure if this is the correct way to set timer LOL

"""
Further down the line goal, get program to allow you to add the accent 
marks if you don't have the proper keyboard
"""

""" 
Consider doing *thing from CS 161* that improves algorithm speed. 
Thing that prevents you from resolving something you've already solved.
Stores the solved information somewhere that's accessible
"""


def parse_verbs(verb_list):
    with codecs.open('sample_verbs.txt', encoding='utf-8') as f:
        for line in f:
            infinitive = line.strip()
            try:
                assert len(infinitive) > 2
                assert infinitive[0] == 'i' or infinitive[0] == '\u1ECB'
            except AssertionError:
                continue
            else:
                curr_verb = Verb(infinitive)
                verb_list.append(curr_verb)


def set_time():
    while True:
        minutes = input("How long would you like to play? (in Minutes) ")  # no error handling
        try:
            minutes = int(minutes)
        except ValueError:
            print("Enter a valid number.")
            continue
        else:
            break
    return minutes


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
        answer = input(f"Sorry the correct answer is {question.answer_list[0]}. Please try again. ")
        answer = answer.lower()
    return count


def start_timer(minutes):
    t = minutes*60
    while t:
        mins, secs = divmod(t, 60)
        clock = '{:02d}:{:02d}'.format(mins, secs)
        # print(clock, end="\r")
        time.sleep(1)
        t -= 1


def play_game(verb_list, questions, correct):
    for _ in range(5):
        ask = select_question(verb_list)
        response = input(ask.prompt)
        questions += check_answer(ask, response.lower())
        questions += 1
        correct += 1
    return questions, correct


def closing_statement(questions, correct):
    try:
        accuracy = 100 * float(correct)/float(questions)
    except ZeroDivisionError:
        print(f"All done! You scored {0} out of {0}. Accuracy: {0}%")
    else:
        print(f"All done! You scored {correct} out of {questions}. Accuracy: {accuracy}%")


if __name__ == '__main__':
    verbs = []
    num_questions = 0
    num_correct = 0

    parse_verbs(verbs)
    timer = set_time()
    # start_timer(timer)

    # thread1 = threading.Thread(target=start_timer, args=(timer,))
    # thread2 = threading.Thread(target=play_game, daemon=True, args=(verbs, num_questions, num_correct))
    # thread1.start()
    # thread2.start()
    # thread1.join()

    num_questions, num_correct = play_game(verbs, num_questions, num_correct)
    closing_statement(num_questions, num_correct)
