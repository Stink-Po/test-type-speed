import customtkinter
from customtkinter import *
import database
from sqlalchemy.orm import sessionmaker
import random
import time
import math

my_font1 = ('times', 18, 'bold')
my_font2 = ('times', 20, 'bold')
timer_font = ('Arial', 34, 'bold')
count_down_font = ('Arial', 50, 'bold')
data = database.Database
Session = sessionmaker(bind=database.engine)
session = Session()


# our database have 5 row we gaet a random number between 1 and 5
# and use it to have a random test
def run_test():
    random_number = random.randint(1, 5)
    test = session.query(data).filter(data.id == random_number).first()
    return test


class UserInterFace:

    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.window = CTk()
        self.window.title("Typing Speed Test Application")
        self.window.resizable(False, False)
        self.window.config(padx=50, pady=50)
        self.window.geometry("1000x700")
        self.test = run_test()
        self.wrong_entry = 0
        self.correct_entry = 0
        self.test_running = True
        self.start_count = 5
        self.key_press_count = 0
        self.start_test_btn = None
        self.timer = None
        self.start_test_time = None
        self.end_test_time = None
        self.final_output = None
        self.test_gain_btn = CTkButton(master=self.window,
                                       text="Test Again",
                                       command=lambda: self.start_time(),
                                       height=100,
                                       width=300,
                                       font=my_font1)
        self.user_input = []
        self.get_ready_label = CTkLabel(master=self.window,
                                        font=timer_font,
                                        text="Get ready Test will be start in :",
                                        text_color="#609EA2")
        self.count_down_label = CTkLabel(master=self.window,
                                         font=count_down_font,
                                         text=str(self.start_count),
                                         text_color="#820000")
        self.label_test = CTkLabel(master=self.window,
                                   font=my_font2,
                                   text="",
                                   wraplength=900,
                                   )

        self.best_score_record = CTkLabel(master=self.window,
                                          font=my_font1,
                                          text_color="#609EA2",
                                          text="")
        self.type_area = CTkTextbox(master=self.window,
                                    width=900,
                                    height=200,
                                    )
        self.type_area.bind('<KeyRelease>', self.count_press)
        self.main()
        self.window.mainloop()

    # save the starting test time and if there is a past record will show the user
    # create a label with test text
    # create textbox for type
    def start_test(self, test):
        self.start_test_time = time.time()
        self.get_ready_label.grid_forget()
        self.count_down_label.grid_forget()
        test_text = test.text
        test_record = test.record
        self.label_test.configure(text=test_text)
        if test_record == 0:
            test_record = "No Record Yet"
        else:
            test_record = f"Best Record : {test_record}"
        self.best_score_record.configure(text=test_record)
        self.best_score_record.grid(row=0, column=0)
        self.label_test.grid(row=1, column=0, pady=(20, 0))
        self.type_area.grid(row=2, column=0, pady=(20, 0))
        self.type_area.focus_set()

    # create a start button in screen and if user click the btn test will be start in 5 second
    def main(self):
        self.start_test_btn = CTkButton(master=self.window,
                                        text="Start Test",
                                        command=lambda: self.start_time(),
                                        height=100,
                                        width=300,
                                        font=my_font1)
        self.start_test_btn.grid(row=0, column=0, padx=(300, 0), pady=(250, 0))

    # show the 5-second countdown in screen for to get ready for the test
    def start_time(self):
        if self.start_count >= 0:
            self.start_test_btn.grid_forget()
            self.get_ready_label.grid(row=0, column=0, pady=(50, 100), padx=(200, 0))
            self.count_down_label.grid(row=1, column=0, padx=(200, 0))
            self.count_down_label.configure(text=self.start_count)
            self.start_count -= 1
            self.timer = self.window.after(1000, self.start_time)
        else:
            self.window.after_cancel(self.timer)
            self.start_test(self.test)

    # check user entry with test text and count wrong entry and showing them to user
    def tset_user_text(self, test_text, user_text):
        test_text_list = list(test_text)
        user_text_list = list(user_text)
        print(len(user_text))
        if len(test_text_list) <= len(user_text_list):
            self.test_running = False
            self.end_test_time = time.time()
            for n in range(len(test_text_list)):
                if test_text_list[n] == user_text_list[n]:
                    self.correct_entry += 1
                else:
                    self.wrong_entry += 1
            final_time = math.floor(self.end_test_time - self.start_test_time)

            if self.test.record != 0:
                if final_time < self.test.record:

                    self.final_output = f"Test is done you got {self.wrong_entry} wrong entry" \
                                        f"and you finish the test in {final_time} you catch the" \
                                        f"new record now"
                    # here we have new record for test this final time will add in database as a new best record
                    # btw i now in future I must add a new column in database for wrong entry
                    # and if user have for etc. more than 10 wrong entry we don't count the final record
                    session.query(data).filter(data.id == self.test.id).update({"record": final_time})
                    session.commit()

                else:
                    self.final_output = f"Test is done you got {self.wrong_entry} wrong entry" \
                                        f"and you finish the test in {final_time} our best record" \
                                        f"is {self.test.record}"

            else:
                self.final_output = f"Test is done you got {self.wrong_entry} wrong Entry and" \
                                    f"you own the new record of this test now your record is" \
                                    f"{final_time}"
                # because we don't have a new record here add final time as a new record in database
                session.query(data).filter(data.id == self.test.id).update({"record": final_time})
                session.commit()

    # a function for binding the keypress on keyboard for counting user keyboard key press
    #  and also check the final of the test
    def count_press(self, event):
        self.user_input = self.type_area.get("1.0", END)
        if len(self.user_input) >= len(self.test.text) or self.key_press_count >= len(self.test.text):
            self.tset_user_text(self.test.text, self.user_input)
            return
        self.key_press_count += 1

    # showing score to user and ask user to start a new test
    def draw_final_screen(self, final):
        self.best_score_record.grid_forget()
        self.label_test.grid_forget()
        self.type_area.grid_forget()
        self.get_ready_label.configure(text=final)
        self.get_ready_label.grid(row=0, column=0, pady=(50, 100), padx=(200, 0))
        self.test_gain_btn.grid(row=1, column=0, padx=(300, 0), pady=(250, 0))
