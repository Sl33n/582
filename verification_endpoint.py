from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk


app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

def verifyAlgorand(request):
    valid_alg = False
    payload = request['payload']
    algo_sig_str = request['sig']
    algo_pk = payload['pk']
    payload = json.dumps(payload)

    if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
        valid_alg = True
    return valid_alg


def verifyEtherium(request):
    valid_eth = False

    eth_pk = request['payload']['pk']
    payload = request['payload']

    payload = json.dumps(payload)
    eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
    if eth_account.Account.recover_message(eth_encoded_msg, signature=content['sig']) == eth_pk:
        valid_eth = True

    return valid_eth


@app.route('/verify', methods=['GET','POST'])
def verify():
    result = False #Should only be true if signature validates
    content = request.get_json(silent=True)

    if content['payload']['platform'] == 'Ethereum' and verifyEtherium(request):
        result = True
    else:
        if content['payload']['platform'] == 'Algorand' and verifyAlgorand(request):
            result = True

    # Check if signature is valid
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5002)
