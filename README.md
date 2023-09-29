# About this repository
* A Repository for cryptography homework of S-DES instance, teamed up with Yuyang Hu @[Gracivio](https://github.com/Gracivio).

# Introduction of S-DES
* S-DES, simple-data encryption standard, is a classic cryptography algorithm, which including mechanics such as **S-Boxes, P-Boxes, swapper function and shift function.**

# Features
In this instance, we created four features to choose from.
1. Generating Keys
   * Secrets module is used in this feature, which generate **10-bits random master key**. It's advised to protect the master key to guard the security of the algorithm.(10-bits is easy to crack XD)
2. Encryption
   * Following S-DES process, we encrypt plain text along **initial permutation, round function(subkey 1), swap, round function(subkey 2) and reversed initial permutation** to get the cipher text. Also, ASCII encoding or binary encoding style are provided. Long text is also transformable.(There may be garbled code in long text transformation)
   * When encrypting the ASCII code in English, each letter will be encrypted in sequence into an 8-bit length binary code, and the result will be converted back to the ASCII code for output.
3. Decryption
   * Following S-DES process, we decrypt plain text along **initial permutation, round function(subkey 2), swap, round function(subkey 1) and reversed initial permutation** to get the plain text.
   * When it comes to long text, the process of decryption is as the same as the process of encryption except the order key used in the process.
4. Crack
   * Given plain text and corresponding cipher text to crack what master keys may be used. Showing potential keys on the screen and displaying the time to crack out the keys.
   * Crack process information will be displayed in the terminal.
   * ASCII and binary styles are provides, however the garbled code issue cannot fixed, you can only copy the garbled code for some of ASCII crack processes.

# GUI
* We use **tkinter** and **ttkbootstrap** for user interface. Relative layout is used for best compatibility.(Although some devices may see wrong layout due to screen size)

# How to use
* Download the S-DES.py above and run it and you need to download some python packages to meet the environment this application runs on including **tkinter and ttkbootstrap**
* For the key is presented on screen with password form, which is demonstrated as '*', you should mark your key so that you can use it correctly.

# Test results
* Check *Test Results.md* for the test results, gif is provided for better demonstration

# FYI
* Since it's a executable file, there is no interface. Yet functions that intergerned in this file can be used.
