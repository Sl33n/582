from flask import Flask, request, g
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
import json
import eth_account
import algosdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import load_only
from datetime import datetime
import sys

from models import Base, Order, Log

engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


@app.before_request
def create_session():
    g.session = scoped_session(DBSession)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    sys.stdout.flush()
    g.session.commit()
    g.session.remove()


""" Suggested helper methods """

def verifyEth(content):
    valid_eth = False
    eth_pk = content['payload']['sender_pk']
    payload = content['payload']
    payload = json.dumps(payload)
    eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
    if eth_account.Account.recover_message(eth_encoded_msg, signature=content['sig']) == eth_pk:
        print("Eth sig verifies!")
        valid_eth = True
    return valid_eth


def verifyAlg(content):
    payload = content['payload']
    algo_sig_str = content['sig']
    algo_pk = payload['sender_pk']
    payload = json.dumps(payload)
    if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
        print("Algo sig verifies!")
        return True
    return False


def check_sig(payload, sig):
    pass


def fill_order(order, txes=[]):
    pass

def insert_order_to_db(order):
    order_obj = Order(sender_pk=order['payload']['sender_pk'], receiver_pk=order['payload']['receiver_pk'],
                      buy_currency=order['payload']['buy_currency'], sell_currency=order['payload']['sell_currency'],
                      buy_amount=order['payload']['buy_amount'], sell_amount=order['payload']['sell_amount'])
    session.add(order_obj)
    session.commit()

def log_message(d):
    payload = d['payload']
    messagePayload = json.dumps(payload)
    log_obj = Log(message=messagePayload)
    session.add(log_obj)
    session.commit()
    pass


def is_valid_order(existing_order):
    sell_currency = existing_order.sell_currency
    if sell_currency != "Ethereum" and sell_currency != "Algorand":
        return False
    return True

""" End of helper methods """


@app.route('/trade', methods=['POST'])
def trade():
    if request.method == "POST":
        content = request.get_json(silent=True)
        print(f"content = {json.dumps(content)}")
        columns = ["sender_pk", "receiver_pk", "buy_currency", "sell_currency", "buy_amount", "sell_amount", "platform"]
        fields = ["sig", "payload"]
        error = False
        for field in fields:
            if not field in content.keys():
                print(f"{field} not received by Trade")
                print(json.dumps(content))
                log_message(content)
                return jsonify(False)

        error = False
        for column in columns:
            if not column in content['payload'].keys():
                print(f"{column} not received by Trade")
                error = True
        if error:
            print(json.dumps(content))
            log_message(content)
            return jsonify(False)

        # Your code here
        platform = content['payload']['sell_currency']
        if platform == 'Ethereum':
            eth_pk = content['payload']['sender_pk']
            payload = content['payload']
            payload = json.dumps(payload)
            eth_encoded_msg = eth_account.messages.encode_defunct(text=payload)
            if eth_account.Account.recover_message(eth_encoded_msg, signature=content['sig']) == eth_pk:
                print("Eth sig verifies!")
                add_order(content)
                return jsonify(True)
        elif platform == 'Algorand':
            payload = content['payload']
            algo_sig_str = content['sig']
            algo_pk = payload['sender_pk']
            payload = json.dumps(payload)
            if algosdk.util.verify_bytes(payload.encode('utf-8'), algo_sig_str, algo_pk):
                print("Algo sig verifies!")
                add_order(content)
                return jsonify(True)
        else:
            log_message(content)
        return jsonify(False)


        # TODO: Check the signature (V)

        # TODO: Add the order to the database (V)

        # TODO: Fill the order

        # TODO: Be sure to return jsonify(True) or jsonify(False) depending on if the method was successful


@app.route('/order_book')
def order_book():
    # Your code here
    # Note that you can access the database session using g.session
    #
    orders = session.query(Order).filter(Order.filled == None).all()
    data = []
    for existing_order in orders:
        if order_correct(existing_order):
            #print("valid")
            sender_pk = existing_order.sender_pk
            receiver_pk = existing_order.receiver_pk
            buy_currency = existing_order.buy_currency
            sell_currency = existing_order.sell_currency
            buy_amount = existing_order.buy_amount
            sell_amount = existing_order.sell_amount
            signature = existing_order.signature

            orderJson = {
                "sender_pk": sender_pk,
                "receiver_pk": receiver_pk,
                "buy_currency": buy_currency,
                "sell_currency": sell_currency,
                "buy_amount": buy_amount,
                "sell_amount": sell_amount,
                "signature": signature,
            }
            data.append(orderJson)
    result = {"data": data}
    # return json.dumps(result)
    # return app.response_class(json.dumps(result), content_type='application/json')
    return jsonify(result)


def add_order(order):
    order_obj = Order(sender_pk=order['payload']['sender_pk'], receiver_pk=order['payload']['receiver_pk'],
                      buy_currency=order['payload']['buy_currency'], sell_currency=order['payload']['sell_currency'],
                      buy_amount=order['payload']['buy_amount'], sell_amount=order['payload']['sell_amount'])
    session.add(order_obj)
    session.commit()
    # print("order inserted ", order)


def order_correct(existing_order):
    sell_currency = existing_order.sell_currency

    if sell_currency != "Ethereum" and sell_currency != "Algorand":
        return False

    return True



if __name__ == '__main__':
    app.run(port='5002')
