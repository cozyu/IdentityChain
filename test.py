import os
import sys
import time
import string
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# global variables
root = tk.Tk()
uname = tk.Entry(root)
unameLabel = tk.Label(root)
pwordLabel = tk.Label(root)
pword = tk.Entry(root)
loginButton = tk.Button(root)
regButton = tk.Button(root)
username = StringVar()
password = StringVar()


def main():
    loginScreen()
    root.mainloop()


def loginScreen():
	root.geometry("500x500")
	root.title("Identity Chain Client v1.0")
	root.minsize(500,500)
	root.maxsize(500,500)
	tk.Label(root, text="Welcome to the Identity Chain Client").pack()


	unameLabel = tk.Label(root, text="Username:")
	unameLabel.pack()

	uname = tk.Entry(root, textvariable = username)
	uname.pack()

	pwordLabel = tk.Label(root, text="Password:")
	pwordLabel.pack()

	pword = tk.Entry(root, textvariable = password)
	pword.pack()

	loginButton = tk.Button(root, text="Login", command=login)
	loginButton.pack()

	regButton = tk.Button(root, text="Register", command=regUser)
	regButton.pack()

def dashboard():
	#welcome = messagebox.showinfo("Welcome", "Welcome, " + uname.get() + "!")

	hello = tk.Label(root, text="" + username.get()+ ", Welcome to the Indentity Chain Dashbaord")
	hello.pack()

	def switch_back():
		root.configure(bg="#f1f1f1")
		hello.configure(bg="#f1f1f1")

	def switchColor():
		global color
		color = root.cget('bg')
		root.configure(bg="#887345")
		hello.configure(bg="#887345")

		if color == "#887345":
			root.after(1, switch_back)

	switch = tk.Button(root, text="Switch", command=switchColor)
	switch.pack()

def checkLogin():
	try:
		f = open(username.get() + '.txt', 'r')
		data = f.readlines()
		getUname = data[0].rstrip()
		getPword = data[1].rstrip()

		if username.get() == getUname and password.get() == getPword:
			clearView()
			dashboard()
			f.close()
		else:
			error = messagebox.showerror("Error", "Password incorrect.")
			clearView()
			loginScreen()

	except IOError:
		error = messagebox.showerror("Error", "User does not exist.")
		root.destroy()

def login():
	checkLogin()

def regUser():
	clearView()
	unameLabel = tk.Label(root, text="Username:")
	unameLabel.pack()

	uname = tk.Entry(root, textvariable = username)
	uname.pack()

	pwordLabel = tk.Label(root, text="Password:")
	pwordLabel.pack()

	pword = tk.Entry(root, textvariable = password)
	pword.pack()

	regButton = tk.Button(root, text="Register", command=saveUser)
	regButton.pack()
	
def saveUser():
	f = open(username.get() + '.txt', 'w')
	f.write(username.get())
	f.write("\n")
	f.write(password.get())
	f.close()
	register = messagebox.showinfo("Welcome", "You have registered.")
	clearView()
	loginScreen()

def clearView():
    list = root.pack_slaves()
    for l in list:
    	l.destroy()

if __name__ == "__main__":
    main()