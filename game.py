import codecs
import random
import time
import tkinter as tk
import threading

from verb import Verb
from tense import *
from pronoun import *
from question import Question


class Game:
    def __init__(self):
        self.verbs = []
        self.parse_verbs()
        self.tenses = []
        self.questions = []
        self.time = 5  # default
        self.score = 0
        self.num_asked = 0

    def parse_verbs(self):
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
                    self.verbs.append(curr_verb)

    def start_game(self, selected_time, tenses, qs_label, feedback, timer_label,
                   input_txt, score_label, canvas, controller, conclusion):
        canvas.itemconfig(score_label, text="0/0")
        self.time = selected_time
        self.tenses = tenses
        self.score = 0
        self.num_asked = 0
        self.questions.clear()
        self.select_question()
        thread1 = threading.Thread(target=self.start_timer,
                                   args=(controller, conclusion, timer_label, canvas), daemon=True)
        thread1.start()
        self.show_question(qs_label, feedback, input_txt)

    def select_question(self):
        chosen_verb = random.choice(self.verbs)
        chosen_tense = random.choice(self.tenses)
        if chosen_tense == IMPERATIVE:
            chosen_pronoun = random.choice(IMPERATIVE_PRONOUNS)
        else:
            chosen_pronoun = random.choice(ALL_PRONOUNS)
        question = Question(chosen_verb, chosen_tense, chosen_pronoun)
        question.create_answer()
        self.questions.append(question)  # may need to change

    def check_answer(self, input_txt, feedback, canvas, score_label, qs_label):
        # done = False
        inp = input_txt.get()
        inp.lower().strip()

        if inp not in self.questions[self.score].answer_list:
            feedback.config(text=f"Sorry the correct answer is {self.questions[self.score].answer_list[0]}."
                            f" Please try again.")
            self.num_asked += 1
            canvas.itemconfig(score_label, text="{}/{}".format(self.score, self.num_asked))
        else:
            self.score += 1
            self.num_asked += 1
            canvas.itemconfig(score_label, text="{}/{}".format(self.score, self.num_asked))
            self.select_question()
            self.show_question(qs_label, feedback, input_txt)

    def show_question(self, qs_label, feedback, input_txt):
        qs_label.config(text=self.questions[self.score].prompt)
        feedback.config(text="")
        input_txt.delete(0, tk.END)

    def skip(self, input_txt, qs_label, feedback):
        self.questions.pop()
        self.select_question()
        self.show_question(qs_label, feedback, input_txt)

    def start_timer(self, controller, conclusion, timer_label, canvas):
        t = self.time * 60
        while t:
            mins, secs = divmod(t, 60)
            clock = '{:01d}:{:02d}'.format(mins, secs)
            canvas.itemconfig(timer_label, text=clock)
            time.sleep(1)
            t -= 1
        controller.final_statement(self.score, self.num_asked)
        controller.show_frame(conclusion)
