from tkinter import Tk, Canvas, PhotoImage, Button
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
timer = None


def random_word():
    global current_word, timer

    window.after_cancel(timer)

    current_word = random.choice(words)
    card.itemconfig(card_img, image=french_card_img)
    card.itemconfig(language, text="French", fill="black")
    card.itemconfig(word, text=current_word["French"], fill="black")

    timer = window.after(3000, flip)


def flip():
    global current_word

    card.itemconfig(card_img, image=english_card_img)
    card.itemconfig(language, text="English", fill="white")
    card.itemconfig(word, text=current_word["English"], fill="white")


def learned():
    global current_word, words

    words.remove(current_word)
    print(len(words))
    random_word()


if __name__ == '__main__':
    # GUI
    window = Tk()
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    window.title('Flashy')

    # Flash card
    card = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
    french_card_img = PhotoImage(file='./images/card_front.png')
    english_card_img = PhotoImage(file="./images/card_back.png")
    card_img = card.create_image(400, 263, image=french_card_img)
    language = card.create_text(400, 150, text='title', font=('Arial', 40, 'italic'))
    word = card.create_text(400, 263, text='word', font=('Arial', 60, 'bold'))
    card.grid(column=0, row=0, columnspan=2)

    # Buttons
    wrong_img = PhotoImage(file='./images/wrong.png')
    wrong_button = Button(image=wrong_img, highlightthickness=0, borderwidth=0, command=random_word)
    wrong_button.grid(column=0, row=1)

    right_img = PhotoImage(file='./images/right.png')
    right_button = Button(image=right_img, highlightthickness=0, borderwidth=0, command=learned)
    right_button.grid(column=1, row=1)

    # ACCESSING FILE
    try:
        words_df = pandas.read_csv('./data/to_learn.csv')
    except FileNotFoundError:
        words_df = pandas.read_csv('./data/french_words.csv')
    words = words_df.to_dict(orient='records')

    timer = window.after(3000, flip)
    random_word()

    window.mainloop()

    data = pandas.DataFrame(words)
    data.to_csv("./data/to_learn.csv", index=False)
