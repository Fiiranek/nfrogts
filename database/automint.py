from configs import PROJ_DIR, TEMP_DIR, COLLECTION_ADDR, METADATA_DIR
from automint.wallet import Wallet
import os
from automint.account import Account
from automint.receivers import TxReceiver
from automint.receivers import MintingReceiver
from automint.wallet import Wallet
from automint.utxo import UTXO
from automint.utils import get_protocol_params, get_policy_id, get_key_hash, write_policy_script, get_policy_id, build_raw_transaction, calculate_tx_fee, submit_transaction, sign_tx


def get_utxos(wallet_address):
    payment_wallet = Wallet(PROJ_DIR, 'payment')
    payment_wallet.query_utxo()

    result = {}

    for txHash in payment_wallet.get_utxos():
        utxo = payment_wallet.get_utxo(identifier=txHash)
        result.update({
            'utxo': str(utxo),
            'amount': utxo.get_account().get_lovelace()
        })

    return result


def refund_utxo(utxo, refund_address):
    """
    utxo : utxo to refund
    refund_address : address to refund to

    note that all assets/funds within the utxo will be sent to the refund_address
    """
    payment_wallet = Wallet(PROJ_DIR, 'payment')
    payment_wallet.query_utxo()
    utxo = payment_wallet.get_utxo(utxo)

    tx_receiver = utxo.convert_to_receiver(refund_address)

    protocol_param_fp = get_protocol_params(TEMP_DIR)

    raw_matx_path = build_raw_transaction(TEMP_DIR,
                                          input_utxo,
                                          tx_receiver.get_blank_receiver())

    fee = calculate_tx_fee(raw_matx_path, protocol_param_fp, utxo, tx_receiver)

    tx_receiver.remove_lovelace(fee)

    raw_matx_path = build_raw_transaction(TEMP_DIR,
                                          input_utxo,
                                          tx_receiver,
                                          fee=fee)

    signed_matx_path = sign_tx(TEMP_DIR,
                               payment_wallet,
                               raw_matx_path)

    return submit_transaction(signed_matx_path)


# 0-4999
def mint_and_send(frog_id, utxo_id, buyer_address, collection_address):
    """
    frog_id : ID of frog (0 - 4999) as a string
    buyer_address : address to send to
    collection_address : adress where all funds sales will be collected
    """
    payment_wallet = Wallet(PROJ_DIR, 'payment')
    policy_wallet = Wallet(PROJ_DIR, 'policy')

    payment_wallet.query_utxo()

    utxo = payment_wallet.get_utxo(identifier=utxo_id)

    protocol_param_fp = get_protocol_params(TEMP_DIR)

    key_hash = get_key_hash(policy_wallet.get_vkey_path())
    policy_script_fp = write_policy_script(PROJ_DIR, key_hash, force=False)
    policy_id = get_policy_id(policy_script_fp)

    collection_receiver = utxo.convert_to_receiver(COLLECTION_ADDR)
    customer_receiver = TxReceiver(buyer_address)
    minting_receiver = MintingReceiver()

    # TODO: get name of asset
    token_id = f'{policy_id}.NFROG{frog_id}'
    customer_receiver.add_native_token(token_id, 1)
    minting_receiver.add_native_token(token_id, 1)

    receivers = [customer_receiver, collection_receiver]

    metadata_fp = os.path.join(METADATA_DIR, f'NFROG{frog_id}.json')

    assert os.path.exists(metadata_fp)

    raw_matx_path = build_raw_transaction(TEMP_DIR,
                                          utxo,
                                          list(map(lambda r: r.get_blank_receiver(), receivers)),
                                          policy_id,
                                          minting_receiver,
                                          metadata=metadata_fp)

    fee = calculate_tx_fee(raw_matx_path, protocol_param_fp, utxo, receivers)

    raw_matx_path = build_raw_transaction(TEMP_DIR,
                                          utxo,
                                          receivers,
                                          policy_id,
                                          minting_receiver,
                                          fee=fee,
                                          metadata=metadata_fp)

    signed_matx_path = sign_tx(TEMP_DIR,
                               [payment_wallet, policy_wallet],
                               raw_matx_path,
                               scipt_path=policy_script_fp)

    return submit_transaction(signed_matx_path)
