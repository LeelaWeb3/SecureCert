from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import json

# Install Solidity compiler
install_solc('0.8.0')
set_solc_version('0.8.0')

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
print("Connected:", w3.is_connected())

# Load contract
with open("contracts/Certificate.sol", "r") as file:
    contract_source_code = file.read()

compiled_sol = compile_source(contract_source_code)
contract_id, contract_interface = compiled_sol.popitem()

abi = contract_interface['abi']
bytecode = contract_interface['bin']

# Deploy
account = w3.eth.accounts[0]
Certificate = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Certificate.constructor().transact({'from': account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print("Contract Address:", contract_address)

# Save ABI + address for app.py
with open("contract_info.json", "w") as f:
    json.dump({"abi": abi, "address": contract_address}, f)