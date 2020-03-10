import base64
import json
from tkinter import *
import os
import nacl
import requests
from flask import Flask


#import modules

window = Tk()
window.title("ItsExceptional")
window.geometry("300x200")
window.config(background = "black", pady=10)


lb1 = Label(window, text = "Login Form", bg = "black", fg="white", font=20)
lb1.place(x=110, y=5)

lb2_u = Label(window, text = "Username - ", bg="black", fg="white")
lb2_u2 = Entry(window)
lb2_u.place(x=10, y=40)
lb2_u2.place(x=110, y=40)


lb2_p = Label(window, text = "Password - ", bg="black", fg="white")
lb2_p2 = Entry(window)
lb2_p.place(x=10, y=80)
lb2_p2.place(x=110,y=80)


display = Label(window, text="Access : ", bg="black")

bt = Button(window, text="Login")



def dis():
    user = lb2_u2.get()
    pas = lb2_p2.get()
    filo = open('register.txt').readlines()
    for lino in filo:
        if user == lino.split()[2]:
            display.config(bg="green",fg="white", text="Access :Granted")
            break
        else:
            display.config(bg="red",fg="white", text="Access :Denied")

bt.config(command=dis)
bt.place(x=110, y=120)


def newsign():
    sign=Tk()
    sign.title("SignUp")
    sign.geometry("300x200")
    sign.config(background = "black", pady=10)

    lbs = Label(sign, text = "SignUp", bg = "black", fg="white", font=20)
    lbs.place(x=110, y=5)

    lb2_s = Label(sign, text = "Username - ", bg="black", fg="white")
    lb2_s2 = Entry(sign)
    lb2_s.place(x=10, y=40)
    lb2_s2.place(x=110, y=40)


    lb2_ps = Label(sign, text = "Password - ", bg="black", fg="white")
    lb2_ps2 = Entry(sign)
    lb2_ps.place(x=10, y=80)
    lb2_ps2.place(x=110,y=80)

    dis = Label(sign, text ="", bg="black", fg="white")
    
    def reg():
        username = lb2_s2.get()
        pas = lb2_ps2.get()
        
        file =  open("register.txt","a")
        fiIn = open('register.txt').readlines()


        l=[] 
        for lines in fiIn:
            l.append(lines.split()[2])

        if username in l:
            print("Exists")
            dis.config(text="User Exists", bg="green")

        else:
            print("not Exists")
            file.write("Username = "+username+"\n")
            file.write("Password = "+pas+"\n")
            file.close()
            dis.config(text = "Registered", bg="green")
        
    bts = Button(sign, text="Register", command=reg)
    bts.place(x=110, y=120)
    dis.place(x=100, y=150)

    
    window.destroy()

bt2 = Button(window, text="SignUp", command=newsign)
bt2.place(x=170, y=120)


display.place(x=110, y=155)




# exec(open("./Blockchain.py").read())

# app = Flask(__name__)

# root = Tk()
# root.title("Identity Chain")
# root.geometry('700x500')

# nodes_w = None
# nodes_list = None
# pk_w = None
# a_w = None

# sk = None
# pk = None
# addresses_list = None

# self_addr = "127.0.0.1"
# self_port = "5000"

# try:
#     # blockchain.load_chain()
#     # blockchain.load_pending_tx()
#     pass
# except:
#     print("Could not load chain from file")
# finally:
#     pass
# address = ""


def save_blockchain():
    pass
    # blockchain.save_chain()
    # blockchain.save_pending_tx()


def load_blockchain():
    pass
    # blockchain.load_chain()
    # blockchain.load_pending_tx()


def send():
    address = send_pk.get()
    SK = nacl.signing.SigningKey(send_sk.get(), encoder=nacl.encoding.HexEncoder)
    j = {'sender': address,
         'recipient': send_entry.get(),
         'amount': float(send_amount.get())}
    msg = f'sender:{j["sender"]},recipient:{j["recipient"]},amount:{j["amount"]}'
    sig = SK.sign(msg.encode())
    sig = sig[:len(sig) - len(msg)]
    j['signature'] = base64.b64encode(sig).decode()
    req = requests.post(f'http://{self_addr}:{self_port}/transactions/new', json=j)
    print("Transaction: ", req.content.decode())
    # save_blockchain()
    # load_blockchain()


def save_nodes():
    f = open("nodes.dat", "w")
    lst = []
    lst = nodes_list.get(1.0, END).splitlines()
    json.dump(lst, f)
    f.close()


def load_nodes():
    file_object = open('nodes.dat', 'r')
    nodes = json.load(file_object)
    for e in nodes:
        nodes_list.insert(INSERT, e + "\n")


def discover_nodes():
    try:
        blockchain.discover_peers()
    except:
        print("Could not discover new nodes")


def nodes_window():
    nodes_w = Tk()
    nodes_w.title("List nodes")
    l = Label(nodes_w, text="List of nodes", font="Arial 14")
    global nodes_list
    nodes_list = Text(nodes_w)
    nodes_list_save_button = Button(nodes_w, command=save_nodes, text="Save list of nodes")
    nodes_discover_button = Button(nodes_w, command=discover_nodes, text="Discover new nodes")
    l.pack(pady=10)
    nodes_list.pack()
    nodes_list_save_button.pack(pady=10)
    nodes_discover_button.pack(pady=10)
    load_nodes()


def gen_pk():
    global sk
    sk = nacl.signing.SigningKey.generate()  # .encode(encoder=nacl.encoding.HexEncoder)
    global pk
    pk = sk.verify_key
    pk = pk.encode(encoder=nacl.encoding.HexEncoder)
    sk = sk.encode(encoder=nacl.encoding.HexEncoder)
    pk_list.insert(INSERT, "=PRIVATE=\n")
    pk_list.insert(INSERT, sk)
    pk_list.insert(INSERT, "\n=PUBLIC=\n")
    pk_list.insert(INSERT, pk)  # .encode(encoder=nacl.encoding.HexEncoder))
    pk_list.insert(INSERT, "\n\n")
    pass


def new_privkeys():
    pk_w = Tk()
    pk_w.title("Generate new private keys")
    l = Label(pk_w, text="Your private keys", font="Arial 14")
    global pk_list
    pk_list = Text(pk_w)
    pk_gen_new = Button(pk_w, command=gen_pk, text="Generate new private key")
    l.pack(pady=10)
    pk_list.pack()
    pk_gen_new.pack(pady=10)


# fileMenu = Menu(menubar)
# fileMenu.add_command(label="Save", command=save_blockchain)
# fileMenu.add_command(label="List nodes", command=nodes_window)
# menubar.add_cascade(label="File", menu=fileMenu)
# walletmenu = Menu(menubar)
# walletmenu.add_command(label="Generate private keys", command=new_privkeys)
# menubar.add_cascade(label="Wallet", menu=walletmenu)
# # Send section
# l1 = Label(text="Submit", font="Arial 14")
# l1.grid(column=1, row=0)

# lbl = Label(text="Recipient: ")
# lbl.grid(column=0, row=1)
# send_entry = Entry(width=50)
# send_entry.grid(column=1, row=1)

# lbl1 = Label(text="Amount: ")
# lbl1.grid(column=0, row=2)
# send_amount = Entry(width=50, text="Amount")
# send_amount.grid(column=1, row=2)

# lbl2 = Label(text="Public key: ")
# lbl2.grid(column=0, row=3)
# send_pk = Entry(width=50, text="Public key")
# send_pk.grid(column=1, row=3)

# lbl3 = Label(text="Private key: ")
# lbl3.grid(column=0, row=4)
# send_sk = Entry(width=50, text="Private key")
# send_sk.grid(column=1, row=4)

# send_button = Button(text="Submit", command=send)
# send_button.grid(column=1, row=5)

# nodes_w.mainloop()
