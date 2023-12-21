---
date: 20 Dec, 2023
tags: error-correction
category: CS
---

# Reed-Solomon Error Correction --- Decoding

Reed-Solomon codes are an especially powerful tool for efficient multi-bit error detection and
correction. In my last [post](./reed-solomon.md), I discussed how to encode messages. In this post,
I will discuss how to correct errors and decode the message.

## Syndromes

Now that we have protected our message with redundant symbols, let us assume that the message we actually
received is $U(x)$ such that

$$
U(x) = T(x) + E(x)
$$

$E(x)$ is called the error polynomial, since it is the difference between the received and the transmitted message.

The $i$-th syndrome $S_i(x)$ is defined by

$$
S_i(x) = U(x) \bmod (x + \alpha^i)
$$

```{important}
Note that $S_i$ is actually a constant since we are taking the remainder when dividing by $(x + \alpha^i)$,
and since the order of the remainder must be less than that of the divisor.
```

Alternatively, we can rewrite the equation as

$$
U(x) = V_i(x)(x + \alpha^i) + S_i(x)
$$

where $V_i(x)$ are the quotients.

If we rearrange and plug in $\alpha_i$, we will get

$$
\begin{align*}
    S_i(x) &= U(x) + V_i(x)(x + \alpha^i) \\
    S_i(\alpha^i) &= U(\alpha^i) + V_i(\alpha^i)(\alpha^i + \alpha^i) \\
                  &= U(\alpha^i)
\end{align*}
$$

As $S_i(x)$ is a constant function, $S_i(x) = S_i(\alpha^i)$. Thus

$$
S_i = U(\alpha^i)
$$

```{note}
We have dropped the $(x)$ of $S_i(x)$, since $S_i$ is a constant.
```

Example:

This is our transmitted message in my last blog post:

$$
T(x) = 2x^2 + x + 3
$$

Let us assume that during transmission, the second symbol (the first check symbol) got entirely flipped: $(01)_2 \rarr (10)_2$.

$$
U(x) = 2x^2 + 2x + 3
$$

Then

$$
\begin{align*}
    S_0 &= U(x) \bmod (x + 1) = 3 \\
    S_1 &= U(x) \bmod (x + 2) = 1 \\
\end{align*}
$$

Alternatively,

$$
\begin{align*}
    S_0 &= U(1) = 3 \\
    S_1 &= U(2) = 1 \\
\end{align*}
$$

## The Fundamental Equation

You may have wondered why we would like to calculate the syndromes in the first place. Syndromes are
the stepping stones to locating and correcting errors.

$$
\begin{align*}
    S_i = U(\alpha^i) &= T(\alpha^i) + E(\alpha^i) \\
                      &= Q(\alpha^i)g(\alpha^i) + E(\alpha^i) \\
                      &= E(\alpha^i) \\
\end{align*}
$$

```{note}
The last equality is true because $x + \alpha^i$ is a factor of $g(x)$. Thus $g(\alpha^i) = 0$.
```

With the equation above in hand, the next step is to determine $E(x)$ from the syndromes.

```{warning}
The following sections contain complex mathematical manipulation.
```

As at most $t$ errors can be corrected, let

$$
E(x) = \sum_{j=1}^t Y_j x^{e_j}
$$

Therefore

$$
\begin{align*}
    S_i = E(\alpha^i) &= \sum_{j=1}^t Y_j \alpha^{ie_j} \\
                      &= \sum_{j=1}^t Y_j X_j^i \\
\end{align*}
$$

where $X_j = \alpha^{e_j}$.

```{note}
We have omitted proving the fact that properties of exponents apply to $\alpha$.
```

```{caution}
$j \in [1, t]\cap\mathbb{Z}$, but $e_j \in [0, n-1]\cap\mathbb{Z}$.
```

Consider the geometric series

$$
\sum_{k=0}^\infty X_j^kx^k = \frac{1}{1 - X_jx}
$$

After a series of manipulations:

$$
\begin{align*}
    Y_j\sum_{k=0}^\infty X_j^k x^k &= \frac{Y_j}{1 - X_jx} \\
    \sum_{j=1}^t \left(Y_j\sum_{k=0}^\infty X_j^k x^k\right) &= \sum_{j=1}^t\frac{Y_j}{1 - X_jx} \\
    \sum_{k=0}^\infty \left(x^k\sum_{j=1}^t Y_jX_j^k\right) &= \sum_{j=1}^t\frac{Y_j}{1 - X_jx} \\
    \sum_{k=0}^\infty S_kx^k &= \frac{\sum_{j=1}^t \left(Y_j\prod_{k=1,\,k \ne j}^t (1 - X_kx)\right)}{\prod_{j=1}^t(1 - X_jx)}
\end{align*}
$$

We can define the *locator polynomial* $\Delta(x)$ as

$$
\Delta(x) = \prod_{j=1}^t(1 - X_jx)
$$

and the *evaluator polynomial* $\Omega(x)$ as

$$
\Omega(x) = \sum_{j=1}^t \left(Y_j\prod_{\substack{k=1 \\ k \ne j}}^t (1 - X_kx)\right)
$$

Then

$$
\sum_{k=0}^\infty S_kx^k = \frac{\Omega(x)}{\Delta(x)}
$$

As $S_k$ doesn't reallly exist when $k\rarr\infty$, we can rewrite it in modulo form:

$$
\sum_{k=0}^{2t-1} S_kx^k \equiv \frac{\Omega(x)}{\Delta(x)}\pmod{x^{2t}}
$$

This is the Fundamental Equation.

## Locating and Detecting Errors

Up to this point, we still have little clue why we need the Fundamental Equation or the nasty-looking
locator and evaluator polynomials.

However, this is just about to change.

The following is the derivative of the locator polynomial $\Delta(x)$:

$$
\begin{align*}
    \Delta'(x) &= \sum_{j=1}^t \left(\frac{d}{dx}(1 - X_jx)\cdot\prod_{\substack{k=1 \\ k \ne j}}^t (1 - X_kx)\right) \\
               &= \sum_{j=1}^t \left(-X_j\prod_{\substack{k=1 \\ k \ne j}}^t (1 - X_kx)\right)
\end{align*}
$$

This is surprisingly similar to $\Omega(x)$. In fact, we have the following equation:

$$
X_l\frac{\Omega(X_l^{-1})}{\Delta(X_l^{-1})} = -Y_l = Y_l
$$

And here we go. If we can find $\Omega(x)$ and $\Delta(x)$, then all we have to do is:

1. For every $i \in [0, n-1]\cap\mathbb{Z}$, find $\alpha^i$ and its multiplicative inverse $\alpha^{-i}$ (with the multiplication table)
2. Plug $\alpha^{-i}$ into the *locator* polynomial $\Delta(x)$. If $i$ is indeed one of $e_j$, call it $e_l$, then $\Delta(\alpha^{-i}) = \Delta(X_l^{-1}) = 0$. (since $(1 - X_lx)$ is one of the factors of $\Delta(x)$)
3. For every $i$ that passed step 2, evaluate $X_l\frac{\Omega(X_l^{-1})}{\Delta(X_l^{-1})}$ to get the error at that position
 
## Citations and Credits

1. Clarke, C. K. P. "R&d white paper." Reed-Solomon error correction," WHP 31 (2002).
2. Shankar, Priti. “Decoding Reed-Solomon Codes Using Euclid’s Algorithm.” Resonance, vol. 12, no. 4, Apr. 2007, pp. 37–51. DOI.org (Crossref), https://doi.org/10.1007/s12045-007-0037-y.

Huge thanks to my professor Mr. Thomas Riordan for making the best out of both papers.
