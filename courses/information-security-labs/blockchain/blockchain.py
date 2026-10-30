#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal Blockchain for Lab
--------------------------
Implements a simple blockchain with a custom Proof of Work (PoW).
Satisfies Task 3 requirements:
 - 3.1: Genesis block creation on instantiation
 - 3.2: Add new blocks with input data
 - 3.3: Retrieve previous block (tip)

Extras:
 - Deterministic block hashing
 - Chain validation
 - Demonstration section showing genesis, full chain, per-block hash audit,
   and print-by-index (Task 1.2 style).
"""
import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List


# ------------------------------- Utilities ---------------------------------
def hash_block(block: Dict[str, Any]) -> str:
    """
    Compute deterministic SHA-256 over a JSON-serialized block.
    """
    encoded = json.dumps(block, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def ensure_list(data: Any) -> List[Any]:
    """
    Ensure that the payload data is always a list.
    """
    return data if isinstance(data, list) else [data]


def utcnow_iso() -> str:
    """
    Return the current UTC timestamp as an ISO 8601 string with 'Z' suffix.
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ------------------------------ Blockchain ----------------------------------
class Blockchain:
    """
    Minimal blockchain with a custom PoW based on a divisibility condition.
    """

    def __init__(self) -> None:
        """Initialize chain and create genesis block."""
        self.chain: List[Dict[str, Any]] = []
        self._create_genesis_block()

    # -- Task 3.1: Genesis block --
    def _create_genesis_block(self) -> Dict[str, Any]:
        """Create and append the genesis block."""
        block = {
            "index": 0,
            "timestamp": utcnow_iso(),
            "data": ["Hello World!"],
            "proof": 0,
            "previous_hash": "0",
        }
        self.chain.append(block)
        return block

    def _build_block(self, *, index: int, data: Any, proof: int, previous_hash: str) -> Dict[str, Any]:
        """Assemble a block with the standard fields."""
        return {
            "index": index,
            "timestamp": utcnow_iso(),
            "data": ensure_list(data),
            "proof": int(proof),
            "previous_hash": previous_hash,
        }

    # -- Task 3.3: Previous block --
    def get_previous_block(self) -> Dict[str, Any]:
        """Return the tip (latest) block of the chain."""
        if not self.chain:
            raise IndexError("Blockchain is empty.")
        return self.chain[-1]

    # -- Custom PoW --
    def _pow_target(self) -> int:
        """Return divisibility parameter M. Larger M => harder mining."""
        return 50_000

    def _pow_digest(self, prev_hash: str, nonce: int) -> str:
        """Compute PoW digest as sha256(f"{prev_hash}|{nonce}")."""
        attempt = f"{prev_hash}|{nonce}".encode("utf-8")
        return hashlib.sha256(attempt).hexdigest()

    def verify_proof(self, prev_hash: str, nonce: int) -> bool:
        """Check if int(hash, 16) % M == 0."""
        digest_hex = self._pow_digest(prev_hash, nonce)
        digest_int = int(digest_hex, 16)
        return (digest_int % self._pow_target()) == 0

    def proof_of_work(self, prev_hash: str) -> int:
        """Find a nonce satisfying the PoW condition."""
        nonce = 0
        while True:
            if self.verify_proof(prev_hash, nonce):
                return nonce
            nonce += 1

    # -- Task 3.2: Add new block --
    def add_block(self, data: Any, proof: int | None = None) -> Dict[str, Any]:
        """Package data into a new block and append it to the chain."""
        prev_block = self.get_previous_block()
        prev_hash = hash_block(prev_block)

        if proof is None:
            proof = self.proof_of_work(prev_hash)

        new_block = self._build_block(
            index=len(self.chain),
            data=data,
            proof=proof,
            previous_hash=prev_hash,
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Validate the entire chain (linkage + PoW)."""
        if not self.chain:
            return False
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr.get("previous_hash") != hash_block(prev):
                return False
            prev_hash = hash_block(prev)
            if not self.verify_proof(prev_hash, curr.get("proof", -1)):
                return False
        return True


# ----------------------------- Demonstration --------------------------------
if __name__ == "__main__":
    from pprint import pprint

    bc = Blockchain()

    print("Mining block 1 (custom PoW)...")
    bc.add_block("Tx A")

    print("Mining block 2 (custom PoW)...")
    bc.add_block(["Tx B"])

    print("\n=== Genesis block (index 0) ===")
    pprint(bc.chain[0])

    print("\n=== Tip (previous block) ===")
    pprint(bc.get_previous_block())

    print("\n=== Full chain (pretty) ===")
    print(json.dumps(bc.chain, ensure_ascii=False, indent=2))

    print("\n=== Audit: each block's hash and linkage ===")
    for i, blk in enumerate(bc.chain):
        h = hash_block(blk)
        prev_h = hash_block(bc.chain[i - 1]) if i > 0 else "N/A"
        print(f"index={i}  hash(block)={h}")
        if i > 0:
            ok = (blk["previous_hash"] == prev_h)
            print(f"         previous_hash == hash(block[{i-1}]) ? {ok}")

    print("\nChain valid? ->", bc.is_chain_valid())

    print("\n=== Print block by index 1 ===")
    pprint(bc.chain[1])
