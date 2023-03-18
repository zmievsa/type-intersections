# type-intersections

Package description

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

## Current issues

### Ordering checks

The current implementation assumes that intersections are unordered which makes some sense for two reasons:

1. I have not been able to come up with an algorithm that can intuitively do structural and ordered intersection issubclass checks at the same time (see the XFAIL testcase). Not sure if that is even possible but I haven't tried for long.
2. TypeScript [doesn't even try](https://www.typescriptlang.org/play?#code/JYOwLgpgTgZghgYwgAgIImAWzgG2QbwChlkBnYALwgC5kQBXTAI2gG5jk4BzGuxlqOwC+hQqEixEKAMJwwyCAA9IIACak0GbHiIkSAdwAWwUgGtoAGQgguYQ7QbM2hEWPDR4SZNPosCHEnIqWlIwKFAudj1kBAB7HFioB35nV3EPKWQAIVwdAJj4xJCwiOFRGHoQBDBgWJBkQwgcBIAKGFjY2nQsXGQAMm85fu9fFAGc5oBKf2iAelnkAEYAOmQAMQ7kE0569KhSCGra+tiYTmbkOygIFDAATwAHCFJVgElliFWAFUbLx+fONc6LF5KoIKp6A8cMAEHJwcgmHADqpkHUtiBGuEwHAqhB8u1YlE9PNkAAmVYAZUoKG2ACIQBAAG7QWn4jrLIIQIkkEkAZlW0kKUC2GnpTJZbNiyziCUELkIQA) to handle order in intersections
