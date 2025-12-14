# -*- coding: utf-8 -*-
"""
Created on Wed July 25 17:26:51 2025
@author: ragha
"""
#to get a random unput &to add random strings like letters and numbers 
#calling library 
#and tkinter 
import random
import string
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox#call the box as a copied& show the error box



#anaylze password content #every case take a type from 1 to 4
#the oop class to recal the check fun
class passCheck:
    def __init__(self, password):
        self.password = password

    def check(self):
        types = 0#we use this bec its global
        if any(c.islower() for c in self.password):
            types += 1
        if any(c.isupper() for c in self.password):
            types += 1
        if any(c.isdigit() for c in self.password):
            types += 1
        if any(c in string.punctuation for c in self.password):
            types += 1
        return types


#the final test 
#concant between the lenght and the types for detiermine the strengh 
#functions to return what the password identy by the length 
    def length2(self):
        types = self.check()
        if len(self.password) <= 8 or types < 2:
            print("Weak Password")
            return "weak"
        elif 8 < len(self.password) < 10 and types >= 2:
            print("Good Password")
            return "good"
        elif 10 <= len(self.password) < 14 and types >= 3:
            print("Powerful Password")
            return "powerful"
        elif 12 <= len(self.password) < 16 and types == 4:
            print("Very Powerful Password")
            return "very_powerful"
        else:
            print("Too long Password")
            return "too_long"


# Class to suggest stronger passwords based on strength
class randoms_sugg:


#uses string w random.choices
#do a make the user enter a prop length###################################
#add a random digit by the diff cases 
    def suggest(self, password, suggestion):#suggestion is the strenght of the pass to know the sugg and what we add
        if suggestion == "weak":
            k = random.randint(3, 6)#make a random number from (letter, num , symbol)
            add = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=6))# a new patterns name is add #add 6 charcters from every thing
        elif suggestion == "good":
            k = random.randint(4, 8)
            add = ''.join(random.choices(string.ascii_uppercase + string.punctuation, k=k))#add only from big letters and symbols
        elif suggestion == "powerful":
            target_length = random.randint(12, 16)
            to_add = max(0, target_length - len(password))#to make the pass to 12-16 char 
            k = random.randint(to_add, to_add + 4)#see how many number we need
            add = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=k))#punctuation=  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        else:
            add = ''
        middle = len(password) // 2# count the middle of the 
        # add the symbols inside the password in random patterns  in the middle 
        return password[:middle] + add + password[middle:]


# Class to provide update reminder date
#sugg a date that is after 2 weeks for better securty
class update_reminder:
    def suggest_date(self):
        today = datetime.today()
        update_due_date = today + timedelta(weeks=2)
        return update_due_date.strftime('%Y-%m-%d')

class Password_all_page:
    def __init__(self, root):
        self.root = root
        root.title("Password Strength Tool By Raghad")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.center_window(screen_width // 2, screen_height // 2)



#input from the user
#enter a password
        tk.Label(root, text="Enter your password please ").pack(pady=10)# add a vertical padding by 10 pixsil using pady 


        self.password_entry = tk.Entry(root, width=20, show="*")#show the pass as a * to protect the password of being leak
        #w the max of 20 char 
        self.password_entry.pack(pady=5)

        self.show = False
        #the button to show the password 
        self.toggle_btn = tk.Button(root, text="Show password", command=self.toggle_password)
        self.toggle_btn.pack()

        self.analyze_button = tk.Button(root, text="Click me", command=self.analyze)#to execute the anaylze classby click on the bottom
        self.analyze_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", fg="gray")
        self.result_label.pack()

        self.suggestion_label = tk.Label(root, text="", fg="green", wraplength=480, justify="center")
        self.suggestion_label.pack(pady=5)

        self.copy_button = tk.Button(root, text="Click to copy", command=self.copy_password)
        self.copy_button.pack()
        self.copy_button.config(state=tk.DISABLED)#in first it be unable to click on it
        #but by entring an pass and suggest one it will be on

        self.update_label = tk.Label(root, text="")
        self.update_label.pack(pady=5)

        self.suggested = ""

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_password(self):
        if self.show:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="Show Password")
        else:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="Hide Password")
        self.show = not self.show

    def analyze(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        try:
            checker = passCheck(password)
            strength = checker.length2()
            self.result_label.config(text=f"Password strength: {strength.replace('_', ' ').capitalize()}")

            if strength in ["powerful","very_powerful", "too_long"]:
                self.open_next_page()

    #sugg a new pass
    #If the word is not very strong or too long, we suggest a 
    #stronger version by adding symbols in the middle.
            if strength not in ["very_powerful", "too_long"]:
                suggester = randoms_sugg()
                self.suggested = suggester.suggest(password, strength)
                self.suggestion_label.config(text=f"Suggested password: {self.suggested}")
                self.copy_button.config(state=tk.NORMAL)
            else:
                self.suggestion_label.config(text="Your password is strong enough!")
                self.copy_button.config(state=tk.DISABLED)

            updater = update_reminder()
            self.update_label.config(text=f"Update due date: {updater.suggest_date()}")

        except Exception as un_case:#unuasul case 
            messagebox.showerror("Error", str(un_case))

    def copy_password(self):
        if self.suggested:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.suggested)
            messagebox.showinfo("Copied success", "Suggested copied")

    def open_next_page(self):
        new_window = tk.Toplevel(self.root)
        new_window.title(" Passed ")
        new_window.geometry("700x100")
        tk.Label(new_window, text="THIS IS THE END OF MY PROJECT", font=("Arial",16)).pack(pady=20)


if __name__ == '__main__':
    root = tk.Tk()
   # root.iconbitmap("hacker_icon.ico")
    app = Password_all_page(root)
    root.mainloop()
