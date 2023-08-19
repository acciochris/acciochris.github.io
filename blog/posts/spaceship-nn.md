---
date: 19 Aug, 2023
tags: neural-network, kaggle
category: machine-learning
---

# Titanic Resurrected

Recently, I have been playing around with a competition on Kaggle named [Spaceship Titanic](https://www.kaggle.com/competitions/spaceship-titanic).

So far, I have tried 3 different models:

1. ensemble of
   - logistic regression
   - random forest
   - k nearest neighbors
2. xgboost
3. neural networks

But what's exciting about it is that the third model (neural networks) turned out to be a pretty
impressive solution! I got an accuracy of 0.80851, which is (as of today) within the top 200 on the
leaderboard.

In fact, the model is pretty basic:

- 3 hidden layers
- cross entropy loss
- adam optimizer
- dropout
- l1/l2 ElasticNet regularization

Nevertheless, its stupidly good performance made me realize how good neural networks are at solving
these kinds of classification problems. And I didn't even need a GPU to train my model!

From an engineering perspective, I have two other things to talk about.

The first thing is that I have tried out [Weights and Biases](https://wandb.ai), which just like
Tensorboard, helps you keep track of ML experiments. The visualization is pretty great! But the loading
time is a bit too long. (perhaps too much javascript?)

The second is [Pytorch Lightning](https://lightning.ai). Indeed, I must admit that lightning did help me
reduce my engineering workload, but the API design is still a bit unsatisfactory, at least in my opinion.
Various methods are bunched together in a class, which makes it really messy. Anyway, I'm going to try
out [Pytorch Ignite](https://pytorch-ignite.ai) and see which one is better.

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
