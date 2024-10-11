---
date: 11 Oct, 2024
tags: java, programming-language
category: CS
---

# Java Data Types

I am studying the Java programming language in AP CS A. Here are a few quirks I noticed about data
types in the language.

## Primitives vs. objects

Java is an object-oriented programming language. It forces you to write `class`es. There are no
such things as standalone functions or variables. Ironically, not everything is an "object" in Java.

```java
int i = 0;
short s = (short)42;
byte b = (byte)25;
long l = 2412346987L;
double d = 3.1415926;
float f = 3.14f;
boolean b = true;
char c = 'a';
```

The code above gives examples of values that are not objects. These values are called "primitives",
which means that sadly, there are no methods available for these objects. While one may argue that
methods are seldom used on integers, booleans, and floating point numbers, sometimes they do come
in handy. Here is an example in Python to check for an alphabetic character:

```python
"A".isalpha()
```

As opposed to the equivalent code in Java:

```java
Character.isLetter('A');
```

The Java version is just more typing. In fact, in order to use methods on those primitives, Java
created "wrapper" classes for each of the primitives, which is very confusing to me. In addition
to `Character`, there are `Double`, `Integer`, etc.

## Converting data types

Notice how I created a `short` above in Java with the following statement:

```java
short s = (short)42;
```

The reason why I did this is that Java only allows implicit type conversion from smaller data types
to larger data types. `42` is an `int` (32 bits) while `short` only holds 16 bits, so we must cast
explicitly.

:::{note}
There is no such issue with Java objects. Variable holding objects are actually holding references
to them, which are all of the same size.
:::

## Conclusion

This is all I have for today. Next time I'm going to talk more about `String`s in Java.

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
