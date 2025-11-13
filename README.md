# README.md
# zk-lite-verifier

Overview
This repository contains a tiny Python utility (app.py) to snapshot and verify on-chain smart contract bytecode. It's intended as a lightweight tool for auditing or tracking contracts used in ZK ecosystems (Aztec, Zama, other zk-rollups) and general Web3 soundness checks.

Files included
- app.py — main Python script (web3.py required)
- verification_log.txt — created after the first run (appends timestamp, address, hash, chain id, length)

Requirements
- Python 3.10+ recommended
- Install dependency: pip install web3

Configuration
- Provide an RPC endpoint via environment variable RPC_URL, for example: export RPC_URL="https://your-rpc.node"
- Or set INFURA_API_KEY to let the script build an Infura mainnet URL: export INFURA_API_KEY="your_infura_project_id"
- If neither is set, the script uses a default Infura mainnet base (may fail without a valid key).

Usage
- Run with the bundled example contract: python3 app.py
- Run a specific address: python3 app.py 0xYourContractAddress
- Compare against an expected hash: python3 app.py 0xYourContractAddress --expect-hash=<hex>
- Choose SHA-1 instead of SHA-256: python3 app.py 0xAddress --algo=sha1
- Avoid creating a log file: python3 app.py 0xAddress --no-log

What the script does (expected output)
- Connects to RPC and prints chain id and current block.
- Validates the provided address format.
- Fetches on-chain bytecode and reports its length.
- Computes and prints the chosen hash (SHA-256 by default).
- Optionally compares computed hash with an expected value and reports match/mismatch.
- Appends a line to verification_log.txt with timestamp | address | hash | chain | len (unless --no-log used).

Example output (human-readable)
🔗 Connected. Chain ID: 1 | Block: 19412345
🧩 Bytecode length: 1024 bytes
🔎 Contract: 0x5A98FcBE...
🛡️ Code SHA256: e2c7a9...
✅ Hash matches expected value.        (or ❌ Hash does NOT match expected value.)
⏱️ Verification time: 0.42s

Notes & next steps
- To inspect contracts on Aztec/Zama or other chains, point RPC_URL to a node for that network.
- For CI use, store expected canonical hashes and fail the pipeline when mismatches occur.
- For production, keep RPC keys secret (use environment variables or a secret manager) and consider stronger logging/alerting.
- This tool snapshots bytecode only; it does not validate ABI, runtime behavior, or formal ZK proofs. For deeper soundness checks integrate with project-specific proof verification workflows.
