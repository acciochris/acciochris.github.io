---
date: 9 Dec, 2023
tags: error-correction
category: CS
---

# Reed-Solomon Error Correction --- Encoding

Reed-Solomon codes are an especially powerful tool for efficient multi-bit error detection and
correction. The following is my understanding of the algorithm after reading my professor's
presentation and correcting several erroneous details.

## Galois Field Arithmetic

In Reed-Solomon codes, a *symbol* is defined a sequence of multiple bits. Each symbol will be corrected
as a whole instead of on a bit-by-bit basis. Usually 8 bits are used. However, for the sake of simplicity,
we will use 3 bits in the following section (and 2 for the actual encoding/decoding process).

To manipulate symbols, we will need finite-field arithmetic (since bits are discrete and finite),
in this case Galois Field arithmetic, commonly denoted as $GF[2^m]$, where $m$ is the number of bits.

Let's take a look at $GF[2^3]$.

| $\alpha^i$ |  polynomial   | binary | decimal |
| :--------: | :-----------: | :----: | :-----: |
|    $0$     |      $0$      |  000   |    0    |
| $\alpha^0$ |      $1$      |  001   |    1    |
| $\alpha^1$ |      $x$      |  010   |    2    |
| $\alpha^2$ |     $x^2$     |  100   |    4    |
| $\alpha^3$ |    $x + 1$    |  011   |    3    |
| $\alpha^4$ |   $x^2 + x$   |  110   |    6    |
| $\alpha^5$ | $x^2 + x + 1$ |  111   |    7    |
| $\alpha^6$ |   $x^2 + 1$   |  101   |    5    |

The table shown above has the following properties:

1. $\alpha$ can be considered a dummy variable.
2. The leftmost column contains increasing powers of $\alpha$.
3. These powers correspond to a polynomial of $x$.
4. $0 = 0$, $\alpha^0 = 1$ and $\alpha^1 = x$
5. An irreducible polymonial $p(x) = x^3 + x + 1$ can be used to construct the rest of the table.
   1. $\alpha$ is a root of $p(x)$, i.e. $\alpha^3 + \alpha + 1 = 0$, so is $x$.
   2. Whenever $x^3$ or $\alpha^3$ is encountered, substitute it with $x + 1$

   ```{important}
   **Addition in $GF[2^3]$**

   In $GF[2^3]$, addition is $\text{mod}\;2$ by default. Therefore, simple xor must be used term by term and there are no carries.
   Subtraction is equivalent to addition.

   For example, $x + x = 0$, and $x^2 + x^2 + x + 1 = x + 1$.
   
   In the case of $p(x)$, $x^3 + x + 1 + x + 1 = x + 1 = x^3$
   ```
6. The coefficients of the polynomial are the bits of the symbol.
7. The decimal representations of the binary bits are also shown.

### Mutiplication

Multiplication of symbols in $GF[2^m]$ is done by multiplying the polynomial forms, dividing the
result thereof by the generator polynomial, and taking the remainder.

For example, in $GF[2^2]$, we have the following symbols

| $\alpha^i$ | polynomial | binary | decimal |
| :--------: | :--------: | :----: | :-----: |
|    $0$     |    $0$     |   00   |    0    |
| $\alpha^0$ |    $1$     |   01   |    1    |
| $\alpha^1$ |    $x$     |   10   |    2    |
| $\alpha^2$ |   $x^2$    |   11   |    3    |

with the generator polynomial being $p(x) = x^2 + x + 1$.

Then

$$
\begin{align*}
   2 \times 3 &= x \cdot x^2 \bmod (x^2 + x + 1) \\
              &= x\cdot(x + 1) \bmod (x^2 + x + 1) \\
              &= 1
\end{align*}
$$

The complete multiplication table is as follows:

| multiplier | multiplicand | product |
| :--------: | :----------: | :-----: |
|     0      |      0       |    0    |
|     0      |      1       |    0    |
|     0      |      2       |    0    |
|     0      |      3       |    0    |
|     1      |      1       |    1    |
|     1      |      2       |    1    |
|     1      |      3       |    1    |
|     2      |      2       |    3    |
|     2      |      3       |    1    |
|     3      |      3       |    2    |

```{important}
The division mentioned above is $GF[2^m]$ polynomial division, where ordinary polynomial division is used
with the quirk of $GF$ addition/subtraction.
```

Now we are ready to dive into the code itself.

```{caution}
From now on, we're going to **abandon** the polynomial representation of symbols and use only $\alpha^i$
or its decimal representation. This is to avoid confusion with the representation of the code itself,
which also happens to be a polynomial.
```

## Encoding a Reed-Solomon Code

A complete Reed-solomon Code consists of $n$ $m$-bit symbols where $n \le 2^m - 1$, of which:

- $k$ are data symbols, and
- $2t$ are check symbols, where
- $k + 2t = n$

$t$ is the maximum number of correctable erroneous symbols. In other words, to correct an erroneous
symbol, we need two redundant ones.

When $m = 2$ (this is the case we'll be considering from now on), $k = t = 1$.

### Polynomial Representation of the Message

To encode a string of data, first the data must be separated into $(k \cdot m)$-bit chunks and then divided evenly into $k$ $m$-bit symbols. The message polynomial

$$
M(x) = \sum_{i=0}^{k - 1}M_ix^i
$$

where $M_i$ are symbols in decimal form. (Once again, *please* forget that the symbols used to be polynomials, too).

### The Code Generator Polynomial

To encode the message, we need another magic polynomial, the code generator polynomial:

$$
g(x) = \prod_{p=0}^{2t-1} (x + \alpha^{b + p})
$$

where:

- $\alpha^{b+p}$ should be understood as a decimal number
- $b$ is an arbitrary constant, but is usually set to $0$

### Encoding

The trick is to divide a shifted version of the message polynomial by the code generator polynomial:

$$
(M(x)x^{2t}) \div g(x) = Q(x)\;\cdots\;R(x)
$$

where $Q(x)$ is the quotient and $R(x)$ is the remainder

```{important}
**Arithmetic When Dealing with Messages**

You may have noticed I have been constantly emphasizing the necessity to forget the previous polynomial arithmetic
we did to symbols. This is because we need a very similar but different polynomial arithmetic
system when dealing with messages, where coefficients can be arbitrary decimal integers, instead of only $0$ and $1$.

Addition is still equivalent to subtraction and done with a simple xor. However, instead of doing it term by term,
it is done bit by bit

$$
2 + 3 = (10)_2 + (11)_2 = (01)_2 = 1
$$

Multiplication follows the multiplication table we've derived earlier.

Polynomial division is still done in the normal manner.
```

We can rewrite the equation as

$$
M(x)x^{2t} = Q(x)g(x) + R(x)
$$

Adding $R(x)$ on both sides gives

$$
M(x)x^{2t} + R(x) = Q(x)g(x) + R(x) + R(x) = Q(x)g(x)
$$

The left hand side is the Reed-Solomon code ($T(x)$ for transmitted message):

$$
T(x) = M(x)x^{2t} + R(x)
$$

In reality, $T(x)$ is converted back to its coefficients and sent in binary.

### Example of Encoding

(A quick reminder that $k = t = 1$ in $GF[2^2]$, see the [section](#encoding-a-reed-solomon-code) above)

Since we only have one data symbol in $GF[2^2]$, let's suppose we want to encode the binary message $10$ (decimal $2$).

$$
2(x^2) \div [(x + 1)(x + 2)] = 2\;\cdots\;x + 3
$$

$$
T(x) = 2x^2 + x + 3
$$

Binary message: $100111$

We'll discuss decoding in the next article.

## Citations and Credits

1. Clarke, C. K. P. "R&d white paper." Reed-Solomon error correction," WHP 31 (2002).
2. Shankar, Priti. “Decoding Reed-Solomon Codes Using Euclid’s Algorithm.” Resonance, vol. 12, no. 4, Apr. 2007, pp. 37–51. DOI.org (Crossref), https://doi.org/10.1007/s12045-007-0037-y.

Huge thanks to my professor Mr. Thomas Riordan for making the best out of both papers.

<script src="https://giscus.app/client.js"
        data-repo="acciochris/acciochris.github.io"
        data-repo-id="R_kgDOKDyTVg"
        data-category="Announcements"
        data-category-id="DIC_kwDOKDyTVs4CYZPy"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
