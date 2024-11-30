import heapq
from collections import Counter
import sys


class node:
    def __init__(self, freq, symbol, left=None, right=None):
        # frequency of symbol
        self.freq = freq

        # symbol name (character)
        self.symbol = symbol

        # node left of current node
        self.left = left

        # node right of current node
        self.right = right

        # tree direction (0/1)
        self.huff = ''

    def __lt__(self, nxt):
        return self.freq < nxt.freq


def read_and_save_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = file.read()
            # print("Data read from file:", data)
    except FileNotFoundError:
        print("File not found:", file_name)
    except Exception as e:
        print("An error occurred:", e)
    return data


def count_character_frequency(data):
    freq_counter = Counter(data)
    # initialising _dictionary

    # split dictionary into keys and values
    keys = list(freq_counter.keys())
    values = list(freq_counter.values())
    return keys, values


def build_huffman_tree(keys, values):
    count = 0
    # characters for huffman tree
    chars = keys

    # frequency of characters
    freq = values

    # list containing unused nodes
    nodes = []

    # converting characters and frequencies
    # into huffman tree nodes
    for x in range(len(chars)):
        heapq.heappush(nodes, node(freq[x], chars[x]))

    while len(nodes) > 1:
        # sort all the nodes in ascending order
        # based on their frequency
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)

        # assign directional value to these nodes
        left.huff = 0
        right.huff = 1

        # combine the 2 smallest nodes to create
        # new node as their parent
        newNode = node(left.freq + right.freq, count, left, right)
        count = count + 1

        heapq.heappush(nodes, newNode)
    return nodes


def printNodes(node, val=''):
    newVal = val + str(node.huff)
    if (node.left):
        printNodes(node.left, newVal)
    if (node.right):
        printNodes(node.right, newVal)
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")


def encode_text(text, huffman_tree):
    encoded_text = ''
    for char in text:
        encoded_text += get_huffman_code(char, huffman_tree)
    return encoded_text


def get_huffman_code(char, node, code=''):
    if node.left is None and node.right is None:
        if node.symbol == char:
            return code
    else:
        if node.left:
            left_code = get_huffman_code(char, node.left, code + '0')
            if left_code:
                return left_code
        if node.right:
            right_code = get_huffman_code(char, node.right, code + '1')
            if right_code:
                return right_code


def convert_to_bytes(encoded_text):
    # Define a mapping for special characters to unique codes
    numberOfPadBits = (8 - len(encoded_text) % 8)
    # Pad the encoded text to ensure its length is a multiple of 8
    padded_encoded_text = encoded_text + '0' * numberOfPadBits
    # Split the encoded text into chunks of 8 bits
    chunks = [padded_encoded_text[i:i + 8] for i in range(0, len(padded_encoded_text), 8)]

    # Convert each chunk to its corresponding character, handling special characters
    bytes_sequence = []
    for chunk in chunks:
        byte_value = int(chunk, 2)
        if byte_value < 32 or byte_value == 127:
            # Use escape mechanism for control characters
            bytes_sequence.append('\x1B' + chr(byte_value + 64))
        else:
            bytes_sequence.append(chr(byte_value))

    # Join the characters to form the byte sequence
    byte_sequence = ''.join(bytes_sequence)
    return byte_sequence, numberOfPadBits


def inorderTraversal(root):
    answer = []

    inorderTraversalUtil(root, answer)
    return answer


def inorderTraversalUtil(root, answer):
    if root is None:
        return

    inorderTraversalUtil(root.left, answer)
    answer.append(root.symbol)
    inorderTraversalUtil(root.right, answer)
    return


def preorderTraversal(root):
    answer = []
    preorderTraversalUtil(root, answer)
    return answer


def preorderTraversalUtil(root, answer):
    if root is None:
        return

    answer.append(root.symbol)
    preorderTraversalUtil(root.left, answer)
    preorderTraversalUtil(root.right, answer)
    return


def combine_and_write_to_file(compressed_sequence, inorder_sequence, preorder_sequence, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:  # Specify the encoding

        # Write compressed sequence
        file.write("Compressed sequence:\n")
        file.write(compressed_sequence + "\n")

        # Write inorder sequence
        file.write("Inorder sequence:\n")
        for item in inorder_sequence:
            file.write(str(item) + "\n")

        # Write preorder sequence
        file.write("Preorder sequence:\n")
        for item in preorder_sequence:
            file.write(str(item) + "\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: enter vaild file name")
        return
    fileName = sys.argv[1]
    data = read_and_save_file(fileName)  # Read and save file content
    keys, values = count_character_frequency(data)  # Create frequencies dictionary of each ascii
    nodes = build_huffman_tree(keys, values)  # Build huffman tree by the frequencies dictionary
    encodedText = encode_text(data, nodes[0])  # Encode the text using the huffman tree
    bytedText, numOfPad = convert_to_bytes(encodedText)  # Convert to bytes ( Padding if needed )
    # Perform inorder traversal
    inorder_result = inorderTraversal(nodes[0])
    # Perform preorder traversal
    preorder_result = preorderTraversal(nodes[0])
    combine_and_write_to_file(bytedText, inorder_result, preorder_result, "compressed.txt")  #



if __name__ == '__main__':
    main()