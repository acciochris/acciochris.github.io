# My personal blog

```{toctree}
:hidden:
Github <https://github.com/acciochris>
My physics notes <https://acciochris.github.io/physics-notes>
```

I'm Chang (Chris) Liu from Lynbrook High School in San Jose, California. ([Github](https://github.com/acciochris))

I'm interested mainly in physics:

$$
\newcommand{\V}[1]{\mathbf{#1}}
\newcommand{\pop}[2]{\frac{\partial #1}{\partial #2}}
\begin{align*}
    \nabla\cdot\V{E} &= \frac{\rho}{\epsilon_0} \\
    \nabla\times\V{E} &= -\pop{\V{B}}{t} \\
    \nabla\cdot\V{B} &= 0 \\
    \nabla\times\V{B} &= \mu_0\V{J} + \mu_0\epsilon_0\pop{\V{E}}{t}
\end{align*}
$$

and computer programming (Python and Rust):

```python
def fib(n: int) -> int:
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)
```

```rust
fn main() {
    println!("Hello, world!");
}
```

You can find my posts down below or by visiting {ref}`blog-posts`.

```{postlist}
:excerpts:
```
