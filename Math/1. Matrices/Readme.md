# Matrix
```
[1,2,3]
[4,5,6]
[7,8,9]
```
# Subscript notation
```
M = [1,2,3]
    [4,5,6]
    [7,8,9]
M₃₁ = 7 (Row 3 Column 1)
```

# Special Matrices
## Row Matrix
```
[1,2,3]
```
## Column Matrix
```
[1]
[2]
[3]
```
## Square Matrix
```
[1,2,3]
[4,5,6]
[7,8,9]
*number of column and row is same
```
## Diagonal Matrix
```
[1,0,0]
[0,2,0]
[0,0,3]
*Can be written as diag[1,2,3]
*A square matrix which elements outside the diagonal are zero
```
## Identity Matrix
```
[1,0,0]
[0,1,0]
[0,0,1]
Can be written as I₃
*Diagonal Matrix but elements are 1
```
## Zero/Null Matrix
```
[0,0,0]
[0,0,0]
[0,0,0]
*All elements are 0
```
## Symmetric Matrix
```
Matrix = Matrixᵀ
ex:
[0,2,3]
[2,1,2]
[3,2,0]
```

# Matrix Operation
## Addition
```
[2,x]	[3,y]	[5,x+y]
[3,0] +	[1,2] =	[4 ,2 ]
```
## Transpose 
```
[1,2,3]ᵀ	[1,4,7]
[4,5,6]	=	[2,5,8]
[7,8,9]		[3,6,9]

[1,2,3]ᵀ	[1,4]
[4,5,6]	=	[2,5]
		[3,6]

		[1]
[1,2,3]ᵀ =	[2]
		[3]
```
## Multiplication
```
row * column
[a,b,c]	  [x,2]	  [a*x+b*y+c*z,28]
[4,5,6] x [y,4] = [49,64]
	  [z,6]		
```
### Conformability
```
Column = Row
2x3, 3x4 = 2x4
*Multiplication of two matrices is defined if and only if the number of columns of the left matrix is the same as the number of rows of the right matrix
```

# Inverse Matrix
```
1/A = A⁻¹ since cannot use a matrix to divide (1/[a,b])
A⁻¹ * A = I (1)(Identity Matrix)

(AB)⁻¹ ≠ A⁻¹B⁻¹
(AB)⁻¹ = B⁻¹A⁻¹

Proof:
AB(AB)⁻¹ = I
A⁻¹AB(AB)⁻¹ = A⁻¹ * I
1B⁻¹B(AB)⁻¹ = B⁻¹A⁻¹ * I
(AB)⁻¹ = B⁻¹A⁻¹ * I
```
