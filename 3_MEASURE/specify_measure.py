from typing import List, Dict, Any, Optional, Union
from enum import Enum, auto
from dataclasses import dataclass, field
import json
from abc import ABC, abstractmethod
import numpy as np


class MeasurementMethod(Enum):
    """Enumeration of supported measurement methods."""
    PROJECTIVE = auto()
    POVM = auto()
    WEAK = auto()
    CONTINUOUS = auto()
    ADAPTIVE = auto()  # New adaptive measurement method

@dataclass
class QRFParameters:
    """Dataclass for Quantum Reference Frame parameters."""
    dimension: int
    symmetry_group: str
    reference_state: Dict[str, Any]
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate QRF parameters after initialization."""
        if self.dimension < 2:
            raise ValueError("Dimension must be at least 2.")
        if not isinstance(self.symmetry_group, str):
            raise TypeError("Symmetry group must be a string.")
        if not isinstance(self.reference_state, dict):
            raise TypeError("Reference state must be a dictionary.")

class MeasurementStrategy(ABC):
    """Abstract base class for measurement strategies."""
    
    @abstractmethod
    def execute(self, quantum_state: np.ndarray) -> Union[np.ndarray, Dict[str, Any]]:
        """Execute the measurement strategy on a given quantum state."""
        pass

class ProjectiveMeasurementStrategy(MeasurementStrategy):
    """Concrete implementation of projective measurement strategy."""

    def execute(self, quantum_state: np.ndarray) -> np.ndarray:
        """Execute a projective measurement and return Born-rule outcome
        probabilities.

        For a state vector ``psi`` (1-D, length = dimension), the probability of
        each outcome in the standard basis is ``|psi_i|^2``, normalised to a valid
        probability distribution.
        """
        state = np.asarray(quantum_state, dtype=complex)
        if state.ndim != 1 or state.size < 1:
            raise ValueError("Projective measurement requires a 1-D state vector")
        probabilities = np.abs(state) ** 2
        total = probabilities.sum()
        if total <= 0:
            raise ValueError("State has zero norm; cannot measure")
        return probabilities / total

class POVMMeasurementStrategy(MeasurementStrategy):
    """Concrete implementation of POVM (Positive Operator-Valued Measure) measurement strategy."""

    def execute(self, quantum_state: np.ndarray) -> Dict[str, Any]:
        """Execute a rank-1 POVM measurement.

        Constructs a resolution of the identity from an orthonormal basis and
        returns the Born-rule outcome probabilities, along with the associated
        outcome labels — a real (simple) POVM, not a random projection.
        """
        state = np.asarray(quantum_state, dtype=complex)
        if state.ndim != 1 or state.size < 1:
            raise ValueError("POVM measurement requires a 1-D state vector")
        probabilities = np.abs(state) ** 2
        total = probabilities.sum()
        if total <= 0:
            raise ValueError("State has zero norm; cannot measure")
        probabilities = probabilities / total
        return {
            "POVM_probabilities": probabilities.tolist(),
            "outcomes": [f"o{i}" for i in range(state.size)],
        }

class WeakMeasurementStrategy(MeasurementStrategy):
    """Concrete implementation of weak measurement strategy."""

    def execute(self, quantum_state: np.ndarray) -> Dict[str, Any]:
        """Weak measurement is not yet implemented; refuse rather than return a
        fabricated random projection."""
        raise NotImplementedError(
            "WeakMeasurementStrategy is not implemented. Provide a weakly-coupled "
            "observable and a coupling strength to implement it."
        )

class ContinuousMeasurementStrategy(MeasurementStrategy):
    """Concrete implementation of continuous measurement strategy."""

    def execute(self, quantum_state: np.ndarray) -> Dict[str, Any]:
        """Continuous measurement is not yet implemented; refuse rather than
        return a fabricated random result."""
        raise NotImplementedError(
            "ContinuousMeasurementStrategy is not implemented. Specify a stochastic "
            "master-equation or measurement record to implement it."
        )

class AdaptiveMeasurementStrategy(MeasurementStrategy):
    """Concrete implementation of adaptive measurement strategy."""

    def execute(self, quantum_state: np.ndarray) -> Dict[str, Any]:
        """Adaptive measurement is not yet implemented; refuse rather than
        return a fabricated random result."""
        raise NotImplementedError(
            "AdaptiveMeasurementStrategy is not implemented. Provide a feedback "
            "policy to implement it."
        )


class QuantumCognitiveMeasure:
    """
    Enhances the specifications for quantum cognitive measurements,
    integrating quantum reference frame (QRF) calculations with advanced measurement techniques.
    """
    
    def __init__(self, measurement_name: str, qrf_parameters: Optional[QRFParameters] = None, 
                 measurement_methods: Optional[List[MeasurementMethod]] = None):
        """
        Constructs the quantum cognitive measurement specifications.
        
        Parameters:
        - measurement_name (str): The identifier for the measurement.
        - qrf_parameters (Optional[QRFParameters]): Configuration for QRF calculations.
        - measurement_methods (Optional[List[MeasurementMethod]]): Enumeration of measurement techniques.
        """
        self.measurement_name = measurement_name
        self.qrf_parameters = qrf_parameters or QRFParameters(dimension=2, symmetry_group="SU(2)", reference_state={})
        self.measurement_methods = measurement_methods or []
        self.measurement_strategies: Dict[MeasurementMethod, MeasurementStrategy] = {}
        self._initialize_default_strategies()
    
    def _initialize_default_strategies(self) -> None:
        """Initialize default measurement strategies."""
        self.measurement_strategies[MeasurementMethod.PROJECTIVE] = ProjectiveMeasurementStrategy()
        self.measurement_strategies[MeasurementMethod.POVM] = POVMMeasurementStrategy()
        self.measurement_strategies[MeasurementMethod.WEAK] = WeakMeasurementStrategy()
        self.measurement_strategies[MeasurementMethod.CONTINUOUS] = ContinuousMeasurementStrategy()
        self.measurement_strategies[MeasurementMethod.ADAPTIVE] = AdaptiveMeasurementStrategy()
        # ... any additional strategies ...
    
    def set_qrf_parameters(self, qrf_parameters: QRFParameters) -> None:
        """
        Sets the QRF configuration parameters.
        
        Parameters:
        - qrf_parameters (QRFParameters): The parameters for QRF calculations.
        """
        self.qrf_parameters = qrf_parameters
    
    def get_qrf_parameters(self) -> QRFParameters:
        """
        Accesses the QRF configuration parameters.
        
        Returns:
        - QRFParameters: The parameters for QRF calculations.
        """
        return self.qrf_parameters
    
    def add_measurement_method(self, method: MeasurementMethod, strategy: Optional[MeasurementStrategy] = None) -> None:
        """
        Adds a measurement method and its corresponding strategy.
        
        Parameters:
        - method (MeasurementMethod): The measurement method to add.
        - strategy (Optional[MeasurementStrategy]): The strategy for executing the measurement.
        """
        if method not in self.measurement_methods:
            self.measurement_methods.append(method)
        if strategy:
            self.measurement_strategies[method] = strategy
        elif method not in self.measurement_strategies:
            raise ValueError(f"No default strategy available for {method.name}. Please provide a strategy.")
    
    def get_measurement_methods(self) -> List[Dict[str, str]]:
        """
        Enumerates the selected measurement techniques and their descriptions.
        
        Returns:
        - List[Dict[str, str]]: A list of measurement techniques with descriptions.
        """
        return [{"method": method.name, "description": f"Utilizes {method.name.lower()} measurement technique"} 
                for method in self.measurement_methods]
    
    def execute_measurement(self, method: MeasurementMethod, quantum_state: np.ndarray) -> Union[np.ndarray, Dict[str, Any]]:
        """
        Executes a specific measurement method on a given quantum state.
        
        Parameters:
        - method (MeasurementMethod): The measurement method to execute.
        - quantum_state (np.ndarray): The quantum state to measure.
        
        Returns:
        - Union[np.ndarray, Dict[str, Any]]: The result of the measurement.
        
        Raises:
        - ValueError: If the specified method is not available.
        """
        if method not in self.measurement_strategies:
            raise ValueError(f"Measurement method {method.name} is not available.")
        return self.measurement_strategies[method].execute(quantum_state)
    
    def compile_measurement_specification(self) -> Dict[str, Any]:
        """
        Aggregates the quantum cognitive measurement specifications into a unified document.
        
        Returns:
        - Dict[str, Any]: The aggregated specifications for the measurement.
        """
        specification = {
            "measurement_name": self.measurement_name,
            "qrf_parameters": {
                "dimension": self.qrf_parameters.dimension,
                "symmetry_group": self.qrf_parameters.symmetry_group,
                "reference_state": self.qrf_parameters.reference_state,
                "additional_params": self.qrf_parameters.additional_params
            },
            "measurement_methods": self.get_measurement_methods()
        }
        return specification
    
    def save_specification(self, filename: str) -> None:
        """
        Saves the measurement specification to a JSON file.
        
        Parameters:
        - filename (str): The name of the file to save the specification to.
        """
        with open(filename, 'w') as f:
            json.dump(self.compile_measurement_specification(), f, indent=2)
    
    @classmethod
    def load_specification(cls, filename: str) -> 'QuantumCognitiveMeasure':
        """
        Loads a measurement specification from a JSON file.
        
        Parameters:
        - filename (str): The name of the file to load the specification from.
        
        Returns:
        - QuantumCognitiveMeasure: A new instance with the loaded specification.
        """
        with open(filename, 'r') as f:
            spec = json.load(f)
        
        qrf_params = QRFParameters(
            dimension=spec['qrf_parameters']['dimension'],
            symmetry_group=spec['qrf_parameters']['symmetry_group'],
            reference_state=spec['qrf_parameters']['reference_state'],
            additional_params=spec['qrf_parameters']['additional_params']
        )
        
        methods = [MeasurementMethod[method['method']] for method in spec['measurement_methods']]
        
        instance = cls(spec['measurement_name'], qrf_params, methods)
        instance._initialize_default_strategies()
        return instance
