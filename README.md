# S-DES
Repository for cryptography homework, teamed up with Yuyang Hu, a S-DES instance.

# Introduction
S-DES, simple-data encryption standard, is a classic cryptography algorithm, which including mechanics such as S-Boxes, P-Boxes, swapper function and shift function.

# Features
In this instance, we create four features to choose from.
1. Generating Keys
   Secrets module is used in this feature, which generate 10-bits random master key. It's advised to protect the master key to guard the security of the algorithm(10-bits is easy to crack XD)
2. Encryption
   Following S-DES process, we encrypt plain text along initial permutation, round function(subkey 1), swap, round function(subkey 2) and reversed initial permutation to get the cipher text.
3. Decryption
   Following S-DES process, we decrypt plain text along initial permutation, round function(subkey 2), swap, round function(subkey 1) and reversed initial permutation to get the plain text.
4. Crack
   Given plain text and corresponding cipher text to crack what master keys may be used. Showing potential keys on the screen.
