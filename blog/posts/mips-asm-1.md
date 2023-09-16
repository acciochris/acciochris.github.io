---
date: 16 Sep, 2023
tags: MIPS, assembly, calling-convention
category: CS
---

# MIPS Assembly Part 1: Stacks and Subroutines

Having recently registered for a *Computer Architechture & Organization* course, I decided to take
some time to start writing MIPS assembly code. However, no sooner had I started writing my first
program than I encountered an obstacle: how to properly manipulate the stack and call subroutines.

## Subroutines

A subroutine is a self-contained block of code that can be reused by other pieces of code. Other
code communicates with the subroutine by passing in arguments and receiving return values.

For example, the following MIPS assembly defines a subroutine that adds 3 numbers:

```mips
add3:
  add $t0, $a0, $a1
  add $v0, $t0, $a2
  jr $ra
```

The variables starting with a `$` sign refer to registers, which are the simplest and the most important
place to store data in computers.

Registers that start with an `a` are argument registers and those that start with a `v` are value registers,
argument and value registers constitute the [calling convention](https://en.wikipedia.org/wiki/Calling_convention)
of MIPS.

## The stack

A stack is a last-in-first-out queue. In computer architecture, the stack is a section of the memory
that grows and shrinks as subroutines are called.

Subroutines store data that does not fit into the registers on the stack. They also save saved registers
for the caller (see below). Their data is discarded once they return.

## My program: fibonacci numbers

This is the final, working version of the program I wrote to calculate fibonacci numbers. You can
find the full version on [Github](https://github.com/acciochris/cs10/blob/main/assembly/fib.s).

```{code-block} mips
:linenos:
# $a0: x
# $v0: fib(x)
fib_recursive:
  addi $sp, $sp, -12
  sw $ra, 0($sp)
  sw $s1, 4($sp)
  sw $s0, 8($sp)

  move $s1, $a0
  slti $t0, $s1, 2
  beq $t0, $zero, fib_recursive_else

  # fib(x) = x where x < 2
  move $s0, $s1
  j fib_recursive_ret

  fib_recursive_else:
  # fib(x - 1)
  addi $a0, $s1, -1
  jal fib_recursive
  move $s0, $v0

  # fib(x - 2)
  addi $a0, $s1, -2
  jal fib_recursive
  add $s0, $s0, $v0

  fib_recursive_ret:
  # debug
  move $a0, $s0
  move $a1, $s1
  jal debug

  # return value
  add $v0, $zero, $s0

  lw $s0, 8($sp)
  lw $s1, 4($sp)
  lw $ra, 0($sp)
  addi $sp, $sp, 12
  jr $ra
```

In the beginning (line 4-7), we push data onto the stack by decreasing the stack pointer `$sp` and then
storing the registers we want to save with the `sw` instruction.

```{caution}
The stack grows downward, from large memory addresses to smaller ones. So be careful to **subtract** `$sp`
and put a **positive** offset on `$sp` when pushing the stack. This is also where I made a mistake and
spent tons of time debugging.
```

Of the three registers we pushed on to the stack, `$ra` is the special one, the return address register.
In MIPS, whenever it is needed to call a subroutine, `$ra` must be saved in the caller and loaded
again before returning. This ensures jumping to the correct address when the routine returns.

After that, we follow the basic algorithm to calculate fibonacci numbers. Equivalent C code:

```c
int fib(int x) {
  if (x < 2) {
    return x;
  }
  return fib(x - 1) + fib(x - 2);
}
```

At the end of the routine, we must reload the saved data from the stack back into registers (line 37-40).

## Conclusion

Subroutines are a crucial part of software design, and so are stacks. When writing assembly, we have to
manually manipulate the stack so as to make sure the entire program runs properly as a whole.

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
