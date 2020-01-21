import base64

exec(open("./Blockchain.py").read())
#1337
def load_all():
    try:
        blockchain.load_chain()
        blockchain.load_pending_tx()
    except:
        print("Could not load chain from file")
    finally:
        pass
def save_all():
    try:
        blockchain.save_chain()
        blockchain.save_pending_tx()
    except:
        print("Could not save chain to file")
    finally:
        pass
def save_nodes():
    try:
        blockchain.save_nodes()
    except:
        print("Could not save nodes to file")
    finally:
        pass
def load_nodes():
    try:
        blockchain.load_nodes()
    except:
        print("Could not load nodes from file")
    finally:
        pass

load_all()
load_nodes()
try:
    blockchain.resolve_conflicts()
except:
    print("Could not syncronize")

print(blockchain.validate_chain(blockchain.chain))

save_nodes()
save_all()

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    load_all()
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/balances', methods=['GET'])
def balances():
    response = blockchain.balances()
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount','signature']
    if not all(k in values for k in required):
        return 'Missing values', 400

    sig = values['signature']
    print(sig)
    print(type(sig))
    sig = sig

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'], sig)

    if index:
        response = {'message': f'Transaction will be added to Block {index}'}
    else:
        response = {'message': f'Transaction failed because of: {err}'}
    return jsonify(response), 201

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
 
    for node in nodes:
        blockchain.register_node(node)
 
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    save_nodes()
    return jsonify(response), 201
 
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    print(blockchain.nodes)
    replaced = blockchain.resolve_conflicts()

    if replaced:
        save_nodes()
        save_all()
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
            }

    return jsonify(response), 200

@app.route('/peers/list', methods=['GET'])
def peer_list():
    peers = blockchain.nodes
    return jsonify(peers), 200
@app.route('/peers/discover', methods=['GET'])
def peers_discover():
    result = blockchain.discover_peers()
    if result:
        response = {
            'message': 'You discovered some new peers'
        }
    else:
        response = {
            'message': 'You could not discover some new peers'
        }
    return jsonify(response), 200
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
