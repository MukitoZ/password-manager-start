from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    entry_password.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]
    random.shuffle(password_list)

    password = "".join(password_list)
    entry_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def password_saver():
    website = entry_website.get().title()
    username = entry_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": username,
            "password": password
        }
    }
    if website == "" or username == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            entry_website.focus()


def find_password():
    website = entry_website.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File Found")
    else:
        if website in data:
            email_password = data[website]
            messagebox.showinfo(title=website, message=f"Email: {email_password['email']}\n"
                                                       f"Password: {email_password['password']}")
        else:
            messagebox.showwarning(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text="Website:")
label_website.grid(column=0, row=1, sticky="w")
label_username = Label(text="Email/Username:")
label_username.grid(column=0, row=2, sticky="w")
label_password = Label(text="Password:")
label_password.grid(column=0, row=3, sticky="w")

# Entries
entry_website = Entry(width=48)
entry_website.grid(column=1, row=1, columnspan=2, sticky="w")
entry_website.focus()
entry_username = Entry(width=68)
entry_username.insert(0, "your_email@mail.com")
entry_username.grid(column=1, row=2, columnspan=2, sticky="w")
entry_password = Entry(width=48)
entry_password.grid(column=1, row=3, sticky="w")

# Buttons
button_search = Button(text="Search", width=15, command=find_password)
button_search.grid(column=2, row=1, sticky="w")
button_generate_password = Button(text="Generate Password", width=15, command=generate_password)
button_generate_password.grid(column=2, row=3, sticky="w")
button_add = Button(text="Add", width=58, command=password_saver)
button_add.grid(column=1, row=4, columnspan=2, sticky="w")

window.mainloop()
