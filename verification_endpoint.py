from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk


app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

def verifyEth(request):
    valid_eth = False

    eth_pk = request['payload']['pk']
    payload = request['payload']

    payload = json.dumps(payload)
    eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
    if eth_account.Account.recover_message(eth_encoded_msg, signature=request['sig']) == eth_pk:
        print("Eth sig verifies!")
        valid_eth = True

    return valid_eth

def verifyAlg(request):
    valid_alg = False
    payload = request['payload']
    algo_sig_str = request['sig']
    algo_pk = payload['pk']
    payload = json.dumps(payload)

    if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
        print("Algo sig verifies!")
        valid_alg = True
    return valid_alg


@app.route('/verify', methods=['GET','POST'])
def verify():
    result = False #Should only be true if signature validates
    request = request.get_json(silent=True)

    if request['payload']['platform'] == 'Ethereum' and verifyEth(request):
        result = True
    else:
        if request['payload']['platform'] == 'Algorand' and verifyAlg(request):
            result = True

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5002)
