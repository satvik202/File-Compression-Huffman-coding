
'''
accessing files
min heap to get the 2 nodes with minimum character frequency
We'll need a binary tree class as well

construct the encoded text from the passed text
return the encoded binary file

'''
import os, heapq

class BinaryTree :
    def __init__(self, value, frequency) -> None:
        #node will have a value and frequency.
        #value -> character
        #corresponding frequency
        self.value= value
        self.frequency = frequency

        self.left= None
        self.right= None

    #need to define __lt__ and __eq__ (less ad equal)
    def __lt__(self, other):
        return self.frequency < other.frequency
    

    def __eq__(self, other):
        return self.frequency == other.frequency



class HuffmanCompression :

    def __init__(self, path) -> None:
        self.path= path

        #iterable for heap
        self.__heap= []
        

        #we need a dictionary to map huffman matching and character

        self.__code = {}       # character to code map

        self.__reversecode= {} # code to character map



    def __frequency_from_text(self,text) :
        frequency_dictionary = {}
        
        #traversing in text character by character

        for char in text :
            if char not in frequency_dictionary:
                frequency_dictionary[char]=1


            frequency_dictionary[char]+=1



        return frequency_dictionary


    def __build_heap(self, frequency_dict) :

        for key in frequency_dict :
            frequency = frequency_dict[key]

            #we'll make a node with elm as value and frequency as frequency & then push it in the heap

            node = BinaryTree(key , frequency) 
            heapq.heappush(self.__heap, node)


    def __build_huffman_tree(self) :

        while len(self.__heap) > 1 :
            node1= heapq.heappop(self.__heap)
            node2= heapq.heappop(self.__heap)

            #merge nodes
            merged_node = BinaryTree(None, node1.frequency + node2.frequency) #key will be none.

            merged_node.left= node1
            merged_node.right= node2

            #pushing it in heap
            heapq.heappush(self.__heap, merged_node)

        #we are here means heap has only one element
        #this element is the huffman tree
            
        return self.__heap[0]
    
    
    def __build_tree_code_helper(self, root, current_code) :
        if root is None :
            return 
        
        #we have values only for leaf nodes 

        if root.value is not None :
            self.__code[root.value] = current_code
            self.__reversecode[current_code] = root.value
            return
        
        #left will be 0 & right will be 1
        self.__build_tree_code_helper(root.left, current_code+'0')
        self.__build_tree_code_helper(root.right, current_code+'1')
    
    
    def __build_tree_code(self) :
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root,'')
        
    
    def __build_encoded_text(self , text) :
        encoded_text = ''

        for char in text :
            #replace each character with it's huffman matching binary string
            encoded_text+= self.__code[char]

        return encoded_text
            

    def __build_padded_encoded_text(self, encoded_text) :
        #to ensure that the binary data has a consistent length.
        padding_len = 8 - len(encoded_text)%8

        for i in range(0, padding_len) :
            encoded_text+='0'

        # 8 bit string with leading zeros
        padded_info= format(padding_len, "08b")

        return padded_info+encoded_text


    def __build_byte_array(self, padded_text) :
        #In binary
        byte_array= []
        #Increment with 8 in order to slice it to one byte
        for i in range(0, len(padded_text), 8):
            byte= padded_text[i:i+8]

            byte_array.append(int(byte,2))
        
        return byte_array

    def compression(self) :
        print("starting compression\n")

        #we need to return an output file !
        output_path = 'compressed_output' + '.bin'

        #let's read the txt file. the self

        with open(self.path , "r") as file :
            text = file.read().rstrip() #remove the trailing spaces from the file


            frequency_dict = self.__frequency_from_text(text)

            #  print(f'Frequency Dictionary: \n{frequency_dictionary}\n')

            #now that we have the frequency table
            #let's create the min heap

            self.__build_heap(frequency_dict)

            #so the heap is built now.

            # now we'll build the huffman tree

            #It's built based on the frequency of characters in a dataset, with the most frequent characters having the shortest paths. 
            #The tree is constructed by pairing the least frequent nodes until only one node, the root, remains.

            huffman_tree = self.__build_huffman_tree()

            #we have to map each character to a unique code of 0s & 1s

            self.__build_tree_code()
            # print(f'Code Dictionary: \n{self.__code}\n')

            encoded_text= self.__build_encoded_text(text)

            #Uncomment to see the encoded text
            # print(f'Encoded Text: \n{encoded_text}\n')

            #now we need to do padding. it is possible that our code is not in 8bit (1byte) format
            #we'll add additional 0's at the ending to make it a 08b format

            padded_encoded_text= self.__build_padded_encoded_text(encoded_text)

            #Uncomment to see the padded encoded text
            # print(padded_encoded_text)



            #Inorder to read convert it into bytes
            bytes_array= self.__build_byte_array(padded_encoded_text)



             #Convert bytes array to final bytes
            final_bytes= bytes(bytes_array)

            # print(final_bytes)

            with open(output_path, 'wb') as output:
                output.write(final_bytes)

            print("Compressed successfully....")
            
            return output_path




one = HuffmanCompression('alice_in_wonderland.txt')

frequency_dictionary= one.compression()