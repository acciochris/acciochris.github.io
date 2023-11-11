---
date: 11 Nov, 2023
tags: robot, scioly, algorithm
category: engineering
---

# How to Make a Robot Car Go in a Straight Line

After messing around with my [micropython-based esp8266 chip](./micropython-server.md), I've finally got
to the point where I can make the robot go in a straight line.

## The Hardware

My robot car is a dual-motored car. This means that unavoidably I'll need to correct the tiny differences
between the two motors so as to make it go in a straight line. To achieve this goal, I bought an MPU9250
motion sensor which can detect its acceleration $\mathbf{a}$, angular velocity $\mathbf{\omega}$ and
the earth's magnetic field $\mathbf{B}$.

## The Original Algorithm

My original algorithm is to increaase the speed of one motor and decrease the speed of the other
when I detect the robot is turning to one direction. As the motors are controlled by the voltages
supplied, when I apply a voltage difference between the two motors, the motors will operate at different
speeds.

The following is a theoretical analysis of my original algorithm.

1. The scalar angular velocity $\omega$ can be determined by projecting the vector onto the gravitational unit vector:
   
   $$
   \omega = \vec{\omega}\cdot\frac{\vec{g}}{|\vec{g}|}
   $$

2. The angular velocity can be approximated as a linear function of $V$, the voltage difference between the two motors I apply:
   
   $$
   \omega(V) = a + bV
   $$

3. The voltage difference is assumed to have a linear relationship with respect to he angle $\theta$ and the angular velocity $\omega$:
   
   $$
   V(\theta, \omega) = p\theta + q\omega
   $$

4. In step 3, $\theta$ is determined by numerically integrating $\omega$:
   
   $$
   \theta = \int_0^t\omega(t)\,dt
   $$

5. Then a differential equation can be set up and solved with separation of variables:
   
   $$
   \begin{align*}
       \dot{\theta} &= a + b(p\theta + q\dot{\theta}) \\
       (1-bq)\frac{d\theta}{dt} &= a + bp\theta \\
       \int_0^\theta\frac{d\theta}{a + bp\theta} &= \int_0^t\frac{1}{1-bq}dt \\
       \frac{1}{bp}\ln\left|\frac{a + bp\theta}{a}\right| &= \frac{1}{1-bq}t \\
       1 + \frac{bq}{a}\theta &= \exp\left(\frac{bp}{1-bq}t\right) \\
       \theta &= \frac{a}{bq}\left(\exp\left(\frac{bp}{1-bq}t\right)-1\right) \\
   \end{align*}
   $$

This implies that my original algorithm should never be able to achieve a perfect straight line.

Nevertheless, I tried it out.

```{note}
The units of $p$ and $q$ were all messed up because I was using degrees and the voltages I used were
not in volts either. I omitted them because they are irrevelant here.
```

| $p$ | $q$ | $\Delta t$ | Result |
| --- | --- | ---------- | ------ |
| 10  | 20  | 0.2        | oscillates |
| 10  | 10  | 0.2        | tilts about 25 degrees |
| 50  | 10  | 0.2        | oscillates |
| 20  | 10  | 0.2        | tilts about 25 degrees |
| 20  | 12  | 0.2        | tilts about 15 degrees |
| 20  | 10  | 0.6        | tilts about 5 degrees |

($\Delta t$ is the period with which I update the voltages)

As you can see, the results are far from satisfactory. Oscillation is not shown in the theoretical
derivation but it was probably a result of latency. Another significant problem was that none of
them works on relatively smooth surfaces. (It oscillates violently)

## The Solution

I eventually solved this problem by using accumulative voltage difference with weight decay.

Instead of using a fixed formula for $V$, I update the value of $V$ with this recursive formula:

$$
V_n = \alpha V_{n-1} + (p\theta + q\omega)
$$

where $\alpha$ is a constant in the interval $(0, 1)$. This way, more recent measurements of $\theta$ and $\omega$
constitute a larger portion of $V$ while older ones constitute a smaller portion.

This not only smooths out the curve for $V$ but also implies that I will be able to reduce $\Delta t$ to a smaller value and thus gain more accurate control.

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
