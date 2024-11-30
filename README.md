
# Huffman Coding Compression and Decompression

## Overview
This repository implements Huffman coding for text compression and decompression in Python. It includes two scripts: one for compressing a text file and another for decompressing the compressed file.

## Features
- Compresses text files using Huffman coding.
- Includes preorder and inorder traversals of the Huffman tree in the compressed file.
- Decompresses the text file back to its original content using the provided Huffman tree.

## Files
- **`compression.py`**: Script to compress a text file.
- **`decompression.py`**: Script to decompress a previously compressed text file.
- **`Alice_in_wonderlands.txt`**: Example input text file for compression.
- **`compressed.txt`**: Example output of the compression script.
- **`decompressed.txt`**: Example output of the decompression script.

## How It Works

### Compression
1. Reads the input text file.
2. Constructs a Huffman tree based on character frequencies.
3. Encodes the text into a binary sequence and converts it into bytes for storage.
4. Stores the compressed sequence along with the inorder and preorder traversals of the Huffman tree.

### Decompression
1. Reads the compressed file to extract the compressed data and Huffman tree traversals.
2. Reconstructs the Huffman tree using the traversals.
3. Decodes the binary data back into the original text.

## Usage

### Compression
```bash
python compression.py Alice_in_wonderlands.txt
```
- **Input**: A text file (e.g., `Alice_in_wonderlands.txt`).
- **Output**: A file named `compressed.txt` containing:
  - The compressed sequence.
  - The inorder traversal of the Huffman tree.
  - The preorder traversal of the Huffman tree.

### Decompression
```bash
python decompression.py compressed.txt
```
- **Input**: A compressed file (e.g., `compressed.txt`).
- **Output**: A file named `decompressed.txt` containing the original text.

## Requirements
- Python 3.9 or above.
- No external libraries are required; the implementation uses Python's standard library.

## Notes
- This implementation avoids using pre-existing libraries for Huffman coding.
- Handles challenges such as mapping binary sequences to ASCII characters and managing dubious control characters.
