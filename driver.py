from db_provider import Server
from data_owner import DataOwner
from adv_client import MaliciousClient
from query_client import QueryClient
from blockchain import Blockchain

if __name__ == '__main__':

    blockchain = Blockchain('http://127.0.0.1:8545')
    blockchain.compile_contract()
    blockchain.deploy_contract()

    server = Server()
    data = {"k1": "a", "k2": "b", "k3": "c"}

    owner = DataOwner(data, server, blockchain)
    owner.build_merkle_tree()
    owner.insert_data_to_server()
    owner.upload_merkle_root_to_blockchain()
    merkle_tree = owner.get_merkle_tree()


    qc = QueryClient(server, blockchain, merkle_tree)
    key = "k1"

    value = qc.query_by_key(key)
    idx = owner.index_of_key(key)
    proof = qc.retrieve_verification_path_by_tree(idx)
    onchain_root = qc.retrieve_root_from_blockchain()
    print("Merkle root from blockchain:", onchain_root)

    ok = qc.query_verification(key, value, proof, onchain_root)
    print(f"[Verify before tamper] key={key}, value={value}, verified={ok}")

    attacker = MaliciousClient(server)
    attacker.modify_data_by_key("k1", "zzz")  

    tampered_value = qc.query_by_key(key)
    tampered_ok = qc.query_verification(key, tampered_value, proof, onchain_root)
    print(f"[Verify after tamper] key={key}, value={tampered_value}, verified={tampered_ok}")
