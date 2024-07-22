---
date: 21 Jul, 2024
tags: tcl, makefile, c, fortran, programming-language, engineering
category: CS
---

# Engineering Montage

Over the past few weeks, I have been working on a technical project that requires a ton of (computer)
engineering. I think it's time to talk about what what I learned from it.

::::{note}
~~Fun~~ Not so fun fact:

You may find the title of this post a bit awkward (lame?). It's probably because I borrowed the word
"montage" from what I've also been working on---writing college essays. Specifically, I have been
attending [College Essay Guy](https://www.collegeessayguy.com/)'s course on how to write the personal
statement and it mentioned "montage" as a possible structure.

:::{important}
I am not in any way affliated with College Essay Guy.
:::

Nevertheless, I believe that the word "montage" captures the essence of this post pretty well, as it
is indeed a, well, montage of many unrelated bits of engineering.
::::

## Tcl

Let's start with what I've [already mentioned](./learn-tcl-1.md) I would be working on.

I previously said that Tcl was a string-based language. ~~I take that back.~~ Actually no, just take
it with a grain of salt. This is because by diving into the internals of Tcl (because of an obscure
error that's related, long story), I discovered that while strings are essential to Tcl, there's a
lot more to it.

Consider the following declaration of a `Tcl_Obj` (taken from Tcl 8.6.14 source code):

```{code-block} c
:linenos:

typedef struct Tcl_Obj {
    int refCount;		/* When 0 the object will be freed. */
    char *bytes;		/* This points to the first byte of the
				 * object's string representation. The array
				 * must be followed by a null byte (i.e., at
				 * offset length) but may also contain
				 * embedded null characters. The array's
				 * storage is allocated by ckalloc. NULL means
				 * the string rep is invalid and must be
				 * regenerated from the internal rep.  Clients
				 * should use Tcl_GetStringFromObj or
				 * Tcl_GetString to get a pointer to the byte
				 * array as a readonly value. */
    int length;			/* The number of bytes at *bytes, not
				 * including the terminating null. */
    const Tcl_ObjType *typePtr;	/* Denotes the object's type. Always
				 * corresponds to the type of the object's
				 * internal rep. NULL indicates the object has
				 * no internal rep (has no type). */
    union {			/* The internal representation: */
	long longValue;		/*   - an long integer value. */
	double doubleValue;	/*   - a double-precision floating value. */
	void *otherValuePtr;	/*   - another, type-specific value,
	                       not used internally any more. */
	Tcl_WideInt wideValue;	/*   - a long long value. */
	struct {		/*   - internal rep as two pointers.
				 *     the main use of which is a bignum's
				 *     tightly packed fields, where the alloc,
				 *     used and signum flags are packed into
				 *     ptr2 with everything else hung off ptr1. */
	    void *ptr1;
	    void *ptr2;
	} twoPtrValue;
	struct {		/*   - internal rep as a pointer and a long,
	                       not used internally any more. */
	    void *ptr;
	    unsigned long value;
	} ptrAndLongRep;
    } internalRep;
} Tcl_Obj;
```

We can see that there's a large `union` at the bottom. This is the internal (alternative)
representation of a Tcl object, as opposed to its string representation: `char *bytes`. In this
case, it can either be a `long`, a `double`, a pointer, a `long long`, two pointers, or a pointer
and a `long`. Phew!

This means that in some corner cases, thinking that every Tcl object is a string can actually
be erroneous. (no example here since I haven't fully understood it myself)

Furthermore, the conversion between the internal representation and strings are problematic and
caused me a ton of trouble. So the fact that Tcl objects have an internal representation isn't
going to change my opinion of Tcl. (-:

## Makefile

I have been interacting with `Makefile`s quite a lot these days. If you want to learn more about
`Makefile`s, [`Makefile` Tutorial](https://makefiletutorial.com/) is definitely one of the best
resources. But here is what I found most useful:

1. Recursive `make`:

   ```makefile
   target:
       cd subdir && $(MAKE)
   ```

2. `:=`, `=` and `?=`

   Basically, `:=` is the normal assignment. `=` evaluates at run time and `?=` only assigns when
   not already present. See [here](https://makefiletutorial.com/#variables-pt-2) for a more detailed
   explanation.

3. `.PHONY`: run even when the file is present

   :::{caution}
   This can sometimes cause the build process to be excessively long, especially if used together
   with dependencies, like this:

   ```makefile
   .PHONY: b
   b:
       <build b>

   .PHONY: a
   a: b
       <build a>
   ```

   `b` will build again if `make a` is invoked, even when `b` is already built previously, for example,
   with a `make b`.

   One possible solution would be to remove the build dependency.
   :::

4. Suppress errors by adding a `-` to the beginning of each command

## Fortran

When some legacy Fortran 77 code needs to be linked to C code, `f2c` is still an option. Just make
sure that you use the latest version since it include important fixes (e.g. building on 64-bit systems).

If you can modify the Fortran code (and have the time to do it), the modern Fortran `bind(c)` is
probably the way to go.

## C

Several random takeaways.

### `long` and `long long` are especially tricky

At least when you're dealing with legacy 32-bit code. Just use the fixed width versions such as `int32_t` or `uint64_t` from `<stdint.h>`.

Also when dealing with pointers, `size_t` and `ptrdiff_t` are really useful (from `<stddef.h>`).

### `printf` format specifiers you've never heard of

You probably need to use the proper `printf` specifier for the aforementioned types. You can find the
full details on [cppreference.com](https://en.cppreference.com/w/c/io/fprintf)

### Compile objects intended for shared libs with `-fPIC`

This is kind of obvious, but nonetheless essential.

### You should never name your symbol after a `libc` symbol

This will cause you a ton of pain during linking. What I did was that I renamed everything to something else.
You could probably make it work with compiler flags, but honestly, I think that way is just too
hacky.

## What's Next

I'm still working on the project. Expect a post on lexer and parser generators and probably something
else as well.

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
