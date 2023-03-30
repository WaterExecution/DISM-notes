# SUB 1
```
No, it gets the value from the address “1” and subtract the accumlator
```
# SUB two numbers
```
INP
STA data1
INP
SUB data1
OUT
HLT
data1   DAT
```
# LOOP until value is 0
```
        INP 
LOOP    OUT
        BRZ END 
        SUB ONE 
        BRA LOOP
END     HLT
ONE     DAT 1

```