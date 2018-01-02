# Author: Jacob Hallberg
# Last Edited: 12/30/2017
"""
Takes in some text file and calculates the freguency of each character.
Using the frequency it constructs a min-heap implementation of a Huffamn Tree
wich will be used to create a Huffman Coding. After encoding, returns a 
compressed file and a codebook with locations specified by user.
"""
import heapq
import json
from tree import Tree


def calculate_frequency(s_file):
    # Takes in a read file and creates a key, value dict.
    # Key denotes the character and value denotes the frequency.
    frequency_dic = {}

    # Iterate character by character and check if found within dict.
    # Note: May want to rewrite for speed.
    for character in s_file:
        if character in frequency_dic:
            # Chacter found increment frequency.
            frequency_dic[character] += 1
        else:
            # Character not found create key with value 1.
            frequency_dic.update({character: 1})

    return frequency_dic


def create_codebook(heap_node):
    codebook = {}
    code = traverse_tree(heap_node, '')
    
    for key, value in code:
        codebook.update({key: value})

    return codebook


def traverse_tree(heap_node, char_seed):
    # Recursive function:
    #  If there is a left child or right child recurse until there isn't.
    #  Build back up in a in-order-traversal.

    # Checks if the passed in node is a leaf node.
    # If it has children, recurse.
    if isinstance(heap_node[1][1], Tree):
        e_1 = traverse_tree(heap_node[1][1].left_child, char_seed + '0')
        e_2 = traverse_tree(heap_node[1][1].right_child, char_seed + '1')

        # Build back up huffman encoding by concating the returned strings.
        return e_1 + e_2
    else:
        # Leaf node found, no recursing needed. return created code.
        code = [(heap_node[1][1], char_seed)]
        return code


def write_binary_encoding(encoding, file_name):
    # As we need to write to the binary file in bytes, we must first
    #   check for left over bits that don't form a byte and concat
    #   '0's to them until they form a byte.

    # leftover_bits are bits that can't form a byte.
    # Example:
    #          00100  '5 bits, need 3 more'
    #          00100 + 000 '8 bits, we have a byte'
    leftover_bits = len(encoding) % 8

    with open(file_name, 'wb') as binary_file:
        if leftover_bits != 0:
            encoding += '0' * (8 - leftover_bits)

        # Create a bytearray to store all of the bits into a file.
        byte = bytearray(int(encoding[i:i + 8], 2)
                         for i in range(0, len(encoding), 8))
        binary_file.write(byte)
    return file_name


def write_code_book(code_book, file_name):
    # Using json to write dictionary to file in readable format.
    with open(file_name, 'w') as code:
        json.dump(code_book, code)


def decode_file(code_book_file, file_name):
    symbol, decoded_file, bit_string = "", "", ""

    with open(code_book_file, 'r') as code:
        code_book = json.load(code)

    with open(file_name, 'rb') as byte_stream:
        for byte in byte_stream.read():
            bit_string += format(byte, '08b')

        # Iterate through specified length so that we don't decode added zeros.
        # Concat bits to a symbol until it matches a code in the code_book.
        for i in range(0, code_book['length']):
            symbol += bit_string[i]

            # If its found, concat with decoded file and reset process.
            if symbol in code_book:
                decoded_file += code_book[symbol]
                symbol = ""
    print(decoded_file)
    return decoded_file


def create_encoding(freq_dic, s_file):
    # Heapq cannot compare objects, so in the case that we have a tie
    #  the tie is broken with the count variable. Silly, but functional.
    count = 0

    # Using a list a heap sead, we iterate through the freq dic and
    #  create construct the heap node by node.
    m_heap = []
    for key, value in freq_dic.items():
        heapq.heappush(m_heap, (value, (count, key)))
        count += 1

    # While there are two are more nodes in the heap, we pop smallest (by freq)
    #  nodes from the priority queue and combine them.

    #  Example:
    #                    (ac:3) <- newly combined node, re-inserted in heap.
    #                    /    \
    # popped node -> (a:1)  (c:2) <- popped node

    while len(m_heap) > 1:
        count += 1
        node_1 = heapq.heappop(m_heap)
        node_2 = heapq.heappop(m_heap)

        parent_node = node_1[0] + node_2[0]

        if node_1[0] <= node_2[0]:
            tree_data = Tree(parent_node, node_1, node_2)
        else:
            tree_data = Tree(parent_node, node_2, node_1)
        heapq.heappush(m_heap, (parent_node, (count, tree_data)))

    # If there is one node left in the heap, we have successfully combined all
    #  of the previously popped nodes into one huffman tree.
    #  We now iterate over the tree and create the code.
    if len(m_heap) == 1:
        code_book = create_codebook(heapq.heappop(m_heap))

    # Convert the string_file to a list and iterate over each char and replace
    #  with the coresponding code from the code_book.
    encoding = list(s_file)
    for i in range(0, len(encoding)):
        encoding[i] = code_book[encoding[i]]

    # Join the list back to a string and flip the code_book for later use.
    encoding = ''.join(encoding)
    flipped_code_book = dict(zip(code_book.values(), code_book.keys()))
    flipped_code_book.update({'length': len(encoding)})

    return encoding, flipped_code_book
