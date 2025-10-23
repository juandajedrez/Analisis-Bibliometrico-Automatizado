# Jaccad distance
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

## Formula matemática

$$
O\left(2^{n_{1}} \sum_{i > 1} n_{i}\right)
$$


## Ejemplo
X=stringOne="tab"
Y=stringTwo="tabe"

lengthStringOne=4
lengthStringTwo:=5

|0|0|0|0|0|
|-|-|-|-|-|
|0|1|1|1|1|
|-|-|-|-|-|
|0|1|2|2|2|
|-|-|-|-|-|
|0|1|2|3|3|


# levenshtein

## Ejemplo
X=stringOne="tab"
Y=stringTwo="tabe"





| 0|  |
|--|--|




