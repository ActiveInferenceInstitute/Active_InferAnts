import numpy as np
from scipy.special import softmax
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

# Standalone Teacher Model Implementation
class TeacherModel:
    def __init__(self, n_states, growth_rate=0.1, max_knowledge=1.0):
        self.n_states = n_states
        self.growth_rate = growth_rate
        self.max_knowledge = max_knowledge
        self.knowledge = np.zeros(n_states)

    def update_knowledge(self, state):
        """Update teacher knowledge using logistic growth model."""
        current = self.knowledge[state]
        exp_gr = np.exp(self.growth_rate)
        self.knowledge[state] = (self.max_knowledge * current * exp_gr) / \
                               (self.max_knowledge + current * (exp_gr - 1))

    def get_knowledge(self):
        """Get current knowledge state."""
        return self.knowledge.copy()

    def suggest_resource(self, student_beliefs):
        """Suggest resource based on student beliefs and teacher knowledge."""
        gaps = (self.max_knowledge - self.knowledge) * student_beliefs
        return np.argmax(gaps)

class StudentTeacherPOMDP:
    def __init__(self, n_states, n_observations, n_actions):
        self.n_states = n_states
        self.n_observations = n_observations
        self.n_actions = n_actions
        
        # Initialize transition, likelihood, and preference matrices
        self.A = np.random.rand(n_observations, n_states)  # Likelihood (observation model)
        self.A /= self.A.sum(axis=0)  # Normalize columns to sum to 1
        self.B = np.ones((n_states, n_states, n_actions)) / n_states  # Transition model
        self.C = np.zeros(n_observations)  # Preference over observations
        
        # Initialize beliefs
        self.D = np.ones(n_states) / n_states  # Prior beliefs about initial states
        self.d = np.copy(self.D)  # Posterior beliefs about states
        
        # Initialize teacher model
        self.teacher = TeacherModel(n_states)
        
    def update_beliefs(self, observation):
        # Bayesian belief updating
        likelihood = self.A[observation, :]
        self.d = self.d * likelihood
        self.d /= np.sum(self.d)
    
    def get_action(self, action_probs: np.ndarray) -> int:
        # Select action with highest probability from softmax policy distribution
        return int(np.argmax(action_probs))
    
    def step(self, action):
        # Transition to a new state
        new_state = np.random.choice(self.n_states, p=self.B[:, np.argmax(self.d), action])
        
        # Generate an observation
        observation = np.random.choice(self.n_observations, p=self.A[:, new_state])
        
        # Update teacher's knowledge
        self.teacher.update_knowledge(new_state)
        
        # Update beliefs
        self.update_beliefs(observation)
        
        return observation
    
    def calculate_free_energy(self, action_idx: int):
        # Simplified free energy for a single action index
        expected_states = np.dot(self.B[:, :, action_idx], self.d)
        expected_observations = np.dot(self.A, expected_states)

        free_energy = np.dot(expected_observations, self.C) + \
                      np.sum(expected_states * np.log(expected_states / self.D))

        return -free_energy  # Negative free energy (to be maximized)

    def infer_policy(self, policies):
        # Calculate free energy for each action and return softmax distribution
        F = np.array([self.calculate_free_energy(a) for a in range(self.n_actions)])
        
        # Softmax distribution over policies
        pi = softmax(F)
        
        return pi

    def plot_matrices(self, output_folder='output'):
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Plot A matrix (Likelihood model)
        plt.figure(figsize=(10, 8))
        plt.imshow(self.A, cmap='viridis', aspect='auto')
        plt.colorbar(label='Probability')
        plt.title('A Matrix: Likelihood Model')
        plt.xlabel('States')
        plt.ylabel('Observations')
        plt.savefig(os.path.join(output_folder, 'A_matrix.png'))
        plt.close()

        # Plot B matrix (Transition model)
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

        # Plot C vector (Preference over observations)
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_observations), self.C)
        plt.title('C Vector: Preference over Observations')
        plt.xlabel('Observations')
        plt.ylabel('Preference')
        plt.savefig(os.path.join(output_folder, 'C_vector.png'))
        plt.close()

        # Plot D vector (Prior beliefs about initial states)
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), self.D)
        plt.title('D Vector: Prior Beliefs about Initial States')
        plt.xlabel('States')
        plt.ylabel('Probability')
        plt.savefig(os.path.join(output_folder, 'D_vector.png'))
        plt.close()

    def plot_student_beliefs(self, beliefs, title, output_folder='output'):
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), beliefs)
        plt.title(f"Student's Beliefs: {title}")
        plt.xlabel('States (Aspects of Romantic Prussian Poetry)')
        plt.ylabel('Belief Probability')
        plt.savefig(os.path.join(output_folder, f'student_beliefs_{title.lower().replace(" ", "_")}.png'))
        plt.close()

    def plot_teacher_knowledge(self, title, output_folder='output'):
        knowledge = self.teacher.get_knowledge()
        plt.figure(figsize=(10, 6))
        plt.bar(range(self.n_states), knowledge)
        plt.title(f"Teacher's Knowledge: {title}")
        plt.xlabel('States (Aspects of Romantic Prussian Poetry)')
        plt.ylabel('Knowledge Level')
        plt.savefig(os.path.join(output_folder, f'teacher_knowledge_{title.lower().replace(" ", "_")}.png'))
        plt.close()

if __name__ == '__main__':
    # Example usage
    n_states = 10  # States represent different aspects of Romantic Prussian poetry
    n_observations = 15  # Observations are learning outcomes or experiences
    n_actions = 5  # Actions are learning activities or resource explorations

    pomdp = StudentTeacherPOMDP(n_states, n_observations, n_actions)

    # Plot initial matrices
    pomdp.plot_matrices()

    # Plot initial student beliefs and teacher knowledge
    pomdp.plot_student_beliefs(pomdp.d, "Initial")
    pomdp.plot_teacher_knowledge("Initial")

    # Simulate a few steps
    num_steps = 20
    for step in range(num_steps):
        policies = np.random.rand(pomdp.n_actions)  # Random policies for demonstration
        pi = pomdp.infer_policy(policies)
        action = pomdp.get_action(pi)
        observation = pomdp.step(action)
        print(f"Step {step + 1}: Action: {action}, Observation: {observation}")

        # Teacher suggests a resource based on current student beliefs
        suggested_resource = pomdp.teacher.suggest_resource(pomdp.d)
        print(f"Teacher suggests focusing on aspect: {suggested_resource}")

    # Plot final student beliefs and teacher knowledge
    pomdp.plot_student_beliefs(pomdp.d, "Final")
    pomdp.plot_teacher_knowledge("Final")

    print("Final beliefs:", pomdp.d)
    print("Teacher's knowledge:", pomdp.teacher.get_knowledge())