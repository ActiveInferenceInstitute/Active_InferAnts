from pymdp import inference, control, utils
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
import logging

class AntAgent:
    """
    An advanced agent employing active inference for sophisticated decision-making within an ant colony environment.
    This agent leverages a comprehensive generative model of its surroundings and colony dynamics.
    """
    def __init__(self, 
                 observation_model: np.ndarray, 
                 transition_model: np.ndarray, 
                 preference_model: np.ndarray, 
                 initial_state_distribution: np.ndarray, 
                 policy_prior: Optional[np.ndarray] = None, 
                 policy_length: int = 1, 
                 inference_depth: int = 1, 
                 controllable_factors: Optional[List[int]] = None, 
                 possible_policies: Optional[np.ndarray] = None,
                 learning_rate: float = 0.1):
        """
        Initializes the AntAgent with sophisticated models of the environment and its preferences.

        Args:
            observation_model (np.ndarray): Sensory mapping (A matrix) - Maps observations to states.
            transition_model (np.ndarray): State dynamics (B matrix) - Describes state transitions.
            preference_model (np.ndarray): Goals and desires (C matrix) - Encodes preferences over observations.
            initial_state_distribution (np.ndarray): Prior beliefs about initial states (D vector).
            policy_prior (Optional[np.ndarray]): Prior beliefs over policies (E vector).
            policy_length (int): Temporal horizon for policy consideration.
            inference_depth (int): Depth of future state inference.
            controllable_factors (Optional[List[int]]): Indices of factors the agent can control.
            possible_policies (Optional[np.ndarray]): Explicit set of policies to consider.
            learning_rate (float): Rate at which the agent updates its models based on experience.
        """
        self.logger = self._setup_logger()
        
        # Initialize generative model components
        self.observation_model = self._validate_and_process_model(observation_model, "Observation")
        self.transition_model = self._validate_and_process_model(transition_model, "Transition")
        self.preference_model = self._validate_preference_model(preference_model)
        self.initial_state_distribution = self._validate_and_process_distribution(initial_state_distribution, "Initial state")
        self.policy_prior = self._validate_and_process_policy_prior(policy_prior)
        
        self.generative_model = {
            'observation_model': self.observation_model,
            'transition_model': self.transition_model,
            'preference_model': self.preference_model,
            'initial_state_distribution': self.initial_state_distribution,
            'policy_prior': self.policy_prior
        }
        
        self.model_dimensions = self._calculate_model_dimensions()
        self.posterior_states = self.initial_state_distribution.copy()
        self.policy_length = policy_length
        self.inference_depth = inference_depth
        self.controllable_factors = controllable_factors or list(range(self.model_dimensions['num_factors']))
        self.possible_policies = possible_policies or self._define_possible_policies()
        self.learning_rate = learning_rate
        
        self.logger.info("AntAgent initialized successfully with the following dimensions:")
        self.logger.info(f"Model dimensions: {self.model_dimensions}")
        self.logger.info(f"Policy length: {self.policy_length}, Inference depth: {self.inference_depth}")

    def _setup_logger(self) -> logging.Logger:
        """Sets up and returns a logger for the AntAgent."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def _validate_and_process_model(self, model: np.ndarray, model_name: str) -> np.ndarray:
        """Validates and processes input models."""
        if not isinstance(model, np.ndarray):
            raise ValueError(f"{model_name} model must be a numpy array.")
        return utils.to_obj_array(model)

    def _validate_preference_model(self, model: np.ndarray) -> np.ndarray:
        """Validates the preference model."""
        if not isinstance(model, np.ndarray):
            raise ValueError("Preference model must be a numpy array.")
        return model

    def _validate_and_process_distribution(self, distribution: np.ndarray, dist_name: str) -> np.ndarray:
        """Validates and processes probability distributions."""
        if not isinstance(distribution, np.ndarray):
            raise ValueError(f"{dist_name} distribution must be a numpy array.")
        if not np.allclose(np.sum(distribution), 1):
            self.logger.warning(f"{dist_name} distribution does not sum to 1. Normalizing.")
            return distribution / np.sum(distribution)
        return distribution

    def _validate_and_process_policy_prior(self, prior: Optional[np.ndarray]) -> np.ndarray:
        """Validates and processes the policy prior."""
        if prior is None:
            # Calculate the number of policies based on controllable factors
            # Assuming each controllable factor has a predefined number of actions
            actions_per_factor = 2  # Example: each factor can have 2 actions
            num_policies = actions_per_factor ** len(self.controllable_factors)
            return np.ones(num_policies) / num_policies  # Initialize uniform prior
        return self._validate_and_process_distribution(prior, "Policy prior")

    def _calculate_model_dimensions(self) -> Dict[str, Any]:
        """Calculates and returns the dimensions of the agent's models."""
        num_observations = [model.shape[0] for model in self.observation_model]
        num_states = [model.shape[0] for model in self.transition_model]
        return {
            'num_observations': num_observations,
            'num_states': num_states,
            'num_modalities': len(num_observations),
            'num_factors': len(num_states)
        }

    def _define_possible_policies(self) -> np.ndarray:
        """Generates the set of feasible policies based on the agent's models."""
        return control.construct_policies(
            self.model_dimensions['num_states'], 
            self.model_dimensions['num_factors'], 
            self.policy_length, 
            self.controllable_factors
        )

    def update_beliefs_about_states(self, observation: np.ndarray) -> None:
        """
        Updates the agent's beliefs about hidden states based on new observations.
        
        Args:
            observation (np.ndarray): The latest sensory input.
        """
        self.posterior_states = inference.update_posterior_states(
            self.observation_model,
            observation,
            self.transition_model,
            self.posterior_states,
            self.policy_length,
            self.inference_depth
        )
        self.logger.debug(f"Updated posterior states: {self.posterior_states}")

    def update_beliefs_about_policies(self) -> None:
        """Refines the agent's beliefs over policies, integrating current states and model insights."""
        self.updated_policies, _ = control.update_posterior_policies(
            self.posterior_states,
            self.observation_model,
            self.transition_model,
            self.preference_model,
            self.possible_policies,
            self.policy_prior
        )
        self.logger.debug(f"Updated policy beliefs: {self.updated_policies}")

    def choose_action(self) -> np.ndarray:
        """Determines an action based on the agent's current policy beliefs."""
        action = control.sample_action(
            self.updated_policies,
            self.possible_policies,
            self.model_dimensions['num_factors'],
            self.controllable_factors
        )
        self.logger.info(f"Chosen action: {action}")
        return action

    def execute_step(self, observation: np.ndarray) -> np.ndarray:
        """
        Conducts a single action selection cycle based on a new observation.
        
        Args:
            observation (np.ndarray): The latest sensory input.
        
        Returns:
            np.ndarray: The chosen action.
        """
        self.update_beliefs_about_states(observation)
        self.update_beliefs_about_policies()
        return self.choose_action()

    def update_models(self, observation: np.ndarray, action: int, next_observation: np.ndarray) -> None:
        """
        Updates the agent's internal models based on observed transitions.
        
        Args:
            observation (np.ndarray): The initial observation.
            action (int): The action taken.
            next_observation (np.ndarray): The resulting observation after the action.
        """
        # Update transition model
        predicted_next_state = np.dot(self.transition_model[action], self.posterior_states)
        state_prediction_error = next_observation - predicted_next_state
        self.transition_model[action] += self.learning_rate * np.outer(state_prediction_error, self.posterior_states)
        
        # Update observation model
        observation_prediction = np.dot(self.observation_model, self.posterior_states)
        observation_prediction_error = observation - observation_prediction
        self.observation_model += self.learning_rate * np.outer(observation_prediction_error, self.posterior_states)
        
        self.logger.info("Updated internal models based on observed transition.")

    def save_agent_state(self, filepath: str) -> None:
        """
        Saves the current state of the agent to a file.
        
        Args:
            filepath (str): The path to save the agent state.
        """
        state = {
            'generative_model': self.generative_model,
            'posterior_states': self.posterior_states,
            'model_dimensions': self.model_dimensions,
            'policy_length': self.policy_length,
            'inference_depth': self.inference_depth,
            'controllable_factors': self.controllable_factors,
            'possible_policies': self.possible_policies,
            'learning_rate': self.learning_rate
        }
        np.save(filepath, state)
        self.logger.info(f"Agent state saved to {filepath}")

    @classmethod
    def load_agent_state(cls, filepath: str) -> 'AntAgent':
        """
        Loads an agent state from a file and returns a new AntAgent instance.

        Warning: the checkpoint is unpickled (``allow_pickle=True``), which can
        execute code in a tampered file. Only load checkpoints that were written
        by this agent / from a trusted source.

        Args:
            filepath (str): The path to load the agent state from.

        Returns:
            AntAgent: A new AntAgent instance with the loaded state.

        Raises:
            ValueError: If the checkpoint is missing required keys or malformed.
        """
        import warnings

        warnings.warn(
            "load_agent_state() unpickles the checkpoint (allow_pickle=True); "
            "only load files from a trusted source.",
            RuntimeWarning,
            stacklevel=2,
        )
        state = np.load(filepath, allow_pickle=True).item()

        # Fail closed on malformed/tampered checkpoints: require every key the
        # reconstruction below depends on, with the right container shapes.
        required_gm = (
            'observation_model', 'transition_model', 'preference_model',
            'initial_state_distribution', 'policy_prior',
        )
        if not isinstance(state, dict):
            raise ValueError("Checkpoint root is not a dict; refusing to load")
        for key in ('generative_model', 'posterior_states', 'policy_length',
                    'inference_depth', 'controllable_factors',
                    'possible_policies', 'learning_rate'):
            if key not in state:
                raise ValueError(f"Checkpoint missing required key: {key}")
        gm = state.get('generative_model')
        if not isinstance(gm, dict) or any(k not in gm for k in required_gm):
            raise ValueError("Checkpoint generative_model is malformed")

        agent = cls(
            observation_model=gm['observation_model'],
            transition_model=gm['transition_model'],
            preference_model=gm['preference_model'],
            initial_state_distribution=gm['initial_state_distribution'],
            policy_prior=gm['policy_prior'],
            policy_length=state['policy_length'],
            inference_depth=state['inference_depth'],
            controllable_factors=state['controllable_factors'],
            possible_policies=state['possible_policies'],
            learning_rate=state['learning_rate']
        )
        agent.posterior_states = state['posterior_states']
        agent.logger.info(f"Agent state loaded from {filepath}")
        return agent
