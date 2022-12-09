# The utility function are implemented here
# https://github.com/mcpower/adventofcode/blob/master/2021/23/utils.py
import typing
import heapq

T = typing.TypeVar("T")


def dijkstra(
        from_node: T,
        expand: typing.Callable[[T], typing.Iterable[typing.Tuple[int, T]]],
        to_node: typing.Optional[T] = None,
        heuristic: typing.Optional[typing.Callable[[T], int]] = None,
) -> typing.Tuple[typing.Dict[T, int], typing.Dict[T, T]]:
    """
    expand should return an iterable of (dist, successor node) tuples.
    Returns (distances, parents).
    Use path_from_parents(parents, node) to get a path.
    """
    if heuristic is None:
        heuristic = lambda _: 0
    seen = set()  # type: typing.Set[T]
    g_values = {from_node: 0}  # type: typing.Dict[T, int]
    parents = {}  # type: typing.Dict[T, T]

    # (f, g, n)
    todo = [(0 + heuristic(from_node), 0, from_node)]  # type: typing.List[typing.Tuple[int, int, T]]

    while todo:
        f, g, node = heapq.heappop(todo)

        assert node in g_values
        assert g_values[node] <= g

        if node in seen:
            continue

        assert g_values[node] == g
        if to_node is not None and node == to_node:
            break
        seen.add(node)

        for cost, new_node in expand(node):
            new_g = g + cost
            if new_node not in g_values or new_g < g_values[new_node]:
                parents[new_node] = node
                g_values[new_node] = new_g
                heapq.heappush(todo, (new_g + heuristic(new_node), new_g, new_node))

    return g_values, parents


def path_from_parents(parents: typing.Dict[T, T], end: T) -> typing.List[T]:
    out = [end]
    while out[-1] in parents:
        out.append(parents[out[-1]])
    out.reverse()
    return out


def a_star(
        from_node: T,
        expand: typing.Callable[[T], typing.Iterable[typing.Tuple[int, T]]],
        to_node: T,
        heuristic: typing.Optional[typing.Callable[[T], int]] = None,
) -> typing.Tuple[int, typing.List[T]]:
    """
    expand should return an iterable of (dist, successor node) tuples.
    Returns (distance, path).
    """
    g_values, parents = dijkstra(from_node, to_node=to_node, expand=expand, heuristic=heuristic)
    if to_node not in g_values:
        raise Exception("couldn't reach to_node")
    return g_values[to_node], path_from_parents(parents, to_node)
