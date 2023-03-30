# Reflection
```
P' = TP
*T makes it so that multiplied with P is the reflection of P(P')
```
## y-axis
```
[-1, 0]
[ 0, 1]
```
## x-axis
```
[1,  0]
[0, -1]
```
## line y=x
```
[ 0, 1]
[ 1, 0]
```
# Scaling
```
[x, 0]
[0, 1]
[1, 0]
[0, y]
!!! Where x > 0, increase expansion in x-axis direction, vice versa
```
# Shearing
```
[1,x]
[0,1]
*0.5 to the right, -0.5 to the left
[1,0]
[y,1]
*0.5 to 45° up, -0.5 to 45° down
```
# Rotation
```
R = [cosθ, -sinθ] (anti-clockwise)
    [sinθ,  cosθ]
R = [cos-θ, -sin-θ] (clockwise)
    [sin-θ,  cos-θ]
P' = RP
*θ > 0 (anti-clockwise) θ < 0 (clockwise)
```
# Transformation
```
[1,0,x][a]
[0,1,y][b]
[0,0,1][1]
*Add 1 to the matrix point (homogeneous coordinates)
x > 0 to the right, x < 0 to the left
y > 0 upward, d < 0 downward
```
# Composition
```
C =T₃T₂T₁
P' = CP

C⁻¹ =T₁⁻¹T₂⁻¹T₃⁻¹
```
# Inverse
## Scaling
```
      [1/x, 0, 0]
T⁻¹ = [0, 1/y, 0]
      [0,   0, 1]
```
## Shearing
```
      [ 1,-x, 0]
T⁻¹ = [-y, 1, 0]
      [ 0, 0, 1]
*Must be mutually exclusive
```
## Rotation
```
T = [cosθ, -sinθ] (anti-clockwise)
    [sinθ,  cosθ]
T⁻¹ = [cos-θ, -sin-θ] (clockwise)
      [sin-θ,  cos-θ]
*vice versa
```
## Translation
```
      [1, 0, -x]
T⁻¹ = [0, 1, -y]
      [0, 0,  1]
```
# Gauss-Jordan (Additional)
```

*Your goal is to turn T into I
*All calculation must go by rows, Example: Take row 2 and add to row 1 (twice)
     [1 2 0][1 0 0]
TI = [0 1 0][0 1 0]
     [0 0 1][0 0 1]
       [1 2-(1*2) 0][1 0-(1*2) 0]
IT⁻¹ = [0 1       0][0 1       0]
       [0 0       1][0 0       1]
```
