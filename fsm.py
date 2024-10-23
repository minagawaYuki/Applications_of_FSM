import customtkinter

customtkinter.set_appearance_mode("dark")

class Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        label = customtkinter.CTkLabel(self, text="New Quiz")
        button = customtkinter.CTkButton(self, text="Start")

        label.grid(row=1, column=0, padx=0, pady=0)
        button.grid(row=2, column=0, padx=0, pady=0)


class QuizSystem(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.app = customtkinter.CTk()
        self.app.title("Finite State Machine")
        self.app.geometry("500x500")

        self.set_state('main_window')
        self.app.mainloop()

    def load_questions(self, subject):

        if subject == 'automata':
            self.title = "Automata Theory"
            self.questions = {
                'What does DFA stands for?': 'Non-deterministic Finite Automata',
                'Also called the start state.': 'Initial state',
                'A mathematical model of computation. It is an abstract machine that can be in exactly one of a finite number of states at any given time.': "Finite-state machine"
            }
        else:
            self.title = "Quantitative Analysis"
            self.questions ={
                'The process of drawing meaningful information from raw data.': 'Quantitative Analysis',
                'The chance of an event happening.': 'Probability',
                'What do you call the probability of a single event happening?': "Simple Probability"
            }

        self.review_questions = self.questions.copy()

        self.score = 0
        self.set_state('initialize')

    def main_window(self):
        for widget in self.app.winfo_children():
            widget.grid_forget()
        
        self.app.grid_columnconfigure((0), weight=1)
        self.app.rowconfigure((0, 1), weight=1)
        
        title_label = customtkinter.CTkLabel(self.app, text="Welcome to the Quiz App!", font=('Arial', 28))
        title_label.grid(row=0, column=0, padx=20)

        frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        frame.grid(row=1, column=0, padx=20, sticky="n")
        
        label = customtkinter.CTkLabel(frame, text="New Quiz")
        button = customtkinter.CTkButton(frame, text="Start", command=lambda: self.set_state('select'))

        label.grid(row=1, column=0, padx=0, pady=15)
        button.grid(row=2, column=0, padx=0, pady=0)
        

    def select_subject(self):
        for widget in self.app.winfo_children():
            widget.grid_forget()

        self.app.grid_columnconfigure((0), weight=1)
        self.app.rowconfigure((0, 1), weight=1)

        title_label = customtkinter.CTkLabel(self.app, text="Welcome to the Quiz App!", font=('Arial', 28))
        title_label.grid(row=0, column=0)

        frame = customtkinter.CTkFrame(self.app, fg_color="transparent", width=155, height=155)
        frame.grid(row=1, column=0, padx=20, sticky="n")

        frame_title = customtkinter.CTkLabel(frame, text="Available subjects")
        frame_title.grid(row=0, column=0, sticky="ew")

        subject_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
        subject_frame.grid(row=1, column=0)

        automata_title = customtkinter.CTkButton(subject_frame, text="Automata Theory", command=lambda: self.set_state('load', subject='automata'))
        automata_title.grid(row=0, column=0, padx=20, pady=20)

        quantitative_title = customtkinter.CTkButton(subject_frame, text="Quantitative Analysis", command=lambda: self.load_questions('quantitative'))
        quantitative_title.grid(row=1, column=0, padx=20, pady=0)

    def initialize_quiz(self):

        if len(self.questions) == 0:
            self.set_state('end')
            return

        for widget in self.app.winfo_children():
            widget.grid_forget()
        
        self.app.grid_columnconfigure((0), weight=1)
        self.app.rowconfigure((0, 1, 2, 3), weight=1)

        title_label = customtkinter.CTkLabel(self.app, text=self.title, font=('Arial', 35))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        frame = customtkinter.CTkFrame(self.app)
        frame.grid_columnconfigure((0), weight=1)
        frame.grid(row=1, column=0, padx=135, pady=20, sticky="new")

        self.item = self.questions.popitem()

        question_label = customtkinter.CTkLabel(frame, text=self.item[0])
        question_label.grid(row=0, column=0, padx=20, pady=20)

        entry = customtkinter.CTkEntry(frame, placeholder_text=f"Answer: {self.item[1]}")
        entry.grid(row=1, column=0, padx=155, sticky="ew")

        self.error_label = customtkinter.StringVar(frame)
        self.error_label.set("")

        error = customtkinter.CTkLabel(frame, textvariable=self.error_label)
        error.grid(row=2, column=0, pady=5)

        submit = customtkinter.CTkButton(frame, text="Submit", command=lambda: self.set_state('check', entry=entry.get()))
        submit.grid(row=3, column=0, pady=20, sticky="n")

        skip = customtkinter.CTkButton(self.app, text="Skip", command=lambda: self.set_state('skip'))
        skip.grid(row=3, column=0, sticky="n")

    def skip_question(self):
        self.set_state('initialize')

    def check_entry(self, entry):
        if entry == self.item[1]:
            self.score += 1
            print("Correct answer")
            self.set_state('initialize')
            return

        self.error_label.set("Incorrect answer.")
        print(entry)

    def end_quiz(self):
        for widget in self.app.winfo_children():
            widget.grid_forget()

        title_label = customtkinter.CTkLabel(self.app, text="You finished the quiz!", font=('Arial', 35))
        title_label.grid(row=0, column=0, padx=20, pady=20)

        frame = customtkinter.CTkFrame(self.app, fg_color="transparent")
        frame.grid(row=1, column=0)

        score_label = customtkinter.CTkLabel(frame, text=f"You scored {self.score} out of {len(self.review_questions)} questions!")
        score_label.grid(row=0, column=0)

        review = customtkinter.CTkButton(frame, text="Review", command=lambda: self.set_state('review'))
        review.grid(row=1, column=0, pady=15)

    def review_quiz(self):
        for widget in self.app.winfo_children():
            widget.grid_forget()

        self.app.grid_columnconfigure((0), weight=1)
        

        title_label = customtkinter.CTkLabel(self.app, text="Review Quiz", font=('Arial', 35))
        title_label.grid(row=0, column=0, padx=20, pady=20)

        item_count = 1

        for key, value in self.review_questions.items():
            frame = customtkinter.CTkFrame(self.app)
            frame.grid_columnconfigure((0), weight=1)
            frame.grid(row=item_count, column=0, sticky='new')

            question_label = customtkinter.CTkLabel(frame, text=key)
            question_label.grid(row=0, column=0, sticky='ew')

            answer_label = customtkinter.CTkLabel(frame, text=f"Answer: {value}")
            answer_label.grid(row=1, column=0, sticky='ew')

            item_count += 1

        new_quiz = customtkinter.CTkButton(self.app, text="New Quiz", command=lambda: self.set_state('main_window'))
        new_quiz.grid(row=item_count, column=0, pady=20)

    def set_state(self, state, **kwargs):
        if state == 'main_window':
            self.main_window()
        elif state == 'initialize':
            self.initialize_quiz()
        elif state == 'load':
            self.load_questions(kwargs['subject'])
        elif state == 'select':
            self.select_subject()
        elif state == 'skip':
            self.initialize_quiz()
        elif state == 'check':
            self.check_entry(kwargs['entry'])
        elif state == 'review':
            self.review_quiz()
        else:
            self.end_quiz()

QuizSystem()