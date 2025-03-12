# Huffman Coding Text File Compressor

A web-based application that compresses and decompresses text files using Huffman coding algorithm.

## Overview

This application provides a simple and intuitive interface for users to compress text files and reduce their size without losing any information. The implementation uses the Huffman coding algorithm, which creates variable-length codes for characters based on their frequency in the text.

## Features

- **Text File Compression**: Upload any text file and download its compressed version (.bin)
- **File Decompression**: Upload compressed files and recover the original text
- **User-Friendly Interface**: Drag and drop functionality with intuitive design
- **Efficient Compression**: Achieves approximately 47% reduction in file size
- **Lossless Compression**: Guarantees that the decompressed file is identical to the original

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Algorithm**: Huffman Coding
- **Serialization**: Python's pickle library

## How It Works

1. **Compression Process**:
   - Analyzes character frequencies in the input text
   - Constructs a Huffman tree based on these frequencies
   - Generates a dictionary of variable-length binary codes
   - Replaces each character with its corresponding code
   - Stores frequency information in the file header
   - Outputs a compressed binary file

2. **Decompression Process**:
   - Reads the frequency information from the file header
   - Reconstructs the Huffman tree
   - Decodes the binary data back to the original text
   - Returns the original text file

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/satvik202/File-Compression-Huffman-coding/
   cd File-Compression-Huffman-coding
   ```

2. Install the required packages:
   ```
   pip install flask
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

```
huffman-file-compressor/
├── app.py              # Flask application
├── huffman.py          # Huffman coding implementation
├── templates/
│   └── index.html      # Frontend interface
└── uploads/            # Directory for uploaded files
```

## How to Use

1. **Compressing a File**:
   - Click on the upload area or drag and drop a text file
   - Click "Compress File"
   - The compressed file will be downloaded automatically

2. **Decompressing a File**:
   - Click on the upload area in the decompression section
   - Upload a previously compressed .bin file
   - Click "Decompress File"
   - The original text file will be downloaded automatically

## Algorithm Details

The Huffman coding algorithm creates an optimal prefix code for lossless data compression. It works by:

1. Calculating the frequency of each character in the text
2. Building a binary tree where characters with higher frequencies have shorter paths
3. Generating variable-length codes for each character
4. The most frequent characters get shorter codes, while less frequent ones get longer codes

This approach minimizes the overall size of the encoded text.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project implements the Huffman coding algorithm developed by David A. Huffman
- Frontend design inspired by modern web applications