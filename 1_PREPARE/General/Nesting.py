# Develop, improve, and professsionalize this
import json
from typing import Dict, Any, Union, List, Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

@dataclass
class Component(ABC):
    name: str

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

@dataclass
class Object(Component):
    properties: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "properties": self.properties}

@dataclass
class Morphism(Component):
    source: str
    target: str
    properties: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source": self.source,
            "target": self.target,
            "properties": self.properties
        }

class CategoryTheorySystem:
    """
    A sophisticated class to represent and manipulate systems based on Category Theory concepts,
    allowing for the arbitrary nesting of systems. It supports adding objects, morphisms,
    nested systems, along with serialization, deserialization, and querying of the system state.

    This implementation uses dataclasses for better structure and type hinting, and
    includes advanced features such as component validation, error handling, and
    support for complex queries.
    """
    
    def __init__(self):
        self.system_components: Dict[str, Dict[str, Union[Object, Morphism, 'CategoryTheorySystem']]] = {
            "objects": {},
            "morphisms": {},
            "systems": {}
        }
    
    def add_component(self, component_type: str, name: str, *args, **kwargs) -> None:
        """
        General method to add objects, morphisms, or systems.
        
        Args:
            component_type (str): Type of component to add ('object', 'morphism', or 'system').
            name (str): Name of the component.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            ValueError: If the component type is unknown or if required arguments are missing.
        """
        component_methods = {
            "object": self._add_object,
            "morphism": self._add_morphism,
            "system": self._add_system
        }
        try:
            component_methods[component_type](name, *args, **kwargs)
        except KeyError:
            raise ValueError(f"Unknown component type: {component_type}")
        except TypeError as e:
            raise ValueError(f"Invalid arguments for {component_type}: {str(e)}")
    
    def _add_object(self, name: str, **kwargs) -> None:
        self.system_components["objects"][name] = Object(name, kwargs)
    
    def _add_morphism(self, name: str, source: str, target: str, **kwargs) -> None:
        if source not in self.system_components["objects"]:
            raise ValueError(f"Source object '{source}' does not exist")
        if target not in self.system_components["objects"]:
            raise ValueError(f"Target object '{target}' does not exist")
        self.system_components["morphisms"][name] = Morphism(name, source, target, kwargs)
    
    def _add_system(self, name: str, objects: Dict[str, Any], morphisms: Dict[str, Any]) -> None:
        nested_system = CategoryTheorySystem()
        for obj_name, obj_props in objects.items():
            nested_system.add_component("object", obj_name, **obj_props)
        for morph_name, morph_props in morphisms.items():
            source = morph_props.pop("source")
            target = morph_props.pop("target")
            nested_system.add_component("morphism", morph_name, source, target, **morph_props)
        self.system_components["systems"][name] = nested_system
    
    def serialize_system(self, filename: str) -> None:
        """
        Serialize the system to a JSON file.

        Args:
            filename (str): The name of the file to save the serialized system.
        """
        serializable_system = self._make_serializable(self.system_components)
        with open(filename, 'w') as file:
            json.dump(serializable_system, file, indent=4)
    
    def _make_serializable(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert the system components to a serializable format.

        Args:
            components (Dict[str, Any]): The system components to convert.

        Returns:
            Dict[str, Any]: A serializable version of the system components.
        """
        serializable = {}
        for key, value in components.items():
            if isinstance(value, dict):
                serializable[key] = {k: v.to_dict() if isinstance(v, (Object, Morphism)) else self._make_serializable(v.system_components) for k, v in value.items()}
            else:
                serializable[key] = value
        return serializable
    
    def load_system(self, filename: str) -> None:
        """
        Load a system from a JSON file.

        Args:
            filename (str): The name of the file to load the system from.
        """
        with open(filename, 'r') as file:
            loaded_system = json.load(file)
        self.system_components = self._reconstruct_system(loaded_system)
    
    def _reconstruct_system(self, loaded_system: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reconstruct the system from a loaded JSON structure.

        Args:
            loaded_system (Dict[str, Any]): The loaded system structure.

        Returns:
            Dict[str, Any]: The reconstructed system components.
        """
        reconstructed = {
            "objects": {},
            "morphisms": {},
            "systems": {}
        }
        for obj_name, obj_data in loaded_system["objects"].items():
            reconstructed["objects"][obj_name] = Object(obj_data["name"], obj_data["properties"])
        for morph_name, morph_data in loaded_system["morphisms"].items():
            reconstructed["morphisms"][morph_name] = Morphism(
                morph_data["name"],
                morph_data["source"],
                morph_data["target"],
                morph_data["properties"]
            )
        for sys_name, sys_data in loaded_system["systems"].items():
            nested_system = CategoryTheorySystem()
            nested_system.system_components = self._reconstruct_system(sys_data)
            reconstructed["systems"][sys_name] = nested_system
        return reconstructed
    
    def query_component(self, component_type: str, name: str) -> Optional[Union[Object, Morphism, 'CategoryTheorySystem']]:
        """
        Query a specific component by type and name.

        Args:
            component_type (str): The type of component to query ('object', 'morphism', or 'system').
            name (str): The name of the component to query.

        Returns:
            Optional[Union[Object, Morphism, 'CategoryTheorySystem']]: The queried component, or None if not found.
        """
        return self.system_components.get(component_type, {}).get(name)

    def list_components(self, component_type: str) -> List[str]:
        """
        List all components of a specific type.

        Args:
            component_type (str): The type of components to list ('object', 'morphism', or 'system').

        Returns:
            List[str]: A list of component names of the specified type.
        """
        return list(self.system_components.get(component_type, {}).keys())

    def query_morphisms(self, source: Optional[str] = None, target: Optional[str] = None) -> List[Morphism]:
        """
        Query morphisms based on source and/or target objects.

        Args:
            source (Optional[str]): The name of the source object.
            target (Optional[str]): The name of the target object.

        Returns:
            List[Morphism]: A list of morphisms matching the query criteria.
        """
        return [
            morph for morph in self.system_components["morphisms"].values()
            if (source is None or morph.source == source) and (target is None or morph.target == target)
        ]

    def get_composition(self, morphism1: str, morphism2: str) -> Optional[Morphism]:
        """
        Get the composition of two morphisms if they are composable.

        Args:
            morphism1 (str): The name of the first morphism.
            morphism2 (str): The name of the second morphism.

        Returns:
            Optional[Morphism]: The composed morphism if composable, None otherwise.
        """
        m1 = self.system_components["morphisms"].get(morphism1)
        m2 = self.system_components["morphisms"].get(morphism2)
        if m1 and m2 and m1.target == m2.source:
            return Morphism(f"{m1.name}_{m2.name}", m1.source, m2.target, {**m1.properties, **m2.properties})
        return None

# Example usage
if __name__ == "__main__":
    ct_system = CategoryTheorySystem()
    ct_system.add_component("object", "ObjectA", property1="value1")
    ct_system.add_component("object", "ObjectB", property2="value2")
    ct_system.add_component("morphism", "Morphism1", "ObjectA", "ObjectB", propertyM="valueM")
    ct_system.add_component("system", "NestedSystem1", 
                            {"ObjectC": {"property3": "value3"}}, 
                            {"Morphism2": {"source": "ObjectC", "target": "ObjectC", "propertyN": "valueN"}})
    
    # Serialize the system
    ct_system.serialize_system("category_theory_system.json")
    
    # Load the system
    new_system = CategoryTheorySystem()
    new_system.load_system("category_theory_system.json")
    
    # Query components
    print(new_system.query_component("object", "ObjectA"))
    print(new_system.query_component("morphism", "Morphism1"))
    
    # List components
    print(new_system.list_components("object"))
    
    # Query morphisms
    print(new_system.query_morphisms(source="ObjectA"))
    
    # Get composition
    ct_system.add_component("object", "ObjectC", property3="value3")
    ct_system.add_component("morphism", "Morphism2", "ObjectB", "ObjectC", propertyN="valueN")
    composed_morphism = ct_system.get_composition("Morphism1", "Morphism2")
    if composed_morphism:
        print(f"Composed morphism: {composed_morphism.name} from {composed_morphism.source} to {composed_morphism.target}")
