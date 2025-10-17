# Verifiable Key-Value Store using Cassandra, Merkle Trees, and Blockchain

## 1. Overview (short)

This project demonstrates a **verifiable key-value store**:  
Data is stored in a fast, mutable database (**Cassandra**).  
The **Data Owner** computes a **Merkle root** over the `(key:value)` pairs and publishes that root on a **blockchain smart contract** (Ganache/Ethereum).  

A client that reads a value from Cassandra also obtains a small **Merkle proof** and checks (locally) whether that value hashes to the same on-chain root — thus detecting any **tampering in the database** without having to trust the DB.

---

## 2. Why These Technologies?

### 🗃️ Cassandra — Distributed NoSQL Database
**What it is:**  
A horizontally scalable key-value / wide-column store optimized for high throughput and availability.

**Why used:**  
Provides fast, resilient storage for large datasets that are not practical to put on chain.  
Acts as the **mutable primary data store** in the system.

**Role in project:**  
Stores the raw `key → value` pairs and is treated as **untrusted storage** for verifying integrity through the Merkle root.

---

### 🌳 Merkle Tree — Cryptographic Hash Tree
**What it is:**  
A binary tree of cryptographic hashes where each leaf is a hash of a data item and internal nodes are hashes of their child hashes.  
The root succinctly commits to all leaves.

**Why used:**  
Allows efficient verification of a single element (logarithmic proof size) instead of rehashing or verifying the entire dataset.

**Role in project:**  
The **Data Owner** builds a Merkle tree over `f"{key}:{value}"`.  
The **Merkle Root** acts as a compact commitment to the dataset.  
Clients use **Merkle proofs** to verify individual values against that root.

---

### ⛓️ Blockchain (Ganache + Solidity + web3.py)
**What it is (in this setup):**  
- **Ganache** → Local Ethereum simulator for testing  
- **Solidity** → Smart contract language used to define blockchain logic  
- **web3.py** → Python library for interacting with Ethereum nodes

**Why used:**  
The blockchain provides an **immutable public anchor**.  
Writing the Merkle root on chain makes the commitment **tamper-evident** and **publicly verifiable**.

**Role in project:**  
Stores the Merkle root (as a string) inside a deployed **`Verify` smart contract**.  
Clients can read this on-chain root to verify whether their data from Cassandra remains authentic.

---

### ⚙️ Key Points

- Data is stored **off-chain** (in Cassandra).  
- Only the **Merkle root** is stored **on-chain**.  
- **Proofs** are computed off-chain and passed to the client.  
- Verification requires the **same deterministic leaf format and order** used during Merkle tree construction.

---

## 3. File Descriptions

| File | Description |
|------|--------------|
| `driver.py` | **Orchestrator (main):** Initializes components, builds Merkle tree, uploads root, runs verification, and simulates tampering. |
| `db_provider.py` | **Cassandra Wrapper (Server):** Handles keyspace and table creation, data insertion, and retrieval. |
| `data_owner.py` | **Data Owner:** Builds the Merkle tree from key-value data and uploads the Merkle root to the blockchain. |
| `blockchain.py` | **Blockchain Module:** Compiles and deploys the Solidity smart contract, and provides `set`/`get` functions for the Merkle root. |
| `query_client.py` | **Query Client:** Fetches values from Cassandra, retrieves Merkle proofs, and verifies data integrity using the blockchain root. |
| `adv_client.py` | **Malicious Client:** Simulates data tampering by modifying entries directly in the database. |

---

## 4. Setup Instructions

Follow these steps to run the project.  
Save them in a separate `readme.txt` or use directly in this README.

```bash
# 1. Install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip
python3 -m pip install -U pip
pip3 install cassandra-driver merkletools py-solc-x web3==5.31.4

# 2. Install Solidity compiler (optional if not auto-installed)
python3 - <<'PY'
from solcx import install_solc, set_solc_version
install_solc('0.8.26')
set_solc_version('0.8.26')
print("solc 0.8.26 installed")
PY

# 3. Start Ganache (Ethereum local blockchain)
ganache

# 4. Start Cassandra database
sudo service cassandra stop || true
sudo service cassandra start

# 5. Run the main driver
python3 driver.py
