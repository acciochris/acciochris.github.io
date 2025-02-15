---
date: Feb 15, 2025
tags: rust, programming-language, tetris
category: CS
---

# Good Ol' Tetris Now in Rust!

As promised, more about Rust! A couple years ago, I implemented the
[classic Tetris game](https://github.com/acciochris/Tetris) in Python. This time, I decided to
reimplement it in Rust---and in the terminal!

## Demo

<script src="https://asciinema.org/a/703611.js" id="asciicast-703611" async="true"></script>

## How to play

The entire game is open-source and available [here](https://github.com/acciochris/tetris-rust)
on Github. Installation instructions are in the README, but if you're on Linux or MacOS, it is as
simple as (if you're on Windows, don't worry, it is also supported):

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/acciochris/tetris-rust/releases/download/v0.1.0/tetris-rust-installer.sh | sh
```

The script will prompt you to make sure that the binary is on your `PATH`. Once it is, you can start
the game with:

```bash
tetris-rust
```

## Owned and borrowed data

In this post I will briefly explain the first and most important takeaway from writing the code in
Rust. I will expand on this section in upcoming posts.

In the game, any individual block (or [tetromino](https://en.wikipedia.org/wiki/Tetromino), if you
prefer the technical term) is implemented with the following `struct`:

```rust
#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Block {
    coords: Vec<(i32, i32)>,
}

impl Block {
    /// Constructs a new block from slice.
    pub fn new(coords: &[(i32, i32)]) -> Self {
        Self {
            coords: coords.to_owned(),
        }
    }

    /// Returns a new block translated from the current by (dx, dy).
    pub fn translate(&self, dx: i32, dy: i32) -> Self {
        Self {
            coords: self.coords.iter().map(|(x, y)| (x + dx, y + dy)).collect(),
        }
    }

    // more methods omitted
}
```

Notice how the constructor `new()` receives data from the slice `coords` and then calls `.to_owned()`
on it to create a `Vec<(i32, i32)>`. The `.to_owned()` method comes from the
[`ToOwned`](https://doc.rust-lang.org/stable/std/borrow/trait.ToOwned.html) trait in the Rust standard
library and a blanket implementation exists for the slice `[T]`:

```rust
impl<T: Clone> ToOwned for [T] {
    type Owned = Vec<T>;
    fn to_owned(&self) -> Vec<T> {
        self.to_vec()
    }

    // more methods omitted
}
```

While I could have called `.to_vec()` instead on the slice, calling `.to_owned()` highlights the
design decision I made when implementing `Block`. It *owns* the coordinates. The opposite decision
would be to declare `Block` like this:

```rust
pub struct Block<'a> {
    coords: &'a [(i32, i32)]
}
```

The `'a` lifetime indicates that the `Block` is borrowing data from another data source, which in this
case is usually static data from literals. I chose not to use this pattern because of another
design decision I made. I implemented `.translate()` with the following signature:

```rust
pub fn translate(&self, dx: i32, dy: i32) -> Self;
```

Notice that the receiver is the borrowed type `&self` while the return type is `Self`, or more
explicitly `Block`. In other words, when I `.translate()` a `Block`, the current `Block` is
untouched. Instead, a new `Block` is allocated and returned.

This pattern does not require `Block`s to be mutable and simplifies the implementation of the actual
Tetris board. It also mandates that I not use the borrowed alternative, in which case I would have
been forced to write this method:

```rust
impl<'a> Block<'a> {
    pub fn translate(&self, dx: i32, dy: i32) -> Block<'b>;
}
```

The return value borrows data with another lifetime `'b`, which I could not have obtained without
allocating memory inside the function and then leaking the `Vec`. This defeats the purpose of
automatic memory management in Rust.

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
