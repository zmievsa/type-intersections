# type-intersections

A naive prototype of type intersections implementation.

---

<p align="center">
<a href="https://github.com/ovsyanka83/type-intersections/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/Ovsyanka83/type-intersections/actions/workflows/test.yaml/badge.svg?branch=main&event=push" alt="Test">
</a>
<a href="https://codecov.io/gh/ovsyanka83/type-intersections" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/ovsyanka83/type-intersections?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/type-intersections/" target="_blank">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/type-intersections?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/type-intersections/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/type-intersections?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Installation

```bash
pip install type-intersections
```

## Intro

Type intersections are a way for a programmer to say that some variable is of type `A` and type `B` at the same time which is only possible if it inherits from `A` and `B` or if `A` and `B` are both structural types with overloaded subclass checks such as `Sized` or `Hashable`.

## Current issues

### Ordering checks

The current implementation assumes that intersections are unordered which makes some sense for two reasons:

1. I have not been able to come up with an algorithm that can intuitively do structural and ordered intersection issubclass checks at the same time (see the XFAIL testcase). Not sure if that is even possible but I haven't tried for long.
2. TypeScript [doesn't even try](https://www.typescriptlang.org/play?#code/JYOwLgpgTgZghgYwgAgIImAWzgG2QbwChlkBnYALwgC5kQBXTAI2gG5jk4BzGuxlqOwC+hQqEixEKAMJwwyCAA9IIACak0GbHiIkSAdwAWwUgGtoAGQgguYQ7QbM2hEWPDR4SZNPosCHEnIqWlIwKFAudj1kBAB7HFioB35nV3EPKWQAIVwdAJj4xJCwiOFRGHoQBDBgWJBkQwgcBIAKGFjY2nQsXGQAMm85fu9fFAGc5oBKf2iAelnkAEYAOmQAMQ7kE0569KhSCGra+tiYTmbkOygIFDAATwAHCFJVgElliFWAFUbLx+fONc6LF5KoIKp6A8cMAEHJwcgmHADqpkHUtiBGuEwHAqhB8u1YlE9PNkAAmVYAZUoKG2ACIQBAAG7QWn4jrLIIQIkkEkAZlW0kKUC2GnpTJZbNiyziCUELkIQA) to handle order in intersections

The issue arises when we try to decide what to use in issubclass checks: the class itself or its `mro()`.

Let's say that a class `C` inherits method `foo()` that is defined in both its parents: `A` and `B`. Let's also say that `C` defines the method `__len__` that its parents do not have. If we have an intersection `A & B & Sized`, what algorithm would we use to check that `C` uses the correct `foo()` and that it is Sized?

```python
class A:
    def foo(self, a):
        print(a)

class B:
    def foo(self, a, b):
        print(a, b)

class C(A, B):
    # Makes C Sized
    def __len__(self):
        return 83
```

1. If we try to just check `issubclass(C, A) and issubclass(C, B) and issubclass(C, Sized)`, then we are omitting order information and cannot definitively tell that `C` will inherit `foo()` from `A`.

2. An alternative would be to go through `C`'s MRO in order: checking that each next item in the MRO is a subclass of each argument in the intersection like so:

```python
def __subclasscheck__(self, cls):
    args = self.__args__

    for type_ in cls.mro():
        while args:
            if issubclass(type_, args[0]):
                args.pop(0)
            else:
                break
    return not args
```

But we quickly realize that the first item in MRO is the class itself which is definitely an instance of `A`, `B`, and `Sized`, thus keeping our check unordered. The naive way to resolve this would be to remove the class itself from its MRO before we start checking:

```python
def __subclasscheck__(self, cls):
    args = self.__args__[1:]

    for type_ in cls.mro():
        while args:
            if issubclass(type_, args[0]):
                args.pop(0)
            else:
                break
    return not args
```

But now `issubclass(C, Intersection[A, B, Sized])` is `False` because `__len__` is defined on `C` which we skip in the MRO checks.

Another option would be to use both algorithms: unordered algorithm for structural checks and ordered algorithm for inheritance-based checks. But we cannot distinguish between the checks because classes can have their `__subclasscheck__` redefined in all sorts of complex ways and because even some structural checks care about order: such as in the example I gave above from TypeScript.

In other words, we can't check that some class `C` inherits from classes `A` and `B` in this specific order (i.e. not from `B` and `A`) **and** check that it implements `Sized` at the same time. The only solution I see is to abandon either structural checks or order in inheritance checks. Order seems a lot less necessary and fundamental so I decided to abandon it for now for my naive implementation.
