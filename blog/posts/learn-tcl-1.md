---
date: 7 Jun, 2024
tags: tcl, programming-language
category: CS
---

# First Thoughts on Tcl

About a week ago, I have started learning the [Tcl programming language](https://www.tcl-lang.org/)
for an upcoming project. Here are my first thoughts on it.

## Tcl is just like a shell

The first thing I noticed about Tcl is its similarity to shells such as bash, zsh and fish.

Consider the following rather convoluted way to implement "Hello, World!" in Tcl:

```tcl
set thing "World"
puts "Hello, $thing!"
```

The variable `thing` is referred to as `$thing`, which is identical to the syntax of bash and many
other shells.

What makes Tcl even more similiar to a shell is that its options can be passed to procedures via dashes (`-`).
For example, this is the way to tell Tcl not to output a newline after printing "Hello, World!":

```tcl
puts -nonewline "Hello, World!"
```

## The difference between names and values

After experimenting with the language for a while, I discovered that many of the errors I made are
due to not properly differentiating between names and values in Tcl. In fact, I consider it a
fundamental property of Tcl since this concept is crucial to the implementation and understanding
of many other features that are present in the language.

Let us take another look at the "Hello, World!" example:

```tcl
set thing "World"
puts "Hello, $thing!"
```

Here `thing` is *name* of the variable, while `$thing` refers to the *value* the variable is holding.
This discrepancy is already quite different from other programming languages:

Python:

```python
thing = "World"
print(f"Hello, {thing}!")
```

Rust:

```rust
let thing = "World";
println!("Hello, {thing}!");
```

where both the name and the value are referred to without the `$`.

While the distinction between names and values in Tcl might seem simple at this stage, it quickly becomes
much more confusing and error-prone.

For example, this is how to access the first element of a list in Tcl:

```tcl
lindex $listVar 0
```

but this is how to append an element to the end of the list:

```tcl
lappend listVar "string"
```

Note how `listVar` is referred to differently in the two examples. While this difference does make
intuitive sense (indexing only requires the value, but appending requires the modification of the variable
itself), in practice, it is not at all difficult to put the `$` in the wrong place.

Want a even more confusing example? Here is how to pass by reference in Tcl:

```{code-block} tcl
:linenos:

proc square {var} {
    upvar $var inner
    set inner [expr {$inner ** 2}]
}

set x 2
square x
puts $x ;# 4
```

In line 7, the string `"x"` is passed as the *value* of the argument `var` to the procedure `square`.
Then, in line 2, the `upvar` command, when given the string `"x"` (from `$var`) and another string `"inner"`,
links the local variable *named* `inner` to the variable *named* `"x"` in the outer scope, which in
this case has *value* 2. Then `$inner` is squared and assigned to `inner`, which in turn is an alias of `x`.

## Everything is a string

While data structures such as lists and dictionaries do exist in Tcl, everything is still represented as a string.
For example, the following two commands have the same effect:

```tcl
set x "1 2 3"
# and
set x [list 1 2 3]
```

You can even do:

```tcl
lindex "1 2 3" 0 ;# 1
```

This feature is, in fact, what makes Tcl so powerful, but at the the same time both error-prone and inefficient.

## The verdict

I have only learned Tcl for about a week, so my views on Tcl may change over time. But if you want
to hear right now my verdict of whether it is a good programming language, here it is:

Tcl is a very powerful scripting language. It is more structured than shells, but less so than other
scripting languages such as Python or Javascript. As a result, it is somewhat lacking in both the
simplicity of the former and the well-defined semantics of the latter. I would not recommend
learning this language unless there is a practical use of it (such as modifying existing codebases).


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
