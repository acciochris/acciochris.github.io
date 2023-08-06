# My personal blog

```{toctree}
:hidden:
Physics notes <https://acciochris.github.io/physics-notes>
Machine learning repo <https://github.com/acciochris/machine-learning>
```

I'm Chang (Chris) Liu from Lynbrook High School in San Jose, California.

Here are some of my interests (or projects I have made):

::::{card-carousel} 1
:::{card} Physics
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
:::

:::{card} Computer Programming
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
:::

:::{card} Physics Notes
:link: https://acciochris.github.io/physics-notes
Click to see my personal physics notes!

Topics include:

- Mechanics: $\mathbf{F} = \dfrac{d\mathbf{p}}{dt}$
- Electromagnetism: $\mathcal{E} = -\dfrac{d\Phi}{dt}$
- Thermodynamics: $pV^\gamma = \text{const.}$
:::

:::{card} Machine Learning
:link: https://github.com/acciochris/machine-learning

Click to visit my machine learning Github repo!

```python
preprocessor = Pipeline(
    [
        ("imputer", imputer),
        ("encoder", encoder),
        ("scaler", scaler),
    ],
    verbose=True,
)
```
:::
::::

Contact me:

- Github: https://github.com/acciochris
- Kaggle: https://www.kaggle.com/acciochris

You can find a list of my posts down below or by visiting {ref}`blog-posts`.

```{postlist}
:excerpts:
```
