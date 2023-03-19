import importlib.metadata
from typing import Any, _GenericAlias, _NotIterable, _SpecialForm, _type_check

__version__ = importlib.metadata.version("type_intersections")


@_SpecialForm
def Intersection(self, parameters):
    if parameters == ():
        raise TypeError("Cannot take an Intersection of no types.")
    if not isinstance(parameters, tuple):
        parameters = (parameters,)
    msg = "Intersection[arg, ...]: each arg must be a type."
    # Skip all Any because we assume that Intersection[T & Any] == T
    parameters = tuple(_type_check(p, msg) for p in parameters if p is not Any)
    parameters = _remove_dups_and_flatten_for_intersections(parameters)
    if len(parameters) == 1:
        return parameters[0]
    return _IntersectionGenericAlias(self, parameters)


# You might notice that I do not merge parents and children (i.e. date & datetime != datetime).
# I do so because it makes the initial implementation simpler and because TypeScript doesn't merge
# them too.
def _remove_dups_and_flatten_for_intersections(parameters):
    parameters = _flatten(parameters)
    # Remove duplicates while preserving order
    return tuple(dict.fromkeys(parameters))


def _flatten(parameters):
    params = []
    for p in parameters:
        if isinstance(p, _IntersectionGenericAlias):
            params.extend(p.__args__)
        else:
            params.append(p)

    return params


# Note that we do not check whether a consistent method ordering is possible at runtime
# so it is possible to create impossible intersections.
class _IntersectionGenericAlias(_NotIterable, _GenericAlias, _root=True):
    def copy_with(self, params):
        return Intersection[params]

    def __eq__(self, other):
        if not isinstance(other, _IntersectionGenericAlias):
            return NotImplemented
        return set(self.__args__) == set(other.__args__)

    def __hash__(self):
        return hash(self.__args__)

    def __reduce__(self):
        func, (origin, args) = super().__reduce__()
        return func, (Intersection, args)

    def __instancecheck__(self, obj):
        return self.__subclasscheck__(type(obj))

    # Quite a naive implementation that works for structural checks
    # but cannot perform order checks (i.e. Intersection[A, B] == Intersection[B, A])
    def __subclasscheck__(self, cls):
        return all(issubclass(cls, arg) for arg in self.__args__)
