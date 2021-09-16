from tkinter import *
from tkinter import messagebox 
import string
import random
import threading


root = Tk()
root.geometry("400x300")
root.title("Password Generator")
root.iconbitmap("icon.ico")
root.resizable(0,0)

var = StringVar()
var1 =IntVar()



def random_colors():
	colors = ["RED","BLUE","GREEN","PINK","YELLOW","LIGHTBLUE","GREY","LIGHTGREEN","ORANGE","GOLD"]
	randomc = random.choice(colors)
	label["bg"] = randomc


def generate():
	get = var1.get()
	words =string.ascii_lowercase
	symbols = string.punctuation 
	nums = string.digits
	

	combination = words+symbols +nums
	password = ''.join(random.choice(combination) for i in range(get))
	if len(password) < 8:
		mb = messagebox.showinfo("WARNING","PASSWORD CANT BE LESS THAN 8 CHARACTERS!")
	else:	
		entry1.insert(END,f"{password}")
		button1["command"] = clear
		random_colors()
		x =len(password)
		label1["text"] = f"Password Length is: {x}"

def clear():
	var.set("")
	button1["command"] = generate




label = Label(root,text="Double tap to generate new passwords",bg="lightgreen",font=("ARIAL 15"))

entry1 = Entry(root,width=60,textvariable=var,bg="lightblue",font=("ARIAL 10 bold"))

button1 = Button(root,text="Generate",command=generate)


entry2 = Entry(root,width=8,textvariable=var1)

label1 = Label(root,text=f"Password Length is: 0",font=("ARIAL 15 bold"))


label.pack(pady=10)
entry1.pack(pady=10)
entry2.pack(pady=10)
button1.pack()
label1.pack()

root.mainloop()
