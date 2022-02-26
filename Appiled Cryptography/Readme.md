# Chapter 1
## Cipher
![](https://i.imgur.com/YigtkWw.png)

### Subtitution Ciphers
#### Caesar Chiper
> Key - Number 
> Rotate X position
#### Monoalphabetic Cipher
> Key - Randomized alphabet position
#### Playfair Cipher*
> Key - Create Table (No J)
> Add 'X' as filler for plain-text 
> Swap L-to-R or R-to-L  based on a "box" formed from the pair of plain-text alphabets on the table
> If box is single column (Take bottom) If box is single row (Take right)
### Polyalphabetic Cipher
#### Vignere Cipher
> Key - Table (Row A-Z →, Column A-Z ↓)
> A-Z
> ... (Shift 1)
> Z-Y
> Repeated key to match plaintext
> From table, align alphabet from plain-text and key to get new alphabet
### Transposition Ciphers
#### Rail Fence Cipher*
> Key - Number of rows
#### Row Transposition Cipher
> Key = Number of columns then randomize column position
> Write alphabet within number of column
#### Rotor Machines
>  Used series of cylinders, each giving 1 substitution, which rotates  after each letter is encrypted
#### Product Cipher
> Multiple ciphers
> Modern cipher is subsitution then transposition

## Symmetric Encryption
```
single shared key
Problem of distributing secret key securely
fast encryption and decryption
Lower chance for Chosen-Plaintext attack
```
## Asymmetric Encryption
```
public private key pair
Can distribute public key freely and safely
usually much slower speed compared to symmetric ciphers
Subject to Chosen-Plaintext attack as public key is open
```
## Cryptanalysis
### Cryptanalytic Attacks
```
known ciphertext
known plaintext
chosen plaintext
chosen ciphertext
chosen text
```
### Brute force search
```
4 bit keys = 16(2^4)
Key/s = 1
Average decryption speed = 8 seconds ((2^4/2)/1) (Divide by 2 for average time)
```

# Chapter 2
## Block cipher
```
Encrypt/decrypt data in blocks typically 64/128bits
Based on substitution-permutation networks
```
## Stream cipher
```
Encrypt/decrypt data in bits or bytes at a time
```
## Diffusion
```
Dissipates statistical structure of plaintext over bulk of ciphertext (permutation/transposition)
```
## Confusion
```
Makes relationship between ciphertext and key as complex as possible (Substitution)
```
## Permutation
```
Straight P-box 32->32
Compression P-box 48->32
Expansion P-box 32->48
```
## Fiestel
> Decryption is same except key is in reverse order
https://www.youtube.com/watch?v=drI2shandyk
 ## DES
 > Decryption is same except key is in reverse order
https://www.youtube.com/watch?v=SaZGjQBItBc

# Chapter 3
|         | Block Size | Rounds |
|---------|------------|--------|
| AES-128 | 128        | 10     |
| AES-192 | 128        | 12     |
| AES-256 | 128        | 14     |


## AES
> First start with add round key, last round no mix column
https://www.youtube.com/watch?v=vZ7YQ67Cbtc

# Chapter 8
# RSA formula
```
n = pq
φ(n) = (p-1)(q-1)
c = M^e mod n 
M = c^d mod n
```
![](https://i.imgur.com/H1RwDTV.png)

![](https://i.imgur.com/DUkgMyI.png)

## RSA benefits
```
Key distribution – enable secure communication without having to trust a KDC with your key
Digital Signature – enable verification of a message form the claimed sender
```
## RSA Attacks
```
Brute-force attack
Mathematical attack
Chosen Ciphertext attack (Mitigate with OAEP)
Timing attack (Mitigate with delays)
Power Cryptanalysis (AKA side channel attack)
Software bugs
```

# Chapter 9
## Diffie Hellman Key Exchange Formula
```
p (prime), g (primitive root)
A (alice's public key) = g^a (alice's private key) mod p
K = A^b mod p or B^a mod p
```

# Chapter 10
```
Digital Signature (DSS/SHA-1 or RSA/SHA)
Message Encryption (CAST or IDEA or 3-DES w/ DH or RSA)
Compression
E-mail compatibility
Segmentation and reassembly
```
https://www.youtube.com/watch?v=lcBpC1RsWsw

# Chapter 11
>A blind signature is  a form of digital signature in which the content of a message is disguised (blinded) before it is signed 

https://www.youtube.com/watch?v=Fu82aJJ3tQQ
https://www.youtube.com/watch?v=BkRLp7rYnc4

# Extras
![](https://i.imgur.com/qqUFwkr.png)

https://www.youtube.com/watch?v=v1JwSaAqVNY
https://www.youtube.com/watch?v=Fr2fQlQIokY