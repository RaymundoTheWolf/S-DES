# S-DES
Repository for cryptography homework, teamed up with Yuyang Hu @[Gracivio](https://github.com/Gracivio), a S-DES instance.

# Introduction
S-DES, simple-data encryption standard, is a classic cryptography algorithm, which including mechanics such as **S-Boxes, P-Boxes, swapper function and shift function.**

# Features
In this instance, we create four features to choose from.
1. Generating Keys
   * Secrets module is used in this feature, which generate **10-bits random master key**. It's advised to protect the master key to guard the security of the algorithm(10-bits is easy to crack XD)
2. Encryption
   * Following S-DES process, we encrypt plain text along **initial permutation, round function(subkey 1), swap, round function(subkey 2) and reversed initial permutation** to get the cipher text. Also, ASCII encoding or binary encoding style are provided. Long text is also transformable.(There may be garbled code)
   * When encrypting the ASCII code in English, each letter will be encrypted in sequence according to an 8-bit length binary codes, and the result will be converted back to the ASCII code for output.
3. Decryption
   * Following S-DES process, we decrypt plain text along **initial permutation, round function(subkey 2), swap, round function(subkey 1) and reversed initial permutation** to get the plain text.
   * When it comes to long text, the process of decryption is as the same as the revese process of encryption.
4. Crack
   * Given plain text and corresponding cipher text to crack what master keys may be used. Showing potential keys on the screen.

# FYI
Since it's a executable file, there is no interface. Yet functions can be used.
