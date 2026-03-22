from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load deployed contract info
with open("contract_info.json", "r") as f:
    info = json.load(f)

abi = info['abi']
contract_address = info['address']

contract = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.accounts[0]

def add_certificate(cert_id, email, name, course, cert_hash):
    tx_hash = contract.functions.addCertificate(
        cert_id, email, name, course, cert_hash
    ).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)

def get_certificate(cert_id):
    try:
        return contract.functions.getCertificate(cert_id).call()
    except:
        return None