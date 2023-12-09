---
date: 9 Dec, 2023
tags: error-correction
category: CS
---

# Reed-Solomon Error Correction

Reed-Solomon codes are an especially powerful tool for efficient multi-bit error detection and
correction. The following is my understanding of the algorithm after reading my professor's
presentation and correcting several erroneous details.

## Galois Field Arithmetic

In Reed-Solomon codes, a *symbol* is defined a sequence of multiple bits. Each symbol will be corrected
as a whole instead of on a bit-by-bit basis. Usually 8 bits are used. However, for the sake of simplicity,
we will use 3 bits in the following sections.

However, to manipulate symbols, we will need finite-field arithmetic (since bits are discrete and finite),
in this case Galois Field arithmetic, commonly denoted as $GF[2^m]$, where $m$ is the number of bits.

Let's take a look at $GF[2^3]$.

| $\alpha^i$ |    polynomial | binary | decimal |
| ---------- | ------------: | :----: | ------: |
| $0$        |           $0$ |  000   |       0 |
| $\alpha^0$ |           $1$ |  001   |       1 |
| $\alpha^1$ |           $x$ |  010   |       2 |
| $\alpha^2$ |         $x^2$ |  100   |       4 |
| $\alpha^3$ |       $x + 1$ |  011   |       3 |
| $\alpha^4$ |     $x^2 + x$ |  110   |       6 |
| $\alpha^5$ | $x^2 + x + 1$ |  111   |       7 |
| $\alpha^6$ |     $x^2 + 1$ |  101   |       5 |

The table shown above has the following properties:

1. $\alpha$ can be considered a dummy variable. It is useful only during the construction of such a field.
2. The leftmost column contains increasing powers of $\alpha$.
3. These powers correspond to a polynomial of $x$.
4. $0 = 0$, $\alpha^0 = 1$ and $\alpha^1 = x$
5. An irreducible polymonial $p(x) = x^3 + x + 1$ can be used to construct the rest of the table.
   1. $\alpha$ is a root of $p(x)$, i.e. $\alpha^3 + \alpha + 1 = 0$, so is $x$.
   2. Whenever $x^3$ or $\alpha^3$ is encountered, substitute it with $x + 1$

   ```{important}
   **Addition in $GF[2^3]$**

   In $GF[2^3]$, addition is $\text{mod}\;2$ by default. Therefore, simple xor must be used and there are no carries.
   Subtraction is equivalent to addition.

   For example, $x + x = 0$, and $x^2 + x^2 + x + 1 = x + 1$.
   
   In the case of $p(x)$, $x^3 + x + 1 + x + 1 = x + 1 = x^3$
   ```
6. The coefficients of the polynomial are the bits of the symbol.
7. The decimal representations of the binary bits are also shown.

### Mutiplication




## Citations and Credits

1. Clarke, C. K. P. "R&d white paper." Reed-Solomon error correction," WHP 31 (2002).
2. Shankar, Priti. “Decoding Reed-Solomon Codes Using Euclid’s Algorithm.” Resonance, vol. 12, no. 4, Apr. 2007, pp. 37–51. DOI.org (Crossref), https://doi.org/10.1007/s12045-007-0037-y.

Huge thanks to my professor Mr. Thomas Riordan for making the best out of both papers.
