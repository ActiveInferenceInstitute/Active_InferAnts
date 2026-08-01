"""
Active Inference Student-Teacher POMDP Implementation.

Demonstrates core active inference concepts:
- Generative model with A, B, C, D matrices
- Bayesian belief updating
- Expected free energy minimization
- Policy selection via softmax
- Teacher-student knowledge interaction

Reference implementation for the Active InferAnts multi-language framework.
"""

import logging
import os
from typing import Optional

import numpy as np
from numpy.typing import NDArray
from scipy.special import softmax
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class TeacherModel:
    """Logistic-growth knowledge model for the teacher agent."""

    def __init__(self, n_states: int, growth_rate: float = 0.1, max_knowledge: float = 1.0) -> None:
        self.n_states = n_states
        self.growth_rate = growth_rate
        self.max_knowledge = max_knowledge
        self.knowledge: NDArray[np.float64] = np.zeros(n_states)
        logger.info("TeacherModel initialized: n_states=%d, growth_rate=%.3f", n_states, growth_rate)

    def update_knowledge(self, state: int) -> None:
        """Update teacher knowledge for a state using logistic growth."""
        current = self.knowledge[state]
        exp_gr = np.exp(self.growth_rate)
        denominator = self.max_knowledge + current * (exp_gr - 1)
        if denominator > 0:
            self.knowledge[state] = (self.max_knowledge * current * exp_gr) / denominator
        logger.debug("Knowledge updated for state %d: %.4f", state, self.knowledge[state])

    def get_knowledge(self) -> NDArray[np.float64]:
        """Return a copy of the current knowledge state."""
        return self.knowledge.copy()

    def suggest_resource(self, student_beliefs: NDArray[np.float64]) -> int:
        """Suggest resource based on student beliefs and teacher knowledge gaps."""
        gaps = (self.max_knowledge - self.knowledge) * student_beliefs
        suggestion = int(np.argmax(gaps))
        logger.debug("Suggested resource: state %d (gap=%.4f)", suggestion, gaps[suggestion])
        return suggestion


class StudentTeacherPOMDP:
    """
    Active Inference agent using a Student-Teacher POMDP formulation.

    Generative model:
        A: Likelihood matrix P(o|s), shape (n_observations, n_states)
        B: Transition tensor P(s'|s, a), shape (n_states, n_states, n_actions)
        C: Preference vector over observations, shape (n_observations,)
        D: Prior belief over initial states, shape (n_states,)
    """

    def __init__(self, n_states: int, n_observations: int, n_actions: int,
                 seed: Optional[int] = None) -> None:
        self.n_states = n_states
        self.n_observations = n_observations
        self.n_actions = n_actions

        # Deterministic reproducibility: the random draws that build the generative
        # model below (and the stochastic transitions/observations in step()) follow
        # the global NumPy RNG. Seeding at init makes a given (n_states, n_obs,
        # n_actions, seed) combination reproduce identical beliefs and trajectories.
        if seed is not None:
            np.random.seed(seed)

        # Generative model matrices
        self.A: NDArray[np.float64] = np.random.rand(n_observations, n_states)
        self.A /= self.A.sum(axis=0)  # Normalize columns
        self.B: NDArray[np.float64] = np.ones((n_states, n_states, n_actions)) / n_states
        self.C: NDArray[np.float64] = np.zeros(n_observations)

        # Prior and posterior beliefs
        self.D: NDArray[np.float64] = np.ones(n_states) / n_states
        self.d: NDArray[np.float64] = np.copy(self.D)

        # Teacher model
        self.teacher = TeacherModel(n_states)

        logger.info(
            "StudentTeacherPOMDP initialized: states=%d, obs=%d, actions=%d",
            n_states, n_observations, n_actions
        )

    def update_beliefs(self, observation: int) -> None:
        """Bayesian belief update: posterior proportional to P(o|s) * prior."""
        likelihood = self.A[observation, :]
        self.d = self.d * likelihood
        total = np.sum(self.d)
        if total > 0:
            self.d /= total
        logger.debug("Beliefs updated for obs=%d", observation)

    def get_action(self, action_probs: NDArray[np.float64]) -> int:
        """Select action with highest probability from softmax policy distribution."""
        return int(np.argmax(action_probs))

    def step(self, action: int) -> int:
        """Execute one perception-action cycle: transition, observe, update."""
        new_state = np.random.choice(self.n_states, p=self.B[:, np.argmax(self.d), action])
        observation = np.random.choice(self.n_observations, p=self.A[:, new_state])
        self.teacher.update_knowledge(new_state)
        self.update_beliefs(observation)
        logger.debug("Step: action=%d, new_state=%d, obs=%d", action, new_state, observation)
        return observation

    def calculate_free_energy(self, action_idx: int) -> float:
        """
        Compute (negative) expected free energy for a single action.

        Returns negative EFE so that argmax selects the best action.
        Uses np.clip for numerical stability to avoid log(0).
        """
        expected_states = np.dot(self.B[:, :, action_idx], self.d)
        expected_observations = np.dot(self.A, expected_states)

        pragmatic = np.dot(expected_observations, self.C)
        kl = np.sum(expected_states * np.log(
            np.clip(expected_states, 1e-16, None) / np.clip(self.D, 1e-16, None)
        ))

        free_energy = -(pragmatic + kl)
        return free_energy

    def infer_policy(self) -> NDArray[np.float64]:
        """Compute softmax policy distribution over actions via EFE minimization."""
        F = np.array([self.calculate_free_energy(a) for a in range(self.n_actions)])
        pi = softmax(F)
        return pi

    def plot_matrices(self, output_folder: str = 'output') -> None:
        """Plot generative model matrices to PNG files."""
        os.makedirs(output_folder, exist_ok=True)

        plt.figure(figsize=(10, 8))
        plt.imshow(self.A, cmap='viridis', aspect='auto')
        plt.colorbar(label='Probability')
        plt.title('A Matrix: Likelihood Model')
        plt.xlabel('States')
        plt.ylabel('Observations')
        plt.savefig(os.path.join(output_folder, 'A_matrix.png'))
        plt.close()

        fig, axes = plt.subplots(1, self.n_actions, figsize=(20, 5), squeeze=False)
        for a in range(self.n_actions):
            im = axes[0, a].imshow(self.B[:, :, a], cmap='viridis', aspect='auto')
            axes[0, a].set_title(f'Action {a}')
            axes[0, a].set_xlabel('Next State')
            axes[0, a].set_ylabel('Current State')
        fig.suptitle('B Matrix: Transition Model')
        fig.colorbar(im, ax=axes.ravel().tolist(), label='Probability')
        plt.savefig(os.path.join(output_folder, 'B_matrix.png'))
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_observations), self.C)
        plt.title('C Vector: Preference over Observations')
        plt.xlabel('Observations')
        plt.ylabel('Preference')
        plt.savefig(os.path.join(output_folder, 'C_vector.png'))
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), self.D)
        plt.title('D Vector: Prior Beliefs about Initial States')
        plt.xlabel('States')
        plt.ylabel('Probability')
        plt.savefig(os.path.join(output_folder, 'D_vector.png'))
        plt.close()
        logger.info("Matrices plotted to %s", output_folder)

    def plot_student_beliefs(self, beliefs: NDArray[np.float64], title: str,
                             output_folder: str = 'output') -> None:
        """Plot student belief distribution to PNG."""
        os.makedirs(output_folder, exist_ok=True)
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), beliefs)
        plt.title(f"Student's Beliefs: {title}")
        plt.xlabel('States')
        plt.ylabel('Belief Probability')
        safe_title = title.lower().replace(" ", "_")
        plt.savefig(os.path.join(output_folder, f'student_beliefs_{safe_title}.png'))
        plt.close()

    def plot_teacher_knowledge(self, title: str, output_folder: str = 'output') -> None:
        """Plot teacher knowledge levels to PNG."""
        os.makedirs(output_folder, exist_ok=True)
        knowledge = self.teacher.get_knowledge()
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), knowledge)
        plt.title(f"Teacher's Knowledge: {title}")
        plt.xlabel('States')
        plt.ylabel('Knowledge Level')
        safe_title = title.lower().replace(" ", "_")
        plt.savefig(os.path.join(output_folder, f'teacher_knowledge_{safe_title}.png'))
        plt.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    n_states = 10
    n_observations = 15
    n_actions = 5

    pomdp = StudentTeacherPOMDP(n_states, n_observations, n_actions)

    pomdp.plot_matrices()
    pomdp.plot_student_beliefs(pomdp.d, "Initial")
    pomdp.plot_teacher_knowledge("Initial")

    num_steps = 20
    for step in range(num_steps):
        pi = pomdp.infer_policy()
        action = pomdp.get_action(pi)
        observation = pomdp.step(action)
        print(f"Step {step + 1}: Action: {action}, Observation: {observation}")

        suggested_resource = pomdp.teacher.suggest_resource(pomdp.d)
        print(f"Teacher suggests focusing on aspect: {suggested_resource}")

    pomdp.plot_student_beliefs(pomdp.d, "Final")
    pomdp.plot_teacher_knowledge("Final")

    print("Final beliefs:", pomdp.d)
    print("Teacher's knowledge:", pomdp.teacher.get_knowledge())
    print("\n✅ Python simulation completed successfully!")