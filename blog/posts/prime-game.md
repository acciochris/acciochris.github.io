---
date: 5 Jan, 2025
tags: rust, programming-language
category: CS
---

# Gambling... and Rust

Happy New Year! In this post I will present a gambling game I designed for AP Stats. And Rust.

## Background

Ok. Let me explain.

Recently, I just finished basic probability theory in AP Stats. One of my assignments was
to design a game of chance [^1] that consistently delivers a profit to the dealer. I also
calculated the expected value and standard deviation of the outcome.

Coincidentally, I have also been learning about the
[Rust programming language](https://www.rust-lang.org/). That's when I came up with an idea:

*Why not simulate my game in Rust?*

And so I did.

## The Game

```{note}
The following description is directly adapted from my assignment for AP Stats.
```

To celebrate the mathematical significance of prime numbers, this game involves choosing your
favorite prime number from a deck of cards!

Given a standard 52-card deck, you are free to randomly select one card from the deck (without
seeing its front side). There are four possible outcomes.

- You selected a prime number (2, 3, 5, or 7): Hooray! You get to *double* your money.
- You selected a composite number (4, 6, 8, 9, or 10): Unfortunately, you *lose* your money.
- You selected 1 (an ace of any color): Although one is neither prime nor composite, it is a special
  number in math. You also get to *double* your money.
- You selected a face card (J, Q, or K):
  - Place your card back into the deck, because now you get to choose your own number!
  - Designate your favorite prime number to be either 2, 3, 5, or 7. You will then choose another
    card from the deck.
    - If the new card has the same prime number, you get paid *5 to 1*.
    - If the new card has any other prime number, you *double* your money.
    - If the new card has composite numbers, aces, or is a face card, you *lose* your money.

|    Outcome     |        Payout        |
| :------------: | :------------------: |
| 2, 3, 5, 7, A  |        1 : 1         |
| 4, 6, 8, 9, 10 |         lose         |
|    J, Q, K     | same prime => 5 : 1  |
|                | other prime => 1 : 1 |
|                |  all other => lose   |

## The Math

Assume that the player pays $10$ dollars for the game.

| Outcome $x$ | Probability $p$  |
| :---------: | :--------------: |
|    $10$     |  $\frac{5}{13}$  |
|    $-10$    |  $\frac{5}{13}$  |
|    $50$     | $\frac{3}{169}$  |
|    $10$     | $\frac{9}{169}$  |
|    $-10$    | $\frac{27}{169}$ |

$$
\begin{align*}
    \mu_x &= \sum_i x_i p_i = -0.178 \\
    \sigma_x &= \sqrt{\sum_i (x_i - \mu_x)^2 p_i} = 11.940 \\
\end{align*}
$$

## The Code

Short. Sweet. Amazingly functional.

```{code-block} rust
:caption: lib.rs
:linenos:

use rand::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Card {
    Ace,
    J,
    Q,
    K,
    Number(u8),
}

#[derive(Debug)]
pub struct Deck {
    deck: Vec<Card>,
}

impl Deck {
    pub fn new() -> Self {
        let mut deck = vec![Card::Ace, Card::J, Card::Q, Card::K];
        for i in 2..=10 {
            deck.push(Card::Number(i));
        }
        Self {
            deck: deck.iter().copied().cycle().take(52).collect(),
        }
    }

    pub fn shuffle(&mut self) {
        let mut rng = thread_rng();
        self.deck.shuffle(&mut rng);
    }

    pub fn choose(&self) -> Card {
        let mut rng = thread_rng();
        *self.deck.choose(&mut rng).unwrap()
    }
}
```

```{code-block} rust
:caption: main.rs
:linenos:

use prime::{Card, Deck};
use rand::prelude::*;

fn simulate(deck: &Deck) -> i64 {
    match deck.choose() {
        Card::Number(2 | 3 | 5 | 7) => 20,
        Card::Number(_) => 0,
        Card::Ace => 20,
        _ => {
            let prime = *[2, 3, 5, 7].choose(&mut thread_rng()).unwrap();
            match deck.choose() {
                Card::Number(x) if x == prime => 60,
                Card::Number(2 | 3 | 5 | 7) => 20,
                _ => 0,
            }
        }
    }
}

fn stats(iter: impl Iterator<Item = i64>) -> (f64, f64) {
    let v = iter.collect::<Vec<_>>();
    let mean = v.iter().sum::<i64>() as f64 / v.len() as f64;
    let mut stdev = v.iter().map(|&x| (x as f64 - mean).powi(2)).sum::<f64>();
    stdev = (stdev / (v.len() - 1) as f64).sqrt();
    (mean, stdev)
}

fn main() {
    let mut deck = Deck::new();
    deck.shuffle();

    let len = 1000000i64;
    // let mean = (0..len).map(|_| simulate(&deck) - 10).sum::<i64>() as f64 / len as f64;
    let (mean, stdev) = stats((0..len).map(|_| simulate(&deck) - 10));

    println!("{mean}, {stdev}");
}
```

## Reflection

IMO, the most exhilarating part is definitely writing the code in Rust. Not only does the program
produce a consistent result with my mathematical calculations:

```
-0.1794, 11.946612840602265
```

but it also demonstrates the unique characteristics of Rust.

Within 80 lines of code, I made use of structs, enums, traits, closures, iterators, and perhaps most
importantly, `match` expressions. While I definitely overcomplicated things a bit (especially with
respect to the iterator soup in `fn stats` :P), the joy of learning a new programming language never
ceases to inspire me.

However,

I did not make use of lifetimes or Rust memory management. I will do that---soon.

[^1]: gambling

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
