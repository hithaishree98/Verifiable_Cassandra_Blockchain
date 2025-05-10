import merkletools

class DataOwner:
    """
    Builds a Merkle tree over (key:value) strings, inserts data into the server,
    and uploads the Merkle root to the blockchain.
    """
    def __init__(self, key_value_data: dict, server, blockchain):
        self.data = key_value_data
        self.server = server
        self.blockchain = blockchain
        self.merkle_tree = merkletools.MerkleTools(hash_type='sha256')
        self._ordered_items = list(self.data.items())

    def insert_data_to_server(self):
        for key, value in self._ordered_items:
            self.server.add_data(key, value)
        print("Data inserted to server.")

    def build_merkle_tree(self):
        for key, value in self._ordered_items:
            self.merkle_tree.add_leaf(f"{key}:{value}", do_hash=True)
        self.merkle_tree.make_tree()
        print("Merkle tree built.")

    def upload_merkle_root_to_blockchain(self):
        root = self.merkle_tree.get_merkle_root()
        self.blockchain.set_merkle_root(root)
        print("Merkle root uploaded to blockchain:", root)

    def get_merkle_tree(self):
        return self.merkle_tree

    def index_of_key(self, key: str) -> int:
        for i, (k, _) in enumerate(self._ordered_items):
            if k == key:
                return i
        raise KeyError(f"Key {key} not found in data owner ordering.")
