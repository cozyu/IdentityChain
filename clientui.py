import os
import sys
import time
import string
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry


import base64
import json

import nacl
import requests
from flask import Flask

exec(open("./Blockchain.py").read())

app = Flask(__name__)
nodes_w = None
nodes_list = None
pk_w = None
a_w = None

sk = None
pk = None
addresses_list = None

self_addr = "127.0.0.1"
self_port = "5000"


# global variables
# root
root = tk.Tk()
style = ttk.Style(root)
style.theme_use('clam')
candidateList = []


# tkEntry
uname = tk.Entry(root)
pword = tk.Entry(root)
pubKey = tk.Entry(root)
privKey = tk.Entry(root)
electionID = tk.Entry(root)
voteChoice = tk.Entry(root)
candidateEntry = tk.Entry(root)

startDate = Calendar(root)
endDate = Calendar(root)

# buttons
createElectionButton = tk.Button(root)
loginButton = tk.Button(root)
regButton = tk.Button(root)
voteButton = tk.Button(root)
voteScreenButton = tk.Button(root)
createAnElectionButton = tk.Button(root)
backButton = tk.Button(root)
calButton = tk.Button(root)


# labels
unameLabel = tk.Label(root)
pwordLabel = tk.Label(root)
pubKeyLabel = tk.Label(root)
privKeyLabel = tk.Label(root)
electionLabel = tk.Label(root)

# vars
username = StringVar()
password = StringVar()
senderPubKey = StringVar()
senderPrivKey = StringVar()
elecID = StringVar()
voteVar = StringVar()
candidate = StringVar()
electionName = StringVar()

def main():
    loginScreen()
    root.mainloop()


def loginScreen():
	root.geometry("500x500")
	root.title("Identity Chain Client v1.0")
	root.minsize(1000,800)
	tk.Label(root, text="Welcome to the Identity Chain Client", font='Helvetica 18 bold').pack()


	unameLabel = tk.Label(root, text="Username:")
	unameLabel.pack()

	uname = tk.Entry(root, textvariable = username)
	uname.pack()

	pwordLabel = tk.Label(root, text="Password:")
	pwordLabel.pack()

	pword = tk.Entry(root, show="*", textvariable = password)
	pword.pack()

	loginButton = tk.Button(root, text="Login", command=login)
	loginButton.pack()

	regButton = tk.Button(root, text="Register", command=regUser)
	regButton.pack()

def dashboard():
	clearView()
	hello = tk.Label(root, text=username.get()+ ", Welcome to the Indentity Chain Dashbaord\n\nChoose an action!\n---------------", font='Helvetica 18 bold')
	hello.pack()
	# button
	voteScreenButton = tk.Button(root, text="Go to Voting Dashboard", command=vote_dashboard)
	createAnElectionButton = tk.Button(root, text="Go to Election Dashboard", command=election_dashboard)
	voteScreenButton.pack()
	createAnElectionButton.pack()

def vote_dashboard():
	clearView()
	hello = tk.Label(root, text=username.get()+ ", Welcome to the Indentity Chain Voting Dashbaord\n\nCast a vote!\n---------------", font='Helvetica 18 bold')
	hello.pack()


	# labels
	pubKeyLabel = tk.Label(root, text=username.get()+"'s Public Key:")
	privKeyLabel = tk.Label(root, text=username.get()+"'s Private Key:")
	electionLabel = tk.Label(root, text="Election Key:")
	voteLabel = tk.Label(root, text="Select your Vote")
	
	# EntryBoxes
	pubKey = tk.Entry(root, textvariable = senderPubKey)
	privKey = tk.Entry(root, textvariable = senderPrivKey)
	electionID = tk.Entry(root, textvariable = elecID)
	voteChoice = tk.Entry(root, textvariable = voteVar)
	
	# clears fields
	pubKey.delete(0, END)
	privKey.delete(0, END)
	electionID.delete(0, END)
	voteChoice.delete(0, END)

	# button
	voteButton = tk.Button(root, text="Vote", command=vote)

	backButton = tk.Button(root, text="Back", command=dashboard)
	

	# display
	pubKeyLabel.pack()
	pubKey.pack()
	privKeyLabel.pack()
	privKey.pack()
	electionLabel.pack()
	electionID.pack()
	voteLabel.pack()
	voteChoice.pack()
	voteButton.pack()
	backButton.pack()


def election_dashboard():
	clearView()
	hello = tk.Label(root, text=username.get()+ ", Welcome to the Indentity Chain Election Dashbaord\n\nCreate an Election!\n---------------", font='Helvetica 18 bold')
	hello.pack()
	tk.Label(root, text='Election Name', font='Arial 18 bold').pack()
	tk.Entry(root, textvariable = electionName).pack()


	tk.Label(root, text='Choose Election Start Date', font='Arial 18 bold').pack()
	startDate = Calendar(root, font="Arial 14", selectmode='day', locale='en_US',disabledforeground='red')
	startDate.pack()

	tk.Label(root, text='\n\nChoose Election End Date', font='Arial 18 bold').pack()
	endDate = Calendar(root, font="Arial 14", selectmode='day', locale='en_US',disabledforeground='red', year=2020, month=5, day=21)
	endDate.pack()
	# labels
	tk.Label(root, text="Select Candidates").pack()
	candidateEntry = tk.Entry(root, textvariable = candidate)
	candidateEntry.delete(0, END)
	candidateEntry.pack()
	tk.Button(root, text="Add Candidate", command=addCandidate).pack()
	tk.Button(root, text="Create Election", command=createElection).pack()


def addCandidate():
	list = root.pack_slaves()
	list[-1].destroy()
	candidateList.append(candidate.get())
	tk.Label(root, text=candidate.get()).pack()
	tk.Button(root, text="Create Election", command=createElection).pack()

def createElection():
	print (electionName.get())
	print (startDate.get_date())
	print (endDate.get_date())
	print (candidateList)
	register = messagebox.showinfo("Thanks", "You have created an Election.")


def vote():
    SK = nacl.signing.SigningKey(senderPrivKey.get(), encoder=nacl.encoding.HexEncoder)
    j = {'sender': senderPubKey.get(),
        'recipient': elecID.get(),
        'amount': 0,
        'script': {'type':1,'vote':int(voteVar.get())}}

    msg = f'sender:{j["sender"]},recipient:{j["recipient"]},amount:{j["amount"]},script:{j["script"]}'
    sig = SK.sign(msg.encode())
    sig = sig[:len(sig) - len(msg)]
    j['signature'] = base64.b64encode(sig).decode()
    req = requests.post(f'http://{self_addr}:{self_port}/vote/new', json=j)
    print("Transaction: ", req.content.decode())
    messagebox.showinfo("", "Thanks, "+ username.get() +"! Your vote has been cast!")
    clearView()
    dashboard()

	

def checkLogin():
	try:
		f = open('users/' +username.get() + '.txt', 'r')
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

	pword = tk.Entry(root, show="*", textvariable = password)
	pword.pack()

	regButton = tk.Button(root, text="Register", command=saveUser)
	regButton.pack()
	
def saveUser():
	f = open('users/' + username.get() + '.txt', 'w')
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
