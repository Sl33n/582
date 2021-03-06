import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import insert_order
from insert_order import order_obj


from models import Base, Order

engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def process_order(order):
    orders = session.query(Order).filter(Order.filled == None).all()
    receiver_stored = order['receiver_pk']
    insert(order)
    for existing_order in orders:
        if matched(existing_order, order):
            new_order = session.query(Order).filter(Order.filled == None,Order.receiver_pk == receiver_stored).first()
            new_order.counterparty_id = existing_order.id
            existing_order.counterparty_id = new_order.id
            existing_order.filled = datetime.now()
            new_order.filled = datetime.now()
            session.commit()
    pass


def matched(existing_order, order):
    if existing_order.buy_currency == order['sell_currency'] \
            and existing_order.sell_currency == order['buy_currency'] \
            and order['sell_amount'] != 0 \
            and existing_order.buy_amount != 0 \
            and existing_order.sell_amount / existing_order.buy_amount >= order['buy_amount'] / order['sell_amount'] \
            and order['buy_amount'] == existing_order.sell_amount:

        return True
    else:
        return False


def insert(order):
    fields = ['sender_pk', 'receiver_pk', 'buy_currency', 'sell_currency', 'buy_amount', 'sell_amount']
    order_obj = Order(**{f: order[f] for f in fields})
    session.add(order_obj)
    session.commit()
    print("\norder inserted ", order)


if __name__ == '__main__':
    order = {
        'buy_currency': "Algorand",
        'sell_currency': "Ethereum",
        'buy_amount': 1245.00,
        'sell_amount': 2342.31,
        'sender_pk': '4EHA2QPRXC2ZJDIAGSKHPSAACC2UC4TGFBKL3TL4QXB2KJZGJAOYZEUC7E',
        'receiver_pk': '0xd1B77a920A0c5010469F40f14c5e4E03f4357226'
    }
    process_order(order)
    exit()
