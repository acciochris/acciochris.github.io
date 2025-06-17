---
date: 11 Nov, 2023
tags: MIPS, processor
category: CS
---

# Building a MIPS Processor from Scratch

Chapter 4 of *Computer Organization and Design* explains how a computer can be build from scratch,
using logic gates. Let's take a look.

## Combinational and State Elements

There are two types of elements we use when designing a classical computer, combinational and state.
Combinational elements operate on data, while state elements, as the name suggests, contain state.

For example, a simple AND gate is a combinational element:

![AND gate](../images/mips-asm-2/and.svg)

While a set-reset latch is a state element:

![set-reset latch](../images/mips-asm-2/set-reset-latch.svg)

For a set-reset latch, when we assert the set signal (S) and deassert the reset signal (R), Q is asserted
and vice versa. A more complex version that incorporates the clock signal is the D flip-flop:

![D flip-flop](../images/mips-asm-2/D-flip-flop.svg)

With combinational and state elements, we can build a finite state machine, which is basically what computers
are.

## Pipelining


