import sys
sys.path.append('/home/jacob/Downloads/PythonPractice/HuffmanEncoding')
import unittest
import huffman


class TestHuffmanFunctions(unittest.TestCase):

    def test_calculate_frequency(self):
        test_string1 = "apples"
        test_string2 = "oranges"
        result1 = {'a': 1, 'p': 2, 'l': 1, 'e': 1, 's': 1}
        result2 = {'o': 1, 'r': 1, 'a': 1, 'n': 1, 'g': 1, 'e': 1, 's': 1}
        self.assertEqual(huffman.calculate_frequency(test_string1), result1)
        self.assertEqual(huffman.calculate_frequency(test_string2), result2)



if __name__ == '__main__':
    unittest.main()