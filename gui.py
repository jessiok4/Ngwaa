import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
from tense import *
from style import *
from accents import *
from game import Game
from tooltip import CreateToolTip


class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # SETTING UP MAIN WINDOW
        self.title("Ngwaa")
        container = tk.Frame(self)
        self.geometry("650x500")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # STYLE #
        style = Style(theme="flatly")
        style.configure("TButton", font=BUTTON_FONT, background=BLUE, foreground=OFF_WHITE, )

        self.frames = {}
        self.time = 5  # default
        self.tenses = []

        for F in (HomePage, Settings, GamePage, Conclusion):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont == GamePage:
            self.frames[cont].init_game(self.time, self.tenses, self)

    def set_settings(self, time, tenses):
        self.time = time
        self.tenses = tenses

    def final_statement(self, correct, total_questions):
        try:
            accuracy = 100 * float(correct) / float(total_questions)
            accuracy = round(accuracy, 1)
        except ZeroDivisionError:
            self.frames[Conclusion].results.config(text=f"All done! You scored {0} out of {0}. Accuracy: {0}%")
        else:
            self.frames[Conclusion].results.config(text=f"All done! You scored {correct} out of {total_questions}. "
                                                        f"Accuracy: {accuracy}%")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # BACKGROUND IMAGE #
        img = Image.open("img/title_pg.png")
        resized_img = img.resize((650, 600))
        bg = ImageTk.PhotoImage(resized_img)
        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg

        # HEADER #
        header = ttk.Label(self, text="NGWAA",
                           font=HEADER_FONT,
                           background=BLUE,
                           foreground=OFF_WHITE,
                           padding=(17, 0, 0, 0),
                           anchor="w")
        header.pack(side="top", fill="both")

        # PLAY BUTTON #
        play_btn = ttk.Button(self, text="Play Game",
                              command=lambda: controller.show_frame(Settings))
        play_btn.place(relx=.5, rely=.605, anchor="center")


class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.selected_tenses = []
        self.selected_time = 5  # default

        # BACKGROUND IMAGE #
        img = Image.open("img/bg.png")
        resized_img = img.resize((650, 600))
        bg = ImageTk.PhotoImage(resized_img)
        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg

        # HEADER #
        header = ttk.Label(self, text="NGWAA",
                           font=HEADER_FONT,
                           background=BLUE,
                           foreground=OFF_WHITE,
                           padding=(17, 0, 0, 0),
                           anchor="w")
        header.pack(side="top", fill="both")

        # TENSES #
        tense_label = ttk.Label(self, text="Choose Tenses:",
                                font=MEDIUM_FONT,
                                anchor="w")
        tense_label.place(relx=.16, y=162, anchor="w")
        self.checkboxes = []
        for i in range(len(TENSES)):
            tense = tk.BooleanVar()
            checkbox = tk.Checkbutton(self, text=TENSES[i],
                                      variable=tense,
                                      onvalue=1,
                                      offvalue=0,
                                      font=SMALL_FONT,
                                      command=lambda index=i: self.set_tense(index)
                                      )
            checkbox.place(relx=.18, y=195 + (30 * i), anchor="w")
            self.checkboxes.append(tense)

        # TIMER #
        timer_label = ttk.Label(self, text="Set Timer:",
                                font=MEDIUM_FONT,
                                anchor="w")
        timer_label.place(relx=.57, y=162, anchor="w")

        self.minutes = ["1 Minute", "2 Minutes", "3 Minutes", "4 Minutes", "5 Minutes"]
        self.time_options = tk.StringVar(self)
        self.time_options.set(self.minutes[4])

        drop_box = tk.OptionMenu(self, self.time_options,
                                 *self.minutes,
                                 command=self.set_timer)
        drop_box.configure(background=WHITE, foreground=BLACK)
        drop_box.place(relx=.57, y=200, anchor="w")

        # START BUTTON #
        self.play_btn = ttk.Button(self, text="Start",
                                   state="disabled",
                                   command=lambda: [controller.set_settings(self.selected_time, self.selected_tenses),
                                                    controller.show_frame(GamePage)])
        self.play_btn.place(relx=.5, rely=.725, anchor="center")

    def set_tense(self, index):
        if self.checkboxes[index].get() == 1:
            self.selected_tenses.append(TENSES[index])
        elif self.checkboxes[index].get() == 0:
            self.selected_tenses.remove(TENSES[index])
        any_checked = (self.checkboxes[0].get() | self.checkboxes[1].get()
                       | self.checkboxes[2].get()) | self.checkboxes[3].get()
        if any_checked:
            self.play_btn.config(state="normal")
        else:
            self.play_btn.config(state="disabled")

    def set_timer(self, event):
        time = self.time_options.get()
        for i in range(len(self.minutes)):
            if time == self.minutes[i]:
                chosen = i + 1
                self.selected_time = chosen


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.game = Game()
        self.done = False

        # BACKGROUND IMAGE #
        img = Image.open("img/bg.png")
        resized_img = img.resize((650, 600))
        bg = ImageTk.PhotoImage(resized_img)
        self.bg_canvas = tk.Canvas(self, width=650, height=600)
        bg_label = self.bg_canvas.create_image(325, 250, anchor="center", image=bg)
        self.bg_canvas.place(x=325, y=300, anchor="center")
        self.bg_canvas.image = bg

        # HEADER #
        header = ttk.Label(self, text="NGWAA",
                           font=HEADER_FONT,
                           background=BLUE,
                           foreground=OFF_WHITE,
                           padding=(17, 0, 0, 0),
                           anchor="w")
        header.pack(side="top", fill="both")

        # SCORE #
        self.score_label = self.bg_canvas.create_text(16, 47,
                                                      text="0/0",
                                                      fill=OFF_WHITE,
                                                      anchor="nw",
                                                      font=HEADER_FONT)
        # TIMER #
        self.timer_label = self.bg_canvas.create_text(603, 47,
                                                      text="5:00",
                                                      fill=OFF_WHITE,
                                                      anchor="n",
                                                      font=HEADER_FONT)

        # QUESTION #
        self.qs_label = ttk.Label(
            self,
            anchor="center",
            wraplength=430,
            padding=0,
            justify=tk.CENTER,
            font=QUESTION_FONT
        )
        self.qs_label.place(relx=.5, y=150, anchor="n")

        # INPUT BOX #
        self.input_text = tk.Entry(
            self,
            width=30,
            font=INPUT_TEXT,
            justify=tk.CENTER
        )
        self.input_text.place(relx=.5, y=250, anchor="n")

        # ACCENTS #
        accent_frame = tk.Frame(self)
        accent_frame.place(relx=.5, y=300, anchor="n")

        for i in range(len(ACCENTS)):
            button = ttk.Button(
                accent_frame,
                text=ACCENTS[i],
                command=lambda index=i: self.add_accent(ACCENTS[index]),
            )
            accent_frame.columnconfigure(i, weight=1)
            button.grid(row=0, column=i, padx=10, ipady=0)
            CreateToolTip(button, text=f'Ctrl + {NON_ACCENTS[i]}')

        # FEEDBACK #
        self.feedback_label = ttk.Label(self, anchor="center",
                                        justify=tk.CENTER,
                                        wraplength=480,
                                        font=FEEDBACK_FONT,
                                        foreground="red")
        self.feedback_label.place(relx=.5, y=360, anchor="n")

        # SKIP BUTTON #
        skip_btn = ttk.Button(
            self,
            text="Skip",
            command=lambda: self.game.skip(self.input_text, self.qs_label, self.feedback_label)
        )
        skip_btn.place(relx=.07, y=445, anchor="n")

        # SUBMIT BUTTON #
        submit_btn = ttk.Button(
            self,
            text="Submit",
            command=lambda: self.game.check_answer(self.input_text, self.feedback_label, self.bg_canvas,
                                                   self.score_label, self.qs_label)
        )
        submit_btn.place(relx=.91, y=445, anchor="n")

        # SHORTCUTS #
        controller.bind("<Return>", lambda event, : self.game.check_answer(self.input_text,
                                                                           self.feedback_label, self.bg_canvas,
                                                                           self.score_label, self.qs_label))
        controller.bind("<Control-u>", lambda event, : self.add_accent(U_ACCENT))
        controller.bind("<Control-o>", lambda event, : self.add_accent(O_ACCENT))
        controller.bind("<Control-i>", lambda event, : self.add_accent(I_ACCENT))

    def init_game(self, time, tenses, controller):
        self.game.start_game(time, tenses, self.qs_label, self.feedback_label, self.timer_label,
                             self.input_text, self.score_label, self.bg_canvas, controller, Conclusion)

    def add_accent(self, accent):
        self.input_text.insert(tk.INSERT, accent)
        self.input_text.focus_set()


class Conclusion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # BACKGROUND IMAGE #
        img = Image.open("img/bg.png")
        resized_img = img.resize((650, 600))
        bg = ImageTk.PhotoImage(resized_img)
        bg_label = tk.Label(self, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg

        # HEADER #
        header = ttk.Label(self, text="NGWAA",
                           font=HEADER_FONT,
                           background=BLUE,
                           foreground=OFF_WHITE,
                           padding=(17, 0, 0, 0),
                           anchor="w")
        header.pack(side="top", fill="both")

        # RESULTS #
        self.results = ttk.Label(
            self,
            anchor="center",
            wraplength=430,
            padding=0,
            justify=tk.CENTER,
            font=HEADER_FONT,
            foreground=BLUE
        )
        self.results.place(relx=.5, y=165, anchor="n")

        # RESTART BUTTON #
        restart_btn = ttk.Button(
            self,
            text="Restart",
            command=lambda: controller.show_frame(GamePage)
        )
        restart_btn.place(relx=.35, y=302, anchor="n")

        # SETTINGS BUTTON #
        settings_btn = ttk.Button(
            self,
            text="Settings",
            command=lambda: controller.show_frame(Settings)
        )
        settings_btn.place(relx=.65, y=302, anchor="n")


app = Gui()
app.mainloop()
