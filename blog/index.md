# My personal blog

```{toctree}
:hidden:
Physics notes <https://acciochris.github.io/physics-notes>
Machine learning repo <https://github.com/acciochris/machine-learning>
```

I'm Chang (Chris) Liu from Lynbrook High School in San Jose, California.

## My projects (every card is clickable!)

::::{grid} 1 1 2 2
:::{grid-item-card} Physics
:link: https://acciochris.github.io/physics-notes
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

:::{grid-item-card} Programming & Machine Learning
:link: https://github.com/acciochris/machine-learning
```python
def evaluate(name, y_test, y_pred):
    print(f"Result for {name}:")
    print(f"precision: {precision_score(y_test, y_pred)}")
    print(f"recall: {recall_score(y_test, y_pred)}")
    print(f"f1: {f1_score(y_test, y_pred)}")
    print(f"matthews: {matthews_corrcoef(y_test, y_pred)}")
    plt.close()
    confusion = ConfusionMatrixDisplay.from_predictions(y_test, y_pred)
    confusion.plot()
```
:::
::::

## Contact me

- Github: https://github.com/acciochris
- Kaggle: https://www.kaggle.com/acciochris

## Blog posts

You can find a list of my posts down below or by visiting {ref}`blog-posts`. You can also subscribe
to the atom feed at {ref}`blog-feed`.

```{postlist}
:excerpts:
```
