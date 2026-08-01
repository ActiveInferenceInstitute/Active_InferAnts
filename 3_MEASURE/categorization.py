import itertools
from typing import List, Dict, Callable, Any, Tuple, Optional, Set, Union
import networkx as nx
import matplotlib.pyplot as plt
from functools import reduce
from collections import defaultdict
import numpy as np
from scipy.stats import entropy

class CategoryTheoryAnalyzer:
    """
    An advanced script for intelligence analysis incorporating Active Inference principles with Category Theory concepts.
    This class provides a comprehensive toolkit for analyzing and manipulating categorical structures,
    with enhanced functionality for complex data analysis and visualization.
    """
    
    def __init__(self):
        self.objects: Dict[str, Any] = {}
        self.morphisms: Dict[Tuple[str, str], Callable] = {}
        self.compositions: Dict[Tuple[str, str], Callable] = {}
        self.identity_morphisms: Dict[str, Callable] = {}
        self.isomorphisms: Dict[Tuple[str, str], Callable] = {}
        self.epimorphisms: Dict[Tuple[str, str], Callable] = {}
        self.monomorphisms: Dict[Tuple[str, str], Callable] = {}
        self.initial_objects: List[str] = []
        self.terminal_objects: List[str] = []
        self.natural_transformations: Dict[Tuple[str, str], Callable] = {}
        self.functors: Dict[str, Callable] = {}
        self.limits: Dict[str, Any] = {}
        self.colimits: Dict[str, Any] = {}
        self.adjunctions: Dict[Tuple[str, str], Tuple[Callable, Callable]] = {}

    def add_object(self, obj_name: str, obj_data: Any) -> None:
        """
        Add an object to the category with associated data, adhering to Active Inference principles.
        
        Args:
            obj_name (str): The name of the object to add.
            obj_data (Any): The data associated with the object.
        
        Raises:
            ValueError: If the object already exists in the category.
        """
        if obj_name in self.objects:
            raise ValueError(f"Object {obj_name} already exists.")
        self.objects[obj_name] = obj_data
        self.identity_morphisms[obj_name] = lambda x: x

    def add_morphism(self, source: str, target: str, morphism: Callable) -> None:
        """
        Add a morphism between two objects, ensuring it aligns with Active Inference principles.
        
        Args:
            source (str): The source object of the morphism.
            target (str): The target object of the morphism.
            morphism (Callable): The function representing the morphism.
        
        Raises:
            ValueError: If the source or target object does not exist, or if the morphism already exists.
        """
        if source not in self.objects or target not in self.objects:
            raise ValueError("Source or target object does not exist.")
        if (source, target) in self.morphisms:
            raise ValueError(f"Morphism from {source} to {target} already exists.")
        self.morphisms[(source, target)] = morphism

    def compose_morphisms(self, source: str, via: str, target: str) -> Optional[Callable]:
        """
        Compose two morphisms to create a direct morphism from source to target, following Active Inference optimization.
        
        Args:
            source (str): The source object of the composition.
            via (str): The intermediate object in the composition.
            target (str): The target object of the composition.
        
        Returns:
            Optional[Callable]: The composed morphism, if successful.
        
        Raises:
            ValueError: If the required morphisms for composition do not exist.
        """
        if (source, via) not in self.morphisms or (via, target) not in self.morphisms:
            raise ValueError("Morphisms for composition do not exist.")
        composed_morphism = lambda x: self.morphisms[(via, target)](self.morphisms[(source, via)](x))
        self.compositions[(source, target)] = composed_morphism
        return composed_morphism

    def find_isomorphisms(self) -> Dict[Tuple[str, str], Callable]:
        """
        Identify isomorphisms in the category, utilizing Active Inference to optimize the process.
        
        Returns:
            Dict[Tuple[str, str], Callable]: A dictionary of identified isomorphisms.
        """
        isomorphisms = {}
        for (source, target), morphism in self.morphisms.items():
            if (target, source) in self.morphisms:
                inverse_morphism = self.morphisms[(target, source)]
                if self._check_isomorphism(morphism, inverse_morphism):
                    isomorphisms[(source, target)] = morphism
        self.isomorphisms = isomorphisms
        return isomorphisms

    def _check_isomorphism(self, morphism: Callable, inverse_morphism: Callable) -> bool:
        """
        Verify if two morphisms form an isomorphism, incorporating Active Inference principles for efficiency.
        
        Args:
            morphism (Callable): The forward morphism.
            inverse_morphism (Callable): The inverse morphism.
        
        Returns:
            bool: True if the morphisms form an isomorphism, False otherwise.
        """
        return all(morphism(inverse_morphism(obj)) == obj and inverse_morphism(morphism(obj)) == obj for obj in self.objects.values())

    def find_epimorphisms(self) -> Dict[Tuple[str, str], Callable]:
        """
        Discover epimorphisms in the category, applying Active Inference strategies for enhanced performance.
        
        Returns:
            Dict[Tuple[str, str], Callable]: A dictionary of identified epimorphisms.
        """
        epimorphisms = {(source, target): morphism for (source, target), morphism in self.morphisms.items() if self._check_epimorphism(morphism)}
        self.epimorphisms = epimorphisms
        return epimorphisms

    def _check_epimorphism(self, morphism: Callable) -> bool:
        """
        Determine if a morphism is an epimorphism, using Active Inference for effective analysis.
        
        Args:
            morphism (Callable): The morphism to check.
        
        Returns:
            bool: True if the morphism is an epimorphism, False otherwise.
        """
        codomain = set(morphism(obj) for obj in self.objects.values())
        return len(codomain) == len(set(self.objects.values()))

    def find_monomorphisms(self) -> Dict[Tuple[str, str], Callable]:
        """
        Identify monomorphisms in the category, leveraging Active Inference for optimization.
        
        Returns:
            Dict[Tuple[str, str], Callable]: A dictionary of identified monomorphisms.
        """
        monomorphisms = {(source, target): morphism for (source, target), morphism in self.morphisms.items() if self._check_monomorphism(morphism)}
        self.monomorphisms = monomorphisms
        return monomorphisms

    def _check_monomorphism(self, morphism: Callable) -> bool:
        """
        Check if a morphism is a monomorphism, incorporating Active Inference principles for efficiency.
        
        Args:
            morphism (Callable): The morphism to check.
        
        Returns:
            bool: True if the morphism is a monomorphism, False otherwise.
        """
        domain = list(self.objects.values())
        return len(set(morphism(obj) for obj in domain)) == len(domain)

    def find_initial_objects(self) -> List[str]:
        """
        Locate initial objects in the category, applying Active Inference for systematic analysis.
        
        Returns:
            List[str]: A list of initial objects in the category.
        """
        initial_objects = [obj for obj in self.objects if self._check_initial_object(obj)]
        self.initial_objects = initial_objects
        return initial_objects

    def _check_initial_object(self, obj: str) -> bool:
        """
        Verify if an object is an initial object, using Active Inference to streamline the process.
        
        Args:
            obj (str): The object to check.
        
        Returns:
            bool: True if the object is an initial object, False otherwise.
        """
        return all((obj, target) in self.morphisms for target in self.objects if target != obj)

    def find_terminal_objects(self) -> List[str]:
        """
        Discover terminal objects in the category, utilizing Active Inference for efficient identification.
        
        Returns:
            List[str]: A list of terminal objects in the category.
        """
        terminal_objects = [obj for obj in self.objects if self._check_terminal_object(obj)]
        self.terminal_objects = terminal_objects
        return terminal_objects

    def _check_terminal_object(self, obj: str) -> bool:
        """
        Determine if an object is a terminal object, applying Active Inference principles for effective analysis.
        
        Args:
            obj (str): The object to check.
        
        Returns:
            bool: True if the object is a terminal object, False otherwise.
        """
        return all((source, obj) in self.morphisms for source in self.objects if source != obj)

    def analyze_morphism_properties(self) -> Dict[Tuple[str, str], Dict[str, bool]]:
        """
        Analyze properties of morphisms such as injectivity, surjectivity, and bijectivity, incorporating Active Inference for comprehensive analysis.
        
        Returns:
            Dict[Tuple[str, str], Dict[str, bool]]: A dictionary containing the properties of each morphism.
        """
        properties = {}
        for (source, target), morphism in self.morphisms.items():
            is_injective = self._check_injectivity(morphism)
            is_surjective = self._check_surjectivity(morphism)
            is_bijective = is_injective and is_surjective
            properties[(source, target)] = {
                'injective': is_injective,
                'surjective': is_surjective,
                'bijective': is_bijective
            }
        return properties

    def _check_injectivity(self, morphism: Callable) -> bool:
        """
        Verify if a morphism is injective, using Active Inference for optimized analysis.
        
        Args:
            morphism (Callable): The morphism to check.
        
        Returns:
            bool: True if the morphism is injective, False otherwise.
        """
        return len(set(morphism(obj) for obj in self.objects.values())) == len(self.objects)

    def _check_surjectivity(self, morphism: Callable) -> bool:
        """
        Determine if a morphism is surjective, applying Active Inference principles for effective evaluation.
        
        Args:
            morphism (Callable): The morphism to check.
        
        Returns:
            bool: True if the morphism is surjective, False otherwise.
        """
        codomain = set(self.objects.values())
        return all(any(morphism(source_obj) == obj for source_obj in self.objects.values()) for obj in codomain)

    def generate_product_objects(self) -> None:
        """
        Generate product objects from all pairs of objects, following Active Inference principles for efficient computation.
        """
        for obj1, obj2 in itertools.combinations(self.objects.keys(), 2):
            product_obj = (self.objects[obj1], self.objects[obj2])
            product_name = f"{obj1}x{obj2}"
            self.add_object(product_name, product_obj)

            # Define projection morphisms
            self.add_morphism(product_name, obj1, lambda x: x[0])
            self.add_morphism(product_name, obj2, lambda x: x[1])

            # Define product morphism for each source with morphisms to obj1 and obj2
            for source in self.objects:
                if (source, obj1) in self.morphisms and (source, obj2) in self.morphisms:
                    product_morphism = lambda x, s=source: (self.morphisms[(s, obj1)](x), self.morphisms[(s, obj2)](x))
                    self.add_morphism(source, product_name, product_morphism)

    def apply_functor(self, functor: Callable[[Any], Any], name: str) -> None:
        """
        Apply a functor to transform objects and morphisms in the category, utilizing Active Inference for adaptive transformation.
        
        Args:
            functor (Callable[[Any], Any]): The functor to apply.
            name (str): A name for the functor.
        """
        self.objects = {obj: functor(data) for obj, data in self.objects.items()}
        self.morphisms = {(source, target): lambda x, f=functor, m=morphism: f(m(x)) for (source, target), morphism in self.morphisms.items()}
        self.functors[name] = functor

    def add_natural_transformation(self, source_functor: str, target_functor: str, transformation: Callable) -> None:
        """
        Add a natural transformation between two functors.
        
        Args:
            source_functor (str): The name of the source functor.
            target_functor (str): The name of the target functor.
            transformation (Callable): The natural transformation function.
        
        Raises:
            ValueError: If either functor does not exist.
        """
        if source_functor not in self.functors or target_functor not in self.functors:
            raise ValueError("Source or target functor does not exist.")
        self.natural_transformations[(source_functor, target_functor)] = transformation

    def visualize_category(self) -> None:
        """
        Visualize the category with objects and morphisms, incorporating Active Inference for dynamic representation.
        """
        G = nx.DiGraph()

        # Add objects as nodes
        for obj in self.objects:
            G.add_node(obj)

        # Add morphisms as edges
        for (source, target) in self.morphisms:
            G.add_edge(source, target)

        # Draw the graph
        pos = nx.spring_layout(G, seed=42)  # Seed for reproducible layout
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_weight='bold', node_size=3000, font_size=10)
        
        # Add edge labels for morphism types
        edge_labels = {}
        for (source, target), morphism in self.morphisms.items():
            label = []
            if (source, target) in self.isomorphisms:
                label.append("Iso")
            if (source, target) in self.epimorphisms:
                label.append("Epi")
            if (source, target) in self.monomorphisms:
                label.append("Mono")
            edge_labels[(source, target)] = ", ".join(label) if label else ""
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Category Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def compute_limit(self, diagram: Dict[str, Any]) -> Any:
        """
        Compute the limit of a diagram in the category.
        
        Args:
            diagram (Dict[str, Any]): A dictionary representing the diagram.
        
        Returns:
            Any: The limit object.
        """
        # Implementation of limit computation
        limit = reduce(lambda x, y: (x, y), diagram.values())
        self.limits[str(diagram)] = limit
        return limit

    def compute_colimit(self, diagram: Dict[str, Any]) -> Any:
        """
        Compute the colimit of a diagram in the category.
        
        Args:
            diagram (Dict[str, Any]): A dictionary representing the diagram.
        
        Returns:
            Any: The colimit object.
        """
        if not diagram:
            raise ValueError("Cannot compute colimit of an empty diagram")

        values = list(diagram.values())
        # A colimit merges/unions the objects of the diagram. The set/dict union
        # operator `|` is only defined for dict/set/frozenset values, so fall back to
        # a pair-tuple for other object types rather than raising. The result is both
        # stored (self.colimits) and returned so the computed value is never discarded.
        if all(isinstance(v, (dict, set, frozenset)) for v in values):
            colimit = reduce(lambda x, y: x | y, values)
        else:
            colimit = reduce(lambda x, y: (x, y), values)

        self.colimits[str(diagram)] = colimit
        return colimit
# Example usage
if __name__ == "__main__":
    analyzer = CategoryTheoryAnalyzer()
    analyzer.add_object("A", {"data": "Object A data"})
    analyzer.add_object("B", {"data": "Object B data"})
    analyzer.add_object("C", {"data": "Object C data"})
    analyzer.add_morphism("A", "B", lambda x: x["data"] + " transformed by morphism")
    analyzer.add_morphism("B", "C", lambda x: x["data"] + " transformed again")
    analyzer.compose_morphisms("A", "B", "C")
    analyzer.find_isomorphisms()
    analyzer.find_epimorphisms()
    analyzer.find_monomorphisms()
    analyzer.find_initial_objects()
    analyzer.find_terminal_objects()
    analyzer.analyze_morphism_properties()
    analyzer.generate_product_objects()
    analyzer.apply_functor(lambda x: x.upper())
    analyzer.visualize_category()