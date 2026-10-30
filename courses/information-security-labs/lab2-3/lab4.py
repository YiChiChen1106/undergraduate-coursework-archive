import datetime
import hashlib
import json

# ---------------------------------------------------------------------------
# Lab 1 & 2: Blockchain Implementation with Proof of Work (PoW)
# Student Name: ChenYiChi
# Student Number: Jianghaoze
# ---------------------------------------------------------------------------

class Blockchain:
    """
    A class representing the Blockchain architecture.
    It manages the chain of blocks and the Proof of Work consensus.
    """

    def __init__(self):
        """
        Initializes the Blockchain.
        Creates the Genesis Block (the first block in the chain).
        """
        self.chain = []
        # Create the Genesis block with a fixed proof of 1 and previous_hash of '0'
        # [cite: 116, 120, 136]
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """
        Creates a new block and adds it to the blockchain.
        
        Args:
            proof (int): The proof given by the Proof of Work algorithm.
            previous_hash (str): Hash of the previous block.
        
        Returns:
            dict: The newly created block.
        """
        block = {
            'index': len(self.chain) + 1,           # [cite: 116]
            'timestamp': str(datetime.datetime.now()), # [cite: 117]
            'proof': proof,                         # [cite: 119]
            'previous_hash': previous_hash,         # [cite: 120]
            'data': "Block Data" # Placeholder data as per Lab 1 structure
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """
        Returns the last block in the chain.
        [cite: 150]
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
            new_proof = 1
            check_proof = False

            while check_proof is False:
                # === 创新点开始 ===
                # 原版: str(new_proof**2 - previous_proof**2).encode()
                
                # 新版: 使用异或 (^) 和乘法混合运算
                # 逻辑: 将两个 proof 进行异或，然后乘以 7 (增加非线性)，最后转为字符串
                operation = (new_proof ^ previous_proof) * 7
                
                hash_operation = hashlib.sha256(str(operation).encode()).hexdigest()
                # === 创新点结束 ===

                if hash_operation[:4] == '0000':
                    check_proof = True
                else:
                    new_proof += 1
                    
            return new_proof

    def hash(self, block):
        """
        Calculates the SHA256 hash of a block.
        Used for validation.
        """
        # Use JSON dumps to encode the block [cite: 40]
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
            previous_block = chain[0]
            block_index = 1

            while block_index < len(chain):
                block = chain[block_index]
                
                # 1. 检查 previous_hash (这部分不用动)
                if block['previous_hash'] != self.hash(previous_block):
                    return False
                
                # 2. 检查 Proof of Work (这里需要修复！)
                previous_proof = previous_block['proof']
                proof = block['proof']
                
                # === 错误代码 (旧算法) ===
                # hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
                
                # === 修正后的代码 (必须与 proof_of_work 保持一致) ===
                operation = (proof ^ previous_proof) * 7  # 使用你现在用的位运算
                hash_operation = hashlib.sha256(str(operation).encode()).hexdigest()
                
                if hash_operation[:4] != '0000':
                    return False
                
                previous_block = block
                block_index += 1
            
            return True

# ---------------------------------------------------------------------------
# Main Execution / Demonstration
# ---------------------------------------------------------------------------

# 1. Instantiate the Blockchain
blockchain = Blockchain()
print("Blockchain initiated.")
print(f"Genesis Block: {blockchain.chain[0]}")
print("-" * 30)

# 2. Mine New Blocks (Task 5: Mine two blocks) [cite: 46]
# --- Mining Block 1 ---
print("Mining block 1...")
previous_block = blockchain.get_previous_block()
previous_proof = previous_block['proof']
previous_hash = blockchain.hash(previous_block)

# Run Proof of Work to find the valid proof
proof = blockchain.proof_of_work(previous_proof)

# Create the block
block1 = blockchain.create_block(proof, previous_hash)
print(f"Block 1 mined! Details: {block1}")
print("-" * 30)

# --- Mining Block 2 ---
print("Mining block 2...")
previous_block = blockchain.get_previous_block()
previous_proof = previous_block['proof']
previous_hash = blockchain.hash(previous_block)

# Run Proof of Work
proof = blockchain.proof_of_work(previous_proof)

# Create the block
block2 = blockchain.create_block(proof, previous_hash)
print(f"Block 2 mined! Details: {block2}")
print("-" * 30)

# 3. Validate Chain (Task 6)
is_valid = blockchain.is_chain_valid(blockchain.chain)
print(f"Is Blockchain Valid? {is_valid}")
print("-" * 30)

# Print final chain
print("Final Chain Structure:")
print(json.dumps(blockchain.chain, indent=4, default=str))