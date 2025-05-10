from web3 import Web3
from solcx import compile_source

class Blockchain:
    def __init__(self, host):
        self.host = host
        self.abi = None
        self.bytecode = None
        self.contract_instance = None
        self.service_provider = None

    def set_merkle_root(self, merkle_root: str):
        try:
            tx_hash = self.contract_instance.functions.setMerkleRoot(merkle_root).transact()
            receipt = self.service_provider.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        except Exception as e:
            print(f"Failed to set Merkle root: {e}")
            return None

    def get_merkle_root(self) -> str | None:
        try:
            return self.contract_instance.functions.getMerkleRoot().call()
        except Exception as e:
            print(f"Failed to retrieve Merkle root: {e}")
            return None

    def compile_contract(self):
        source = '''
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;
        contract Verify {
            string private merkleRoot;

            function setMerkleRoot(string memory _merkleRoot) public {
                merkleRoot = _merkleRoot;
            }

            function getMerkleRoot() public view returns (string memory) {
                return merkleRoot;
            }
        }
        '''
        compiled = compile_source(source, output_values=['abi', 'bin'])
        _, contract_interface = compiled.popitem()
        self.bytecode = contract_interface['bin']
        self.abi = contract_interface['abi']

    def deploy_contract(self):
        w3 = Web3(Web3.HTTPProvider(self.host))
        self.service_provider = w3
        w3.eth.default_account = w3.eth.accounts[0]

        Verify = w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = Verify.constructor().transact()
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_instance = w3.eth.contract(
            address=receipt.contractAddress,
            abi=self.abi
        )
