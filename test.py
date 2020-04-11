import base64
import json
from tkinter import *

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


def save_blockchain():
    pass
    # blockchain.save_chain()
    # blockchain.save_pending_tx()


def load_blockchain():
    pass
    # blockchain.load_chain()
    # blockchain.load_pending_tx()


def sendVote(address, SK, recipientPublicKey, amount):
    SK = nacl.signing.SigningKey(SK, encoder=nacl.encoding.HexEncoder)
    j = {'sender': address,
         'recipient': recipientPublicKey,
         'amount': float(amount)}
    msg = f'sender:{j["sender"]},recipient:{j["recipient"]},amount:{j["amount"]}'
    sig = SK.sign(msg.encode())
    sig = sig[:len(sig) - len(msg)]
    j['signature'] = base64.b64encode(sig).decode()
    req = requests.post(f'http://{self_addr}:{self_port}/transactions/new', json=j)
    print("Transaction: ", req.content.decode())
    # save_blockchain()
    # load_blockchain()

def send():
    address = senderPublicKey.get()
    SK = nacl.signing.SigningKey(senderPrivateKey.get(), encoder=nacl.encoding.HexEncoder)
    j = {'sender': address,
         'recipient': recipientPublicKey.get(),
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


# Add test method calls from here --- Jack will build out corresponding UI
bobPubKey = '15c0486a008d3d8e0f920222df7d18215d90c2cfa489f133a7a583e04c575007'
bobPrivKey = 'f4483f68ded20a9907cb3b8c348524f4d238c1b162471d4591c3705e56d15301'
alicePublicKey = '9e933a6f4142ac06d2625625747ac117ef3998e9d2a8fef4f578ddc5e18e6908'

sendVote(bobPubKey, bobPrivKey, alicePublicKey, 10)


