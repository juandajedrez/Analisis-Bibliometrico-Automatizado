# Jaccad distance
## Función
```python
from typing import Set


def generate_ngrams(text: str, n: int) -> Set[str]:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    lowered = text.lower()
    length = len(lowered)
    if length < n:
        return set()
    return {lowered[i : i + n] for i in range(length - n + 1)}


def jaccard_distance(s1: str, s2: str, n: int = 2) -> float:
    grams1 = generate_ngrams(s1, n)
    grams2 = generate_ngrams(s2, n)

    intersection = grams1.intersection(grams2)
    union = grams1.union(grams2)

    if not union:
        return 0.0

    similarity = len(intersection) / len(union)
    return 1.0 - similarity

```

## Formula matemática
$$
J(A,B) = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}
$$

## Ejemplo
string ="Airport agencies"
n-ngrama=3
length=17-3+1=15


| i         | i<length    | string[i:i+n]  |Resultado |
|-----------|--------------|---------------|----------| 
|0          |i1<15         |string[0:3]    | air      |
|1          | 1<15         |string[1:1+3]  | irp      |
|2          |2<15          |string[2:2+3]  | rpo      |
|3          |3<15          |string[3:3+3]  |por       |
|4          |4<15          |string[4:4+3]  |ort       |
|5          |5<15          |string[5:5+3]  |rt        |
|6          |6<15          |string[6:6+3]  |t a       |
|7          |7<15          |string[7:7+3]  |ag        |
|8          |8<15          |string[8:8+3]  |age       |
|9          |8<15          |string[9:9+3]  |gen       |
|10         |10<15         |string[10:10+3]|enc       |
|11         |11<15         |string[11:11+3]|nci       |
|12         |12<15         |string[12:12+3]|cie       |
|13         |13<15         |string[13:13+3]|ies       |


# Distance LCS

## Código
```python

def editDistanceWith2Ops(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0 for x in range(n + 1)] for y in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    lcs = L[m][n]
    return (m - lcs) + (n - lcs)
```


## Código

```python
def levenshtein_iterative(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

```
## 2. Datos de prueba

| Variable | Descripción | Valor |
|-----------|--------------|--------|
| X | Cadena 1 | "tab" |
| Y | Cadena 2 | "tabe" |
| m | Longitud de X | 3 |
| n | Longitud de Y | 4 |
| L | Matriz (m+1) × (n+1) inicializada en 0 | 4 × 5 |

---

## 3. Tabla que se construye

La matriz L almacena en `L[i][j]` la longitud de la subsecuencia común más larga entre `X[:i]` y `Y[:j]`.

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 |   |   |   |   |
| 2 | 0 |   |   |   |   |
| 3 | 0 |   |   |   |   |

---

### Paso 1: i = 1 ('t')

| j | X[i-1] | Y[j-1] | Resultado | L[i][j] |
|---|---------|---------|------------|----------|
| 1 | 't' = 't' | iguales | L[1][1] = L[0][0] + 1 | 1 |
| 2 | 't' ≠ 'a' | L[1][2] = max(L[0][2], L[1][1]) | 1 |
| 3 | 't' ≠ 'b' | L[1][3] = max(L[0][3], L[1][2]) | 1 |
| 4 | 't' ≠ 'e' | L[1][4] = max(L[0][4], L[1][3]) | 1 |

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 2 | 0 |   |   |   |   |
| 3 | 0 |   |   |   |   |

---

### Paso 2: i = 2 ('a')

| j | X[i-1] | Y[j-1] | Resultado | L[i][j] |
|---|---------|---------|------------|----------|
| 1 | 'a' ≠ 't' | max(L[1][1], L[2][0]) | 1 |
| 2 | 'a' = 'a' | L[2][2] = L[1][1] + 1 | 2 |
| 3 | 'a' ≠ 'b' | max(L[1][3], L[2][2]) | 2 |
| 4 | 'a' ≠ 'e' | max(L[1][4], L[2][3]) | 2 |

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 2 | 2 | 2 |
| 3 | 0 |   |   |   |   |

---

### Paso 3: i = 3 ('b')

| j | X[i-1] | Y[j-1] | Resultado | L[i][j] |
|---|---------|---------|------------|----------|
| 1 | 'b' ≠ 't' | max(L[2][1], L[3][0]) | 1 |
| 2 | 'b' ≠ 'a' | max(L[2][2], L[3][1]) | 2 |
| 3 | 'b' = 'b' | L[3][3] = L[2][2] + 1 | 3 |
| 4 | 'b' ≠ 'e' | max(L[2][4], L[3][3]) | 3 |

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | 1 |
| 2 | 0 | 1 | 2 | 2 | 2 |
| 3 | 0 | 1 | 2 | 3 | 3 |
## Formula matemática

$$
O\left(2^{n_{1}} \sum_{i > 1} n_{i}\right)
$$


## Ejemplo

# levenshtein

## Ejemplo

| Variable | Descripción | Valor |
|-----------|--------------|--------|
| `str1` | Cadena 1 | `"tab"` |
| `str2` | Cadena 2 | `"tabe"` |
| `m` | Longitud de `str1` | 3 |
| `n` | Longitud de `str2` | 4 |
| `dp` | Matriz (m+1) × (n+1) | 4 × 5 |

---

## 3️⃣ Estructura base de la matriz `dp`


| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 | 0 |

---

## 4️⃣ Inicialización de la primera fila y columna

- Si `i == 0` → `dp[0][j] = j` (se necesitan `j` inserciones para formar la subcadena de `str2`)
- Si `j == 0` → `dp[i][0] = i` (se necesitan `i` eliminaciones para vaciar `str1`)

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 | 4 |
| 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 0 | 0 | 0 | 0 |
| 3 | 3 | 0 | 0 | 0 | 0 |

---

##  Relleno de la matriz paso a paso

###  Comparamos los caracteres

| Índice | `str1[i-1]` | `str2[j-1]` | Acción | Valor resultante |
|--------|---------------|--------------|---------|-------------------|
| i=1, j=1 | 't' = 't' | true | `dp[1][1] = dp[0][0] = 0` |
| i=1, j=2 | 't' ≠ 'a' |  false| `dp[1][2] = 1 + min( dp[0][2]=2, dp[1][1]=0, dp[0][1]=1 ) = 1` |
| i=1, j=3 | 't' ≠ 'b' | false | `dp[1][3] = 1 + min(3, 1, 2) = 2` |
| i=1, j=4 | 't' ≠ 'e' |  false| `dp[1][4] = 1 + min(4, 2, 3) = 3` |

### Matriz parcial

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 | 4 |
| 1 | 1 | 0 | 1 | 2 | 3 |
| 2 | 2 | 0 | 0 | 0 | 0 |
| 3 | 3 | 0 | 0 | 0 | 0 |

---

### Segunda fila (i = 2, carácter `'a'`)

| i=2, j=1 | 'a' ≠ 't' | `dp[2][1] = 1 + min(1,2,1)=1` |
| i=2, j=2 | 'a' = 'a' | true `dp[2][2] = dp[1][1] = 0` |
| i=2, j=3 | 'a' ≠ 'b' | false `dp[2][3] = 1 + min(2,0,1)=1` |
| i=2, j=4 | 'a' ≠ 'e' | false `dp[2][4] = 1 + min(3,1,2)=2` |

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 | 4 |
| 1 | 1 | 0 | 1 | 2 | 3 |
| 2 | 2 | 1 | 0 | 1 | 2 |
| 3 | 3 | 0 | 0 | 0 | 0 |

---

### Tercera fila (i = 3, carácter `'b'`)

| i=3, j=1 | 'b' ≠ 't' | `dp[3][1] = 1 + min(2,3,1)=2` |
| i=3, j=2 | 'b' ≠ 'a' | `dp[3][2] = 1 + min(1,2,0)=1` |
| i=3, j=3 | 'b' = 'b' | true `dp[3][3] = dp[2][2] = 0` |
| i=3, j=4 | 'b' ≠ 'e' | false `dp[3][4] = 1 + min(2,0,1)=1` |

| i/j | 0 | 1 | 2 | 3 | 4 |
|-----|---|---|---|---|---|
| 0 | 0 | 1 | 2 | 3 | 4 |
| 1 | 1 | 0 | 1 | 2 | 3 |
| 2 | 2 | 1 | 0 | 1 | 2 |
| 3 | 3 | 2 | 1 | 0 | 1 |

---

## Tabla terminada

|   | "" | **t** | **a** | **b** | **e** |
|---|---|---|---|---|---|
| **""** | 0 | 1 | 2 | 3 | 4 |
| **t** | 1 | 0 | 1 | 2 | 3 |
| **a** | 2 | 1 | 0 | 1 | 2 |
| **b** | 3 | 2 | 1 | 0 | 1 |

---




