import json
def make_blocks(n):
    blocks=[]
    for i in range(n):
        value =(i+1)*100
        blocks.append({"index": i, "data": [value]})
    return blocks

    

def get_block(blocks,index):
        if index < 0 or index >= len(blocks):
            print(f'你输入的指标不对')
        else:
            return blocks[index]

class TutorialStore:
    """
    A tiny wrapper class for Task 1.3.
    - Builds the list of blocks on initialization
    - Prints a block by index
    """
    def __init__(self, n: int = 10) -> None:
        """
        Parameters
        ----------
        n : int
            Number of blocks to generate (default 10).
        """
        self.blocks = make_blocks(n)

    def print_block(self, index: int) -> None:
        """
        Pretty-print a block by index.

        Parameters
        ----------
        index : int
            Zero-based index of the block to print.
        """
        blk = get_block(self.blocks, index)
        print(json.dumps(blk, ensure_ascii=False, indent=2))
    
if __name__ == "__main__":
    store = TutorialStore(n=10)
    # 打印第 4 个块（索引 3）
    store.print_block(3)
