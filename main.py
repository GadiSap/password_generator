from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = ("Courier", 11)
EMAIL = "Add default email"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def password_generator():


    let = [choice(letters) for _ in range(randint(8, 10))]
    num = [choice(numbers) for _ in range(randint(2, 4))]
    sym = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = let + num + sym

    shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().lower()
    user = user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "user": user,
            "password": password,
        }
    }
    to_save = True
    if len(website) == 0:
        messagebox.showinfo(title="Input Error", message="Website field empty")
        to_save = False
    elif len(user) == 0:
        messagebox.showinfo(title="Input Error", message="User name/email field empty")
        to_save = False
    elif len(password) == 0:
        messagebox.showinfo(title="Input Error", message="Password field empty")
        to_save = False
    elif len(password) < 8:
        pass_short_ok = messagebox.askokcancel(title="Not Recommended", message="Password shorter than 8 characters.\nAre you sure you want to save?")
        if not pass_short_ok:
            to_save = False

    if to_save:

        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            user_entry.delete(0, END)
            password_entry.delete(0, END)
            user_entry.insert(0, EMAIL)

# ____________________________SEARCH __________________________________#

def search():
    website = website_entry.get().lower()
    if len(website) == 0:
        messagebox.showinfo(title="Input Error", message="Website field empty")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="File Error", message="No data file found")
        else:
            if website in data:
                user = data[website]["user"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"User Name: {user}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message="Password for this website does not exist")
        finally:
            website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas=Canvas(width=200, height=200, bg="white", highlightthickness=0)
mypass = PhotoImage(file= "logo.png")
canvas.create_image(100, 100, image=mypass)
canvas.grid(row=0, column= 1)

website_entry = Entry(width=31, borderwidth = 2)
website_entry.grid(row=1, column=1)

user_entry = Entry(width=49, borderwidth = 2)
user_entry.grid(row=2, column=1, columnspan=2)
user_entry.insert(0, EMAIL)

password_entry = Entry(width=31, borderwidth = 2)
password_entry.grid(row=3, column=1)

website_label = Label(text="Website:", bg="white", fg="black")
website_label.grid(row=1, column=0)
website_entry.focus()

user_label = Label(text="Email/Username:", bg="white", fg="black")
user_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg="white", fg="black")
password_label.grid(row=3, column=0)

add_button = Button(text="Add", bg="white", fg="black", width=42, command=save)
add_button.grid(row=4, column=1, columnspan=2)

generate_button = Button(text="Generate password", bg="white", fg="black", width=14, command=password_generator)
generate_button.grid(row=3, column=2)

search_button = Button(text="Search", bg="white", fg="black", width=14, command=search)
search_button.grid(row=1, column=2)






window.mainloop()