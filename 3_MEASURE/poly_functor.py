from typing import Any, Callable, Generic, Tuple, TypeVar

# Type variables for input and output types
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")


class PolyFunctor(Generic[A, B]):
    """
    A generic Polynomial Functor for heterogeneous data structures.
    """

    def hmap(self, func: Callable[[A], B], data: Any) -> Any:
        """
        Applies a polymorphic function to the data structure.

        Args:
            func: A polymorphic function to apply.
            data: The data structure to be transformed.

        Returns:
            A new data structure with the function applied.
        """
        raise NotImplementedError("hmap must be implemented by subclasses.")


class Tuple2Functor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for 2-tuples.
    """

    def hmap(self, func: Callable[[A], B], data: Tuple[A, A]) -> Tuple[B, B]:
        """
        Applies the function to both elements of a 2-tuple.

        Args:
            func: A polymorphic function to apply.
            data: A 2-tuple of type (A, A).

        Returns:
            A new 2-tuple with the function applied to each element.
        """
        if not isinstance(data, tuple) or len(data) != 2:
            raise ValueError("Input data must be a 2-tuple.")
        return (func(data[0]), func(data[1]))


class Tuple3Functor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for 3-tuples.
    """

    def hmap(self, func: Callable[[A], B], data: Tuple[A, A, A]) -> Tuple[B, B, B]:
        """
        Applies the function to all three elements of a 3-tuple.

        Args:
            func: A polymorphic function to apply.
            data: A 3-tuple of type (A, A, A).

        Returns:
            A new 3-tuple with the function applied to each element.
        """
        if not isinstance(data, tuple) or len(data) != 3:
            raise ValueError("Input data must be a 3-tuple.")
        return (func(data[0]), func(data[1]), func(data[2]))


class ListFunctor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for lists.
    """

    def hmap(self, func: Callable[[A], B], data: list) -> list:
        """
        Applies the function to each element of the list.

        Args:
            func: A polymorphic function to apply.
            data: A list of elements of type A.

        Returns:
            A new list with the function applied to each element.
        """
        if not isinstance(data, list):
            raise ValueError("Input data must be a list.")
        return [func(element) for element in data]


class MaybeFunctor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for Maybe type.
    Represents an optional value.
    """

    def hmap(self, func: Callable[[A], B], data: Any) -> Any:
        """
        Applies the function to the value if it exists.

        Args:
            func: A polymorphic function to apply.
            data: Either None or a value of type A.

        Returns:
            The result of applying the function to the value, or None.
        """
        if data is None:
            return None
        return func(data)


class EitherFunctor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for Either type.
    Represents a value of two possible types (Left or Right).
    """

    def hmap(self, func: Callable[[A], B], data: Tuple[str, Any]) -> Tuple[str, Any]:
        """
        Applies the function to the Right value.

        Args:
            func: A polymorphic function to apply.
            data: A tuple where the first element is 'Left' or 'Right',
                  and the second element is the value.

        Returns:
            A new Either type with the function applied to the Right value,
            or unchanged if it's a Left.
        """
        if not (isinstance(data, tuple) and len(data) == 2):
            raise ValueError(
                "Input data must be a tuple of ('Left' or 'Right', value)."
            )

        tag, value = data
        if tag == "Left":
            return data
        elif tag == "Right":
            return ("Right", func(value))
        else:
            raise ValueError("First element of the tuple must be 'Left' or 'Right'.")


class Tree:
    """
    A simple binary tree structure.
    """

    def __init__(self, value: A, left: "Tree" = None, right: "Tree" = None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Tree({self.value}, {self.left}, {self.right})"


class TreeFunctor(PolyFunctor[A, B]):
    """
    Polynomial Functor instance for binary trees.
    """

    def hmap(self, func: Callable[[A], B], data: Tree) -> Tree:
        """
        Applies the function to each node in the binary tree.

        Args:
            func: A polymorphic function to apply.
            data: A Tree instance.

        Returns:
            A new Tree with the function applied to each node.
        """
        if not isinstance(data, Tree):
            raise ValueError("Input data must be a Tree instance.")
        new_left = self.hmap(func, data.left) if data.left else None
        new_right = self.hmap(func, data.right) if data.right else None
        return Tree(func(data.value), new_left, new_right)


# Example usage
if __name__ == "__main__":

    def triple(x: int) -> int:
        """
        Example polymorphic function that triples an integer.

        Args:
            x: An integer to triple.

        Returns:
            The tripled integer.
        """
        return 3 * x

    # Instantiate functors
    tuple2_functor = Tuple2Functor[int, int]()
    tuple3_functor = Tuple3Functor[int, int]()
    list_functor = ListFunctor[int, int]()
    maybe_functor = MaybeFunctor[int, int]()
    either_functor = EitherFunctor[int, int]()
    tree_functor = TreeFunctor[int, int]()

    # Apply hmap to a 2-tuple
    data2 = (3, 4)
    result2 = tuple2_functor.hmap(triple, data2)
    print(f"hmap result on 2-tuple: {result2}")  # Output: (9, 12)

    # Apply hmap to a 3-tuple
    data3 = (3, 4, 5)
    result3 = tuple3_functor.hmap(triple, data3)
    print(f"hmap result on 3-tuple: {result3}")  # Output: (9, 12, 15)

    # Apply hmap to a list
    data_list = [1, 2, 3, 4]
    result_list = list_functor.hmap(triple, data_list)
    print(f"hmap result on list: {result_list}")  # Output: [3, 6, 9, 12]

    # Apply hmap to a Maybe type (Some value)
    data_maybe_some = 5
    result_maybe_some = maybe_functor.hmap(triple, data_maybe_some)
    print(f"hmap result on Maybe Some: {result_maybe_some}")  # Output: 15

    # Apply hmap to a Maybe type (None)
    data_maybe_none = None
    result_maybe_none = maybe_functor.hmap(triple, data_maybe_none)
    print(f"hmap result on Maybe None: {result_maybe_none}")  # Output: None

    # Apply hmap to an Either type (Right value)
    data_either_right = ("Right", 7)
    result_either_right = either_functor.hmap(triple, data_either_right)
    print(
        f"hmap result on Either Right: {result_either_right}"
    )  # Output: ('Right', 21)

    # Apply hmap to an Either type (Left value)
    data_either_left = ("Left", "Error")
    result_either_left = either_functor.hmap(triple, data_either_left)
    print(
        f"hmap result on Either Left: {result_either_left}"
    )  # Output: ('Left', 'Error')

    # Apply hmap to a binary tree
    data_tree = Tree(2, Tree(3), Tree(4))
    result_tree = tree_functor.hmap(triple, data_tree)
    print(
        f"hmap result on Tree: {result_tree}"
    )  # Output: Tree(6, Tree(9, None, None), Tree(12, None, None))
