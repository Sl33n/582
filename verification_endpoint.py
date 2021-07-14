from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk


app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    result = False #Should only be true if signature validates
    request = request.get_json(silent=True)

    if request['payload']['platform'] == 'Ethereum':
        eth_pk = request['payload']['pk']
        payload = request['payload']

        payload = json.dumps(payload)
        eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
        if eth_account.Account.recover_message(eth_encoded_msg, signature=content['sig']) == eth_pk:
            result = True
        else:
            result = False

        if content['payload']['platform'] == 'Algorand' and verifyAlgorand(request):

            payload = request['payload']
            algo_sig_str = request['sig']
            algo_pk = payload['pk']
            payload = json.dumps(payload)

            if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):           
                result = True
            else: 
                result = False
        
    # Check if signature is valid
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5002)
