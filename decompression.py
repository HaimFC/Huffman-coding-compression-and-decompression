import sys

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def extract_data(file_path):

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the index of "Inorder sequence::"
    end_index = lines.index("Inorder sequence:\n")

    # Extract lines before "Inorder sequence::"
    data_before_inorder = lines[1:end_index]

    # Join the lines into a single string
    data_before_inorder_str = ''.join(data_before_inorder)

    # Printing or doing whatever you want with the data
    return(data_before_inorder_str)

def process_inorder_sequence(file_path):
    inorder_sequence = []

    # Open the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Flag to determine if we're reading the inorder sequence
        is_inorder = False

        # Flag to track if the previous line was blank
        prev_line_blank = False

        # Iterate through the lines
        for line in file:
            # Check if the line indicates the start of the inorder sequence
            if is_inorder:
                # Check if the line indicates the start of the preorder sequence
                if line.strip() == "Preorder sequence:":
                    break  # Stop processing after reaching the end of the inorder sequence
                # Check if the line is blank
                elif not line.strip():
                    if prev_line_blank:
                        # If there are two consecutive blank lines, replace the last item with '\n'
                        inorder_sequence.pop()
                        inorder_sequence.append('\n')
                    else:
                        inorder_sequence.append(' ')
                    prev_line_blank = True
                    continue
                else:
                    inorder_sequence.append(line.strip())
                    prev_line_blank = False
            elif line.strip() == "Inorder sequence:":
                is_inorder = True

    return inorder_sequence

def process_preorder_sequence(file_path):
    preorder_sequence = []

    # Open the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Flag to determine if we're reading the preorder sequence
        is_preorder = False

        # Flag to track if the previous line was blank
        prev_line_blank = False

        # Iterate through the lines
        for line in file:
            # Check if the line indicates the start of the preorder sequence
            if is_preorder:
                # Check if the line is blank
                if not line.strip():
                    if prev_line_blank:
                        # If there are two consecutive blank lines, replace the last item with '\n'
                        preorder_sequence.pop()
                        preorder_sequence.append('\n')
                    else:
                        preorder_sequence.append(' ')
                    prev_line_blank = True
                    continue
                else:
                    preorder_sequence.append(line.strip())
                    prev_line_blank = False
            elif line.strip() == "Preorder sequence:":
                is_preorder = True

    return preorder_sequence

def cast_numbers_to_int(lst):
    new_lst = []
    for item in lst:
        if item.isdigit():  # Check if the item is a number
            new_lst.append(int(item))  # Convert to integer and append to the new list
        else:
            new_lst.append(item)  # Keep the item as it is if it's not a number
    return new_lst

def build_tree(inorder, preorder):
    if not inorder or not preorder:
        return None

    # Find root node
    root_val = preorder.pop(0)
    root = TreeNode(root_val)

    # Find index of root in inorder
    root_index = inorder.index(root_val)

    # Recursively construct left and right subtrees
    root.left = build_tree(inorder[:root_index], preorder)
    root.right = build_tree(inorder[root_index + 1:], preorder)

    return root

def assign_binary_codes(root, code, codes):
    if root is None:
        return

    # If leaf node is reached, assign code to the character
    if isinstance(root.val, str):
        codes[root.val] = code
        return

    # Traverse left subtree with adding '0' to code
    assign_binary_codes(root.left, code + '0', codes)

    # Traverse right subtree with adding '1' to code
    assign_binary_codes(root.right, code + '1', codes)

def convert_to_binary(byte_sequence):
    binary_sequence = ""

    i = 0
    while i < len(byte_sequence):
        if byte_sequence[i] == '\x1B':  # Check for escape sequence
            # Decode the escaped character
            escaped_char = ord(byte_sequence[i + 1]) - 64
            binary_sequence += format(escaped_char, '08b')  # Convert the ASCII value to binary and append to the sequence
            i += 2  # Skip to the next character after the escape sequence
        else:
            # Convert the character to binary and append to the sequence
            binary_sequence += format(ord(byte_sequence[i]), '08b')
            i += 1

    return binary_sequence

def decode_huffman_text(bin_text, huffman_tree):
    decoded_text = ''
    current_node = huffman_tree

    for bit in bin_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if isinstance(current_node.val, str):  # If current node is a leaf node
            decoded_text += current_node.val
            current_node = huffman_tree  # Reset to the root for next character

    return decoded_text

def write_to_text_file(data, filename):
    try:
        with open(filename, 'w') as file:
            file.write(data)
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: enter vaild file name")
        return
    fileName = sys.argv[1]
    data = extract_data(fileName)
    inorder_list = process_inorder_sequence(fileName)
    inorder_list = cast_numbers_to_int(inorder_list)
    preorder_list = process_preorder_sequence(fileName)
    preorder_list = cast_numbers_to_int(preorder_list)
    root = build_tree(inorder_list, preorder_list)
    codes = {}
    assign_binary_codes(root, '', codes)
    binText = convert_to_binary(data)
    dec_Text = decode_huffman_text(binText, root)
    write_to_text_file(dec_Text, "decompressed.txt")

if __name__ == '__main__':
    main()