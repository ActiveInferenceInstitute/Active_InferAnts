import ast
import functools
import importlib
import inspect
import os
import sys
import types
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

T = TypeVar('T')


class MetaProgramming:
    """A utility class providing various meta-programming functionalities."""

    @staticmethod
    def get_class_methods(cls: Type[T]) -> List[str]:
        """
        Retrieve a list of callable method names for a given class, excluding special methods.

        Args:
            cls (Type[T]): The class to inspect.

        Returns:
            List[str]: A list of method names.
        """
        return [
            method
            for method in dir(cls)
            if callable(getattr(cls, method)) and not method.startswith("__")
        ]

    @staticmethod
    def get_function_signature(func: Callable[..., Any]) -> str:
        """
        Obtain the signature of a function as a string.

        Args:
            func (Callable[..., Any]): The function to inspect.

        Returns:
            str: The function's signature.
        """
        return str(inspect.signature(func))

    @staticmethod
    def get_source_code(obj: Union[Callable[..., Any], Type[Any]]) -> str:
        """
        Retrieve the source code of a function or class.

        Args:
            obj (Union[Callable[..., Any], Type[Any]]): The object to inspect.

        Returns:
            str: The source code of the object.

        Raises:
            TypeError: If the object is neither a function nor a class.
        """
        if not (inspect.isfunction(obj) or inspect.isclass(obj)):
            raise TypeError("Object must be a function or class")
        return inspect.getsource(obj)

    @staticmethod
    def create_dynamic_class(class_name: str, attributes: Dict[str, Any]) -> Type[Any]:
        """
        Dynamically create a new class with the specified attributes.

        Args:
            class_name (str): The name of the class to create.
            attributes (Dict[str, Any]): A dictionary of attribute names and their values.

        Returns:
            Type[Any]: The newly created class.
        """
        return type(class_name, (), attributes)

    @staticmethod
    def add_method_to_class(cls: Type[T], method_name: str, method: Callable[..., Any]) -> None:
        """
        Add a new method to an existing class.

        Args:
            cls (Type[T]): The class to modify.
            method_name (str): The name of the method to add.
            method (Callable[..., Any]): The method to add.

        Raises:
            AttributeError: If the method already exists in the class.
        """
        if hasattr(cls, method_name):
            raise AttributeError(f"Method '{method_name}' already exists in class '{cls.__name__}'")
        setattr(cls, method_name, method)

    @staticmethod
    def _exec_enabled(allow_exec: bool) -> bool:
        """Whether arbitrary code execution is permitted.

        ``modify_function`` / ``compile_ast`` materialise and can execute
        caller-supplied source, which is a full code-execution primitive. It is
        gated behind an explicit opt-in: pass ``allow_exec=True`` OR set the
        ``META_PROGRAMMING_ALLOW_EXEC`` environment variable. Without one of
        these, the call refuses rather than silently executing untrusted code.
        """
        if allow_exec:
            return True
        return bool(os.environ.get("META_PROGRAMMING_ALLOW_EXEC"))

    @staticmethod
    def modify_function(func: Callable[..., T], new_code: str,
                        allow_exec: bool = False) -> Callable[..., T]:
        """Replace the implementation of an existing function with new code.

        Warning: this compiles and installs ``new_code`` as a live callable,
        which is an arbitrary-code-execution primitive. Calling it executes the
        supplied source; it is refused unless ``allow_exec=True`` or the
        ``META_PROGRAMMING_ALLOW_EXEC`` environment variable is set.

        Args:
            func (Callable[..., T]): The function to modify.
            new_code (str): The new code for the function.
            allow_exec (bool): Explicitly opt in to code execution.

        Returns:
            Callable[..., T]: The modified function.

        Raises:
            RuntimeError: If code execution is not explicitly enabled.
            SyntaxError: If the new code contains invalid Python syntax.
        """
        if not MetaProgramming._exec_enabled(allow_exec):
            raise RuntimeError(
                "modify_function() would execute arbitrary code. Refusing unless "
                "allow_exec=True or META_PROGRAMMING_ALLOW_EXEC is set."
            )
        try:
            compiled_code = compile(new_code, "<string>", "exec")
        except SyntaxError as e:
            raise SyntaxError(f"Invalid syntax in new code: {e}")

        new_func = types.FunctionType(
            compiled_code.co_consts[0],
            func.__globals__,
            func.__name__,
            func.__defaults__,
            func.__closure__
        )
        functools.update_wrapper(new_func, func)
        return new_func

    @staticmethod
    def create_decorator(decorator_func: Callable[..., Callable[..., T]]) -> Callable[..., Callable[..., T]]:
        """
        Create a decorator from a decorator function.

        Args:
            decorator_func (Callable[..., Callable[..., T]]): The function to use as a decorator.

        Returns:
            Callable[..., Callable[..., T]]: The created decorator.
        """
        @functools.wraps(decorator_func)
        def wrapper(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def decorated(*args: Any, **kwargs: Any) -> T:
                return decorator_func(func, *args, **kwargs)
            return decorated
        return wrapper

    @staticmethod
    def parse_ast(code: str) -> ast.AST:
        """
        Parse a string of Python code into an Abstract Syntax Tree (AST).

        Args:
            code (str): The Python code to parse.

        Returns:
            ast.AST: The parsed AST.

        Raises:
            SyntaxError: If the code contains invalid Python syntax.
        """
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Invalid syntax in code: {e}")

    @staticmethod
    def modify_ast(tree: ast.AST, transformer: Type[ast.NodeTransformer]) -> ast.AST:
        """
        Apply a transformer to modify an AST.

        Args:
            tree (ast.AST): The AST to modify.
            transformer (Type[ast.NodeTransformer]): The transformer class to apply.

        Returns:
            ast.AST: The modified AST.
        """
        transformer_instance = transformer()
        return transformer_instance.visit(tree)

    @staticmethod
    def compile_ast(tree: ast.AST, filename: str = "<ast>",
                    allow_exec: bool = False) -> types.CodeType:
        """Compile an AST into a code object.

        Warning: compiling an AST into ``"exec"`` mode produces executable code;
        if that object is later run it is an arbitrary-code-execution primitive.
        Refused unless ``allow_exec=True`` or ``META_PROGRAMMING_ALLOW_EXEC`` is
        set.

        Args:
            tree (ast.AST): The AST to compile.
            filename (str, optional): The filename to associate with the code.
            allow_exec (bool): Explicitly opt in to compiling executable code.

        Returns:
            types.CodeType: The compiled code object.

        Raises:
            RuntimeError: If exec compilation is not explicitly enabled.
        """
        if not MetaProgramming._exec_enabled(allow_exec):
            raise RuntimeError(
                "compile_ast() would compile an executable code object. Refusing "
                "unless allow_exec=True or META_PROGRAMMING_ALLOW_EXEC is set."
            )
        return compile(tree, filename, "exec")

    @staticmethod
    def hot_reload_module(module_name: str) -> None:
        """
        Reload a module dynamically.

        Args:
            module_name (str): The name of the module to reload.

        Raises:
            ImportError: If the module cannot be imported or reloaded.
        """
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(f"Failed to import or reload module '{module_name}': {e}")

    @staticmethod
    def create_metaclass(name: str, bases: tuple, attrs: Dict[str, Any]) -> Type[Any]:
        """
        Create a custom metaclass.

        Args:
            name (str): The name of the metaclass.
            bases (tuple): Base classes for the metaclass.
            attrs (Dict[str, Any]): Attributes for the metaclass.

        Returns:
            Type[Any]: The created metaclass.
        """
        return type(name, bases, attrs)

    @staticmethod
    def introspect_object(obj: Any) -> Dict[str, Any]:
        """
        Introspect an object to retrieve its type, attributes, and methods.

        Args:
            obj (Any): The object to introspect.

        Returns:
            Dict[str, Any]: A dictionary containing the object's type, attributes, and methods.
        """
        return {
            "type": type(obj),
            "attributes": {
                attr: getattr(obj, attr)
                for attr in dir(obj)
                if not callable(getattr(obj, attr)) and not attr.startswith("__")
            },
            "methods": {
                method: getattr(obj, method)
                for method in dir(obj)
                if callable(getattr(obj, method)) and not method.startswith("__")
            }
        }

    @staticmethod
    def create_property_decorator() -> Callable[..., Any]:
        """
        Create a custom property decorator.

        Returns:
            Callable[..., Any]: The custom property decorator.
        """
        class CustomProperty:
            """A custom property descriptor."""

            def __init__(
                self,
                fget: Optional[Callable[[Any], Any]] = None,
                fset: Optional[Callable[[Any, Any], None]] = None,
                fdel: Optional[Callable[[Any], None]] = None,
                doc: Optional[str] = None
            ):
                self.fget = fget
                self.fset = fset
                self.fdel = fdel
                self.__doc__ = doc

            def __get__(self, obj: Any, objtype: Optional[Type[Any]] = None) -> Any:
                if obj is None:
                    return self
                if self.fget is None:
                    raise AttributeError("unreadable attribute")
                return self.fget(obj)

            def __set__(self, obj: Any, value: Any) -> None:
                if self.fset is None:
                    raise AttributeError("can't set attribute")
                self.fset(obj, value)

            def __delete__(self, obj: Any) -> None:
                if self.fdel is None:
                    raise AttributeError("can't delete attribute")
                self.fdel(obj)

            def getter(self, fget: Callable[[Any], Any]) -> 'CustomProperty':
                """Define a getter for the property."""
                return type(self)(fget, self.fset, self.fdel, self.__doc__)

            def setter(self, fset: Callable[[Any, Any], None]) -> 'CustomProperty':
                """Define a setter for the property."""
                return type(self)(self.fget, fset, self.fdel, self.__doc__)

            def deleter(self, fdel: Callable[[Any], None]) -> 'CustomProperty':
                """Define a deleter for the property."""
                return type(self)(self.fget, self.fset, fdel, self.__doc__)

        return CustomProperty

    @staticmethod
    def create_singleton_metaclass() -> Type[Any]:
        """
        Create a singleton metaclass to ensure a class only has one instance.

        Returns:
            Type[Any]: The singleton metaclass.
        """
        class Singleton(type):
            """A metaclass that creates a Singleton base class."""

            _instances: Dict[Type[Any], Any] = {}

            def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
                return cls._instances[cls]

        return Singleton

    @staticmethod
    def create_abstract_base_class(abstract_methods: List[str]) -> Type[Any]:
        """
        Create an abstract base class with specified abstract methods.

        Args:
            abstract_methods (List[str]): A list of method names to be declared as abstract.

        Returns:
            Type[Any]: The created abstract base class.
        """
        class AbstractBaseClass:
            """An abstract base class enforcing the implementation of specified methods."""

            def __init_subclass__(cls: Type[Any], **kwargs: Any) -> None:
                super().__init_subclass__(**kwargs)
                for method in abstract_methods:
                    if not hasattr(cls, method) or not callable(getattr(cls, method)):
                        raise NotImplementedError(
                            f"Subclass must implement abstract method '{method}'"
                        )

        return AbstractBaseClass


# Example usage
if __name__ == "__main__":
    # Create a dynamic class
    DynamicClass = MetaProgramming.create_dynamic_class("DynamicClass", {"x": 1, "y": 2})

    # Add a method to the dynamic class
    MetaProgramming.add_method_to_class(DynamicClass, "sum", lambda self: self.x + self.y)

    # Create an instance and use the added method
    instance = DynamicClass()
    print(instance.sum())  # Output: 3

    # Create a custom property decorator
    custom_property = MetaProgramming.create_property_decorator()

    class TestClass:
        def __init__(self):
            self._value = 0

        @custom_property
        def value(self):
            """Get the value."""
            return self._value

        @value.setter
        def value(self, new_value):
            """Set the value."""
            self._value = new_value

    test = TestClass()
    test.value = 10
    print(test.value)  # Output: 10

    # Create a singleton metaclass
    SingletonMeta = MetaProgramming.create_singleton_metaclass()

    class Singleton(metaclass=SingletonMeta):
        def __init__(self):
            self.value = 0

    s1 = Singleton()
    s2 = Singleton()
    print(s1 is s2)  # Output: True

    # Create an abstract base class
    AbstractBase = MetaProgramming.create_abstract_base_class(["abstract_method"])

    class ConcreteClass(AbstractBase):
        def abstract_method(self):
            """Implementation of the abstract method."""
            print("Implemented abstract method")

    concrete = ConcreteClass()
    concrete.abstract_method()  # Output: Implemented abstract method
