from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Variables
timer = None
counter = False
remaining_time = 0
loop = 1
my_tik = ""


# ---------------------------- TIMER RESET ------------------------------- #
def stop_timer():
    global counter, timer
    if timer is not None:
        window.after_cancel(timer)
    counter = False
    start_button.config(text="continue", command=continue_timer)


def reset_timer():
    global counter, my_tik, loop, timer

    if remaining_time != 0:
        counter = False
        if timer is not None:
            window.after_cancel(timer)
        canvas.itemconfig(time_config, text="00:00", fill="white")
        start_button.config(text="start", command=start_timer)

        my_label.config(text="Timer", fg=GREEN)
        my_tik = ""
        my_label2.config(text=my_tik)
        loop = 1
    elif not counter:
        return


# ---------------------------- TIMER MECHANISM ------------------------------- #
def continue_timer():
    global remaining_time, counter
    count_down(remaining_time)
    counter = True
    start_button.config(text="stop", command=stop_timer)


def start_timer():
    global counter, loop, remaining_time

    # Changed * 1 to * 60 to convert minutes to seconds properly
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    counter = True
    start_button.config(text="stop", command=stop_timer)

    if loop % 8 == 0:
        my_label.config(text="Break", fg=RED)
        canvas.itemconfig(time_config, fill=RED)
        count_down(long_break_sec)
    elif loop % 2 == 0:
        my_label.config(text="Break", fg=PINK)
        canvas.itemconfig(time_config, fill=PINK)
        count_down(short_break_sec)
    else:
        canvas.itemconfig(time_config, fill=GREEN)
        my_label.config(text="Work", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global counter, loop, my_tik, timer, remaining_time
    remaining_time = count

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    if count_min == 0:
        count_min = "00"
    elif int(count_min) < 10:
        count_min = f"0{int(count_min)}"

    canvas.itemconfig(time_config, text=f"{count_min}:{count_sec}")

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        loop += 1
        if loop % 2 == 0:
            my_tik += "✔"
            my_label2.config(text=my_tik)
        counter = False
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("pomodoro")
window.config(padx=100, pady=100, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# Added a try/except block just in case the image is missing, so the app won't completely crash
try:
    tomato_image = PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=tomato_image)
except TclError:
    print("Warning: tomato.png not found. UI will load without the background image.")

canvas.grid(column=1, row=1)
time_config = canvas.create_text(103, 132, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

my_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 32, "bold"))
my_label.grid(column=1, row=0)

start_button = Button(text="start", font=("Classic", 15), fg=RED, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="reset", font=("Classic", 15), fg=RED, command=reset_timer)
reset_button.grid(column=2, row=2)

my_label2 = Label(fg=GREEN, bg=YELLOW, font=("Classic", 20))
my_label2.grid(column=1, row=3)

window.mainloop()