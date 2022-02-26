# Simple Proposition
```
1+1=2 (Proposition, True)
1+1=0 (Proposition, False)

There are 30 days in a month. (Non-proposition)
```

# Compound Proposition
## Number of rows
```
2ⁿ
```

## Negation(Not)
```
¬q converts from T to F & F to T.
```
| p | ¬q |
|---|----|
| T | F  |
| F | T  |
| T | F  |
| F | T  |

## Conjunction(And)
```
p^q pioritize "F" If it contains F, then p^q will be F. 
```
| p | q | p^q |
|---|---|-----|
| T | T | T   |
| F | T | F   |
| T | F | F   |
| F | F | F   |

## Disjunction(Or)
### Inclusive OR
```
p∨q pioritize "T" If it contains T, then p∨q will be T. 
```
| p | q | pVq |
|---|---|-----|
| T | T | T   |
| F | T | T   |
| T | F | T   |
| F | F | F   |

## Exclusive Disjunction(Xor)
### Exclusive OR
```
p⊻q 
if p and q are the same, p⊻q = F. 
if p are not the same q, p⊻q = T.
```
| p | q | p⊻q |
|---|---|-----|
| T | T | F   |
| F | T | T   |
| T | F | T   |
| F | F | F   |

## Implication (If)
```
p⇒q
if P = T and Q = F, p⇒q = F. The rest will be T.
```
| p | q | p⇒q |
|---|---|-----|
| T | T | T   |
| F | T | T   |
| T | F | F   |
| F | F | T   |

## Equivalence (IFF)
```
p⇔q 
if p and q are the same, p⇔q  = T. 
if p are not the same q, p⇔q  = F.
```
| p | q | p⇔q |
|---|---|-----|
| T | T | T   |
| F | T | F   |
| T | F | F   |
| F | F | T   |

# Truth Table for all logical operators

| p | q | ¬q (NOT) | p∨q (OR) | p^q (AND) | p⊻q (XOR) | p⇒q (IF) | p⇔q (IFF) |
|---|---|----------|----------|-----------|-----------|----------|-----------|
| T | T | F        | T        | T         | F         | T        | T         |
| F | T | T        | T        | F         | T         | T        | F         |
| T | F | F        | T        | F         | T         | F        | F         |
| F | F | T        | F        | F         | F         | T        | T         |

