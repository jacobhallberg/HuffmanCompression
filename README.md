
<h1 align="center">Huffman Compression</h1>

<p align="center">A quick and easy way to compress your files.</p>

<p align="center"><a href="#site">Check It Out!</a> | <a href="#documentation">Read the Docs</a></p>

```
                  _    _        __  __                          _____          _ _             
                 | |  | |      / _|/ _|                        / ____|        | (_)            
                 | |__| |_   _| |_| |_ _ __ ___   __ _ _ __   | |     ___   __| |_ _ __   __ _ 
                 |  __  | | | |  _|  _| '_ ` _ \ / _` | '_ \  | |    / _ \ / _` | | '_ \ / _` |
                 | |  | | |_| | | | | | | | | | | (_| | | | | | |___| (_) | (_| | | | | | (_| |
                 |_|  |_|\__,_|_| |_| |_| |_| |_|\__,_|_| |_|  \_____\___/ \__,_|_|_| |_|\__, |
                                                                                          __/ |
                                                                                         |___/ 
 ```


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Explanation](#explanation)
- [Acknowldegements](#acknowledgements)
- [Some Useful Links](#some-useful-links)


## Prerequisites

Must have Python3 installed or the ability to run .exe .

## Getting Started

Operating Systems: Windows, Linux, Mac


There are a couple ways to download the compression application:
- [Download the zip](https://github.com/jacobhallberg/HuffmanCompression/archive/master.zip)
- Clone the repo: `git clone https://github.com/jacobhallberg/HuffmanCompression.git` 

To Run type:
```
$ python3 exeEncode.py
```
Or run the .exe directly.

## Explanation

A Huffman Coding counts the frequencies of each character and creates binary codes decreasing in length for the characters with higher frequency.
After encoding the file, a corresponding codebook is needed to decode the file providing space savings and privacy for the user with the codebook.

For more information, please refer to the [Wikipedia Page](https://en.wikipedia.org/wiki/Huffman_coding).

## License
MIT License - see the [LICENSE](https://github.com/jacobhallberg/HuffmanCompression/blob/master/LICENSE) file for more details.

### Some Useful links

- **Theoretical Encoding Limit:** https://en.wikipedia.org/wiki/Entropy_(information_theory)
- **Huffman Encoding Algorithm:** https://www.geeksforgeeks.org/greedy-algorithms-set-3-huffman-coding/
