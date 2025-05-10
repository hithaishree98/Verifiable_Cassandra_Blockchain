import hashlib
import merkletools

class QueryClient:

    def __init__(self, server, blockchain, merkle_tree):
        self.server = server
        self.blockchain = blockchain
        self.merkle_tree: merkletools.MerkleTools = merkle_tree

    def query_by_key(self, key: str) -> str | None:
        return self.server.get_data(key)

    def retrieve_verification_path_by_tree(self, key_index: int) -> list[dict]:
        return self.merkle_tree.get_proof(key_index)

    def retrieve_root_from_blockchain(self) -> str | None:
        return self.blockchain.get_merkle_root()

    def query_verification(self, key: str, retrieved_value: str | None,
                           proofs: list[dict], root_from_contract: str | None) -> bool:
        if retrieved_value is None or root_from_contract is None:
            return False

        leaf_bytes = f"{key}:{retrieved_value}".encode("utf-8")
        leaf_hex = hashlib.sha256(leaf_bytes).hexdigest()

        return self.merkle_tree.validate_proof(proofs, leaf_hex, root_from_contract)
