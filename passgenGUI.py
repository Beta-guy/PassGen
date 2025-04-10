#imports
import random
from tkinter import messagebox, Tk, Entry, Label, Checkbutton, IntVar, Button
import csv
import pathlib

#collecting Information
def save_input():
    site_value = site.get()
    username_value = username.get()
    char_lists = ""
    if special_val.get() == 1:
        char_lists += spe
    if low_val.get() == 1:
        char_lists += low
    if upp_val.get() == 1:
        char_lists += upp
    if num_val.get() == 1:
        char_lists += numbers
    if space_val.get() == 1:
        char_lists += spa
    password = ""
    max_value = max_text.get()
    if max_value == '':
        max_value = 12
    elif max_value.isnumeric() == 0:
        messagebox.showinfo("Type Error", "Numbers only please!")
    else:
        max_value = int(max_text.get())
    if char_lists == "":
        char_lists = upp+low+numbers+spe
    for num in range(int(max_value)):
        password += random.choice(char_lists)
    default_row = ["Application", "Username", "Password"]
    csv_row = [site_value, username_value, password]
    file = pathlib.Path('password.csv').is_file()
    if file == True:
        with open('password.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_row)
    else:
        with open('password.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(default_row)
            writer.writerow(csv_row)
#defining list types
low = "abcdefghijklmnopqrstuvwxyz"
upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
spe = "!@#$%^&*()-+<>?"
spa = " "

#GUI Fun!
root = Tk()
#rnd title
title = random.sample(low+upp+numbers+spe+spa, k=12)
root.title(title)

#window size
root.geometry("500x200")
# get Site Name
site = Entry(root, width=30)
site.place(x=20, y=20)
site_label = Label(root, text="Site or Application")
site_label.place(x=280, y=20)
#get username
username = Entry(root, width=30)
username.place(x=20, y=70)
username_label = Label(root, text="Username or Email Address")
username_label.place(x=280, y=70)
#get Password length
max_text = Entry(root, width=3)
max_text.place(x=20, y=120)
max_label = Label(root, text="Password Length")
max_label.place(x=60, y=120)
#get password attributes
special_val = IntVar()
special = Checkbutton(root, text="Special Chars?", variable=special_val)
special.place(x=280, y=100)

low_val = IntVar()
low_check = Checkbutton(root, text="Lowercase?", variable=low_val)
low_check.place(x=160, y=120)

upp_val = IntVar()
upp_check = Checkbutton(root, text="Uppercase?", variable=upp_val)
upp_check.place(x=160, y=100)

num_val = IntVar()
num_check = Checkbutton(root, text="Numbers?", variable=num_val)
num_check.place(x=400, y=120)

space_val = IntVar()
space = Checkbutton(root, text="Space Chars?", variable=space_val)
space.place(x=280, y=120)

button = Button(root, text="Generate Password", command=save_input)
button.place(x=180, y=160)

root.mainloop()

