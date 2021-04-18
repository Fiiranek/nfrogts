def get_utxos(wallet_address):
    return [{'amount': 11,
             'utxo': 'jjjjjjjjjjjj'},
            {'amount': 32195065,
             'utxo': '1bb719e0aedabab1d74b0b549c770e99e557b9f5d7e6534030b727fc7691ace8'}]


def refund_utxo(utxo, refund_address):
    """
    utxo : utxo to refund
    refund_address : address to refund to

    note that all assets/funds within the utxo will be sent to the refund_address
    """
    return True


# 0-4999
def mint_and_send(frog_id, buyer_address, collection_address):
    """
    frog_id : ID of frog (0 - 4999) as a string
    buyer_address : address to send to
    collection_address : adress where all funds sales will be collected
    """
    return True
