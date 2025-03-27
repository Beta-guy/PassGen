#imports

from tkinter import messagebox, Tk, Entry, Label, Checkbutton, IntVar, Button, ttk, Toplevel
import csv, pathlib, random, platform
import base64,os,tkinter,atexit
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

system = platform.system()
vaultpass = ""
salt = os.urandom(16)
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
    global system
    match system:
        case 'Linux':
            if file:
                with open('password.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(csv_row)
            else:
                with open('password.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(default_row)
                    writer.writerow(csv_row)
        case 'Windows':
            if file:
                with open('password.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(csv_row)
            else:
                with open('password.csv', 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(default_row)
                    writer.writerow(csv_row)
#save and close (compress csv file and delete original csv file)
def close():
    global vaultpass
    encrypt_file(vaultpass, "password.csv", "password.csv")
    exit()

def get_fernet_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust iterations as needed
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_file(password, filepath, output_filepath):
    salt = os.urandom(16)
    key = get_fernet_key(password, salt)
    cipher = Fernet(key)
    try:
        with open(filepath, "rb") as file:
            plaintext = file.read()
            ciphertext = cipher.encrypt(plaintext)
    except FileNotFoundError as e:
        print("File will be created.")
        ciphertext = cipher.encrypt(plaintext)

    with open(output_filepath, "wb") as file:
        file.write(salt + ciphertext)


def decrypt_file(password, filepath, output_filepath):
    with open(filepath, "rb") as file:
        data_with_salt = file.read()
        salt = data_with_salt[:16]
        data = data_with_salt[16:]
        key = get_fernet_key(password, salt)
        cipher = Fernet(key)

        plaintext = cipher.decrypt(data)

    with open(output_filepath, "wb") as file:
        file.write(plaintext)

def vault_window():
    secondary_window = Toplevel(root)
    secondary_window.title("Vault Password")
    secondary_window.config(width=300, height=150)
    secondary_window.attributes('-topmost', True)
    global vaultpass
    userpass = ttk.Entry(secondary_window, show='*')
    vaultpass = userpass.get()
    userpass.place(x=65, y=50)
    userpass_label = ttk.Label(secondary_window, text="Enter Vault Password")
    userpass_label.place(x=80, y=25)
    button_close = ttk.Button(
        secondary_window,
        text="Ok",
        command=lambda: unlock_vault(secondary_window))
    button_close.place(x=110, y=100)

def unlock_vault(secondary_window):
    global vaultpass
    try:
        decrypt_file(vaultpass, "password.csv", "password.csv")
    except:
        tkinter.messagebox.showinfo("Error", "File not Encrypted")
    secondary_window.destroy()


#defining list types
low = "abcdefghijklmnopqrstuvwxyz"
upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "1234567890"
spe = "!@#$%^&*()-+<>?"
spa = ' '

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
num_check.place(x=280, y=120)

button = Button(root, text="Generate Password", command=save_input)
button.place(x=100, y=160)

button = Button(root, text="Save & Close", command=close)
button.place(x=280, y=160)
root.after(50, vault_window())
atexit.register(close)
root.mainloop()


