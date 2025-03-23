#imports
from tkinter import *
import subprocess
import sys
import random
#collecting Information
def save_input():
    system = sys.platform
    site_value = site.get()
    username_value = username.get()
    max_value = max_text.get()
    match max_value:
        case "":
            max_value = "12"
        case type("test"):
            messagebox.showinfo("Password Length", "Invalid Password Length")
            exit(0)
        case _:
            max_value = max_text.get()
    special_value = special_val.get()
    match special_value:
        case 1:
            special_value = "yes"
        case 0:
            special_value = "no"
#defining list types
low = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
upp = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
num = [1,2,3,4,5,6,7,8,9,0]
spe = ["!","@","#","$","%","^","&","*","(",")","?","<",">"]
spa = [" "]
#GUI Fun!
root = Tk()
#rnd title
title = random.sample(low+upp+num+spe+spa, k=12)
root.title(title)

#window size
root.geometry("500x200")

site = Entry(root, width=30)
site.place(x=20, y=20)
site_label = Label(root, text="Site or Application")
site_label.place(x=280, y=20)

username = Entry(root, width=30)
username.place(x=20, y=70)
username_label = Label(root, text="Username or Email Address")
username_label.place(x=280, y=70)

max_text = Entry(root, width=3)
max_text.place(x=20, y=120)
max_label = Label(root, text="Password Length")
max_label.place(x=60, y=120)

special_val = IntVar()
special = Checkbutton(root, text="Special Chars?", variable=special_val)
special.place(x=280, y=120)


button = Button(root, text="Generate Password", command=save_input)
button.place(x=180, y=160)

root.mainloop()
