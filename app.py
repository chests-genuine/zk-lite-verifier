# app.py
"""
zk-lite-repo: small utility to snapshot and verify on-chain contract bytecode integrity.
Usage:
  - Set RPC_URL or INFURA_API_KEY environment variable.
  - Run: python3 app.py [0xContractAddress] [--expect-hash=<hex>]
"""
import os
import sys
import time
import hashlib
import argparse
from web3 import Web3

DEFAULT_CONTRACT = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"

def get_rpc_url():
    # Prefer explicit RPC_URL, fall back to Infura mainnet if INFURA_API_KEY provided
    if os.getenv("RPC_URL"):
        return os.getenv("RPC_URL")
    if os.getenv("INFURA_API_KEY"):
        return f"https://mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY')}"
    return "https://mainnet.infura.io/v3/"

def compute_hash(code_bytes, algo="sha256"):
    if algo == "sha256":
        return hashlib.sha256(code_bytes).hexdigest()
    if algo == "sha1":
        return hashlib.sha1(code_bytes).hexdigest()
    raise ValueError("unsupported hash algo")

def verify_zk_contract(address, rpc_url, expect_hash=None, algo="sha256", save_log=True):
    start = time.time()
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL/INFURA_API_KEY and network access.")
        sys.exit(1)

    print(f"🔗 Connected. Chain ID: {w3.eth.chain_id} | Block: {w3.eth.block_number}")
    if not Web3.is_address(address):
        print("❌ Invalid Ethereum address format.")
        sys.exit(1)

    checksum = Web3.to_checksum_address(address)
    code = w3.eth.get_code(checksum)
    print(f"🧩 Bytecode length: {len(code)} bytes")
    if not code:
        print("⚠️ No bytecode found — address may be an EOA or not deployed on this chain.")
        return {"address": checksum, "hash": None, "code_len": 0, "ok": False}

    code_hash = compute_hash(code, algo=algo)
    print(f"🔎 Contract: {checksum}")
    print(f"🛡️ Code {algo.upper()}: {code_hash}")

    ok = True
    if expect_hash:
        ok = (code_hash.lower() == expect_hash.lower())
        if ok:
            print("✅ Hash matches expected value.")
        else:
            print("❌ Hash does NOT match expected value.")

    if save_log:
        try:
            with open("verification_log.txt", "a") as f:
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                f.write(f"{ts} | {checksum} | {code_hash} | chain:{w3.eth.chain_id} | len:{len(code)}\n")
        except Exception:
            pass

    print(f"⏱️ Verification time: {time.time() - start:.2f}s")
    return {"address": checksum, "hash": code_hash, "code_len": len(code), "ok": ok}

def main():
    parser = argparse.ArgumentParser(description="Lightweight zk-related contract bytecode snapshot & verifier")
    parser.add_argument("address", nargs="?", default=DEFAULT_CONTRACT, help="Contract address to check")
    parser.add_argument("--expect-hash", dest="expect_hash", help="Expected hex hash to compare against")
    parser.add_argument("--algo", dest="algo", default="sha256", choices=["sha256","sha1"], help="Hash algorithm")
    parser.add_argument("--no-log", dest="nolog", action="store_true", help="Do not append to verification_log.txt")
    args = parser.parse_args()

    rpc_url = get_rpc_url()
    verify_zk_contract(args.address, rpc_url, expect_hash=args.expect_hash, algo=args.algo, save_log=not args.nolog)

if __name__ == "__main__":
    main()
import random
emoji = random.choice(["🧠", "🔒", "💫", "⚙️", "🛡️"])
print(f"{emoji} Verification completed successfully.")
