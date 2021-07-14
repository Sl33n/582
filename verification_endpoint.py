from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk


app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

def verifyEth(content):
    valid_eth = False

    eth_pk = content['payload']['pk']
    payload = content['payload']

    payload = json.dumps(payload)
    eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
    if eth_account.Account.recover_message(eth_encoded_msg, signature=content['sig']) == eth_pk:
        print("Eth sig verifies!")
        valid_eth = True

    return valid_eth

def verifyAlg(content):
    valid_alg = False
    payload = content['payload']
    algo_sig_str = content['sig']
    algo_pk = payload['pk']
    payload = json.dumps(payload)

    if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
        print("Algo sig verifies!")
        valid_alg = True
    return valid_alg


@app.route('/verify', methods=['GET','POST'])
def verify():
    result = False #Should only be true if signature validates
    content = request.get_json(silent=True)

    if content['payload']['platform'] == 'Ethereum' and verifyEth(content):
        result = True
    else:
        if content['payload']['platform'] == 'Algorand' and verifyAlg(content):
            result = True

    return jsonify(result)


if __name__ == '__main__':
#    content = {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c',
# 'payload':
#   {'message': 'Ethereum test message',
#    'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF',
#    'platform': 'Ethereum'}}

#    print(verifyAlg(content))
    app.run(port=5002)
