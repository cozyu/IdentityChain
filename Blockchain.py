import hashlib
import json
from time import time
from urllib.parse import urlparse

from flask import Flask, jsonify, request
from uuid import uuid4
import requests

node_identifier = str(uuid4()).replace('-', '')

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = []
    def new_block(self, proof, previous_hash=None, time_stamp=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time_stamp or time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    @property
    def last_block(self):
        return self.chain[-1]
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.append(parsed_url.netloc)
    def validate_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
            return True
    def resolve_conflicts(self):
        print("resolving conflicts")
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.validate_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def receive_pending_tx(self):
        print("receiving pending txs from nodes")
        neighbours = self.nodes
        for node in neighbours:
            response = requests.get(f'http://{node}/pending_txs')
            if response.status_code == 200:
                self.current_transactions = response.json()['pending_txs']
                return self.current_transactions

    def save_chain(self):
        with open('blockchain.dat', 'w') as outfile:
            json.dump(self.chain, outfile)
    def load_chain(self):
        file_object = open('blockchain.dat', 'r')
        dict_object = json.load(file_object)
        self.chain = dict_object
    def save_pending_tx(self):
        with open('pending_txs.dat', 'w') as outfile:
            json.dump(self.current_transactions, outfile)
    def load_pending_tx(self):
        with open('pending_txs.dat', 'r') as file_object:
            self.current_transactions = json.load(file_object)
    def save_nodes(self):
        with open('nodes.dat', 'w') as outfile:
            json.dump(self.nodes, outfile)
    def load_nodes(self):
        file_object = open('nodes.dat', 'r')
        dict_object = json.load(file_object)
        self.nodes = dict_object
    def mine(self):
        # Мы запускаем алгоритм подтверждения работы, чтобы получить следующее подтверждение…
        last_block = self.last_block
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)
     
        # Мы должны получить вознаграждение за найденное подтверждение
        # Отправитель “0” означает, что узел заработал крипто-монету
        self.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=50,
        )
     
        # Создаем новый блок, путем внесения его в цепь
        previous_hash = self.hash(last_block)
        block = self.new_block(proof, previous_hash)
blockchain = Blockchain()
blockchain.new_block(previous_hash=1, proof=100, time_stamp=1337)
