from collections.abc import Hashable, Sized
from operator import getitem

import pytest

from type_intersections import Intersection

# Problem is: we can't compare it directly to TypeScript's intersection type
# because TypeScript doesn't support multiple inheritance. Hence we need to
# come up with out own semantics :)


class A:
    pass


class B:
    pass


class C(A, B):
    pass


@pytest.mark.xfail(reason="This test cannot possibly pass. I can't find an implementation that satisfies it")
def test_inheritance_and_structural_checking():
    class E(A, B):
        def __len__(self) -> int:
            return 42

    # Check that both inheritance-based intersection works and abc-based intersection works
    assert issubclass(E, Intersection[A, B, Sized])

    # Check that intersection subclass checks are ordered
    assert not issubclass(E, Intersection[B, A, Sized])

    # Therefore Intersections cannot support both inheritance checks and structural checks.
    # Is this the reason why TypeScript doesn't support order in Intersections?


def test_order_in_inheritance():
    assert issubclass(C, Intersection[B, A])


def test_abcs():
    class D:
        def __hash__(self) -> int:
            return 83

        def __len__(self) -> int:
            return 42

    assert issubclass(D, Intersection[Hashable, Sized])


def test_basic_inheritance():
    assert issubclass(C, Intersection[A, B])
    assert not issubclass(A, Intersection[A, B])
    assert not issubclass(B, Intersection[A, B])

    assert hash(Intersection[A, B]) == hash(Intersection[A, B])
    assert hash(Intersection[A, B]) != hash(Intersection[B, A])
    assert Intersection[A, B] == Intersection[A, B]
    assert Intersection[A, B] == Intersection[B, A]

    assert str(Intersection[A, B]) == f"typing.Intersection[{A.__module__}.{A.__name__}, {B.__module__}.{B.__name__}]"


def test_no_types():
    with pytest.raises(TypeError, match="Cannot take an Intersection of no types."):
        Intersection[()]


def test_list_type():
    assert Intersection[int] is int


def test_inner_intersections():
    assert Intersection[int, Intersection[str, A]].__args__ == (int, str, A)


def test_copy_with():
    assert Intersection[int, str].copy_with((bytes, list)).__args__ == (bytes, list)


def test_isinstance():
    assert isinstance(C(), Intersection[A, B])


def test_reduce():
    assert Intersection[A, B].__reduce__() == (getitem, (Intersection, (A, B)))
