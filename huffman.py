import heapq
import os

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        
    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
            
        def __lt__(self, other):
            return self.freq < other.freq
            
        def __eq__(self, other):
            if other == None:
                return False
            if not isinstance(other, HuffmanCoding.HeapNode):
                return False
            return self.freq == other.freq
            
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency
        
    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)
            
    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(self.heap, merged)
            
    def make_codes_helper(self, root, current_code):
        if root is None:
            return
            
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
            
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")
        
    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)
        
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text
        
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
            
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text
        
    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)
            
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b
        

    def compress(self):
        # Get file name without extension
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        
        with open(self.path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read()
            
            # Make frequency dictionary using the text
            frequency = self.make_frequency_dict(text)
            
            # Convert the frequency dictionary to bytes using pickle
            import pickle
            freq_bytes = pickle.dumps(frequency)
            
            # Write the size of the frequency dictionary and the dictionary itself
            # Format: [size of freq_dict (4 bytes)][freq_dict][encoded data]
            output.write(len(freq_bytes).to_bytes(4, byteorder='big'))
            output.write(freq_bytes)
            
            # Construct the heap from the frequency dict
            self.make_heap(frequency)
            
            # Merge nodes
            self.merge_nodes()
            
            # Make codes
            self.make_codes()
            
            # Create the encoded text
            encoded_text = self.get_encoded_text(text)
            
            # Pad this encoded text
            padded_encoded_text = self.pad_encoded_text(encoded_text)
            
            # Get the encoded text as bytes
            b = self.get_byte_array(padded_encoded_text)
            
            # Write bytes to the output file
            output.write(bytes(b))
            
        return output_path



    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        
        return encoded_text
        
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
                
        return decoded_text
        
    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"
        
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            # Read the size of the frequency dictionary
            import pickle
            freq_size = int.from_bytes(file.read(4), byteorder='big')
            
            # Read the frequency dictionary
            freq_bytes = file.read(freq_size)
            frequency = pickle.loads(freq_bytes)
            
            # Rebuild the Huffman tree
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            
            # Read the encoded data
            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            
            encoded_text = self.remove_padding(bit_string)
            
            decompressed_text = self.decode_text(encoded_text)
            
            output.write(decompressed_text)
        
        return output_path