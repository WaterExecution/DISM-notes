# Binary
```
Count in base 2
8 4 2 1
~~~~~~~	= 5 (Decimal)
0 1 0 1 
```

# Hexadecimal
```
Count in base 16
255 15
~~~~~~ = 31
 1   F
```

# Signed Binary
## 1's Complement
```
0111 = 7
0000 = 0
1111 = -0
1001 = -7
```
## 2's Complement
```
0111 = 7
0000 = 0
1111 = -1
1000 = -8
```
## Example
```
-0xDEADBEEF = 0x21524111 (0xFFFF FFFF - 0xDEAD BEEF)+1 (2's Compliment)
```

# Overflow
```
 1111
+0111
~~~~~
10110
*Extra bit from the allocated 4 bits 7 to -8(2's Complement)
```