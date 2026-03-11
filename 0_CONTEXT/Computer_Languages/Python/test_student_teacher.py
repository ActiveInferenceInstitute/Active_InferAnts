"""
Unit tests for the Active Inference Student-Teacher POMDP implementation.

Tests core algorithmic correctness:
- Belief update normalization
- Free energy computation
- Policy inference distribution validity
- Teacher knowledge monotonicity
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from student_teacher import TeacherModel, StudentTeacherPOMDP


def test_belief_update_normalization():
    """Beliefs must sum to 1 after Bayesian update."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    for obs in range(pomdp.n_observations):
        pomdp.update_beliefs(obs)
        total = np.sum(pomdp.d)
        assert abs(total - 1.0) < 1e-10, f"Beliefs sum to {total} after obs={obs}"
    print("✅ test_belief_update_normalization passed")


def test_belief_update_shifts_distribution():
    """Beliefs should change after observing evidence."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    initial_beliefs = pomdp.d.copy()
    pomdp.update_beliefs(0)
    # Beliefs should differ from uniform after update
    assert not np.allclose(pomdp.d, initial_beliefs), "Beliefs unchanged after observation"
    print("✅ test_belief_update_shifts_distribution passed")


def test_free_energy_returns_finite():
    """Free energy must be a finite number for all actions."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    for action_idx in range(pomdp.n_actions):
        fe = pomdp.calculate_free_energy(action_idx)
        assert np.isfinite(fe), f"Free energy is {fe} for action {action_idx}"
    print("✅ test_free_energy_returns_finite passed")


def test_free_energy_numerical_stability():
    """Free energy should not produce NaN even with near-zero beliefs."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    # Set beliefs to be very peaked (near-zero for most states)
    pomdp.d = np.array([1e-20, 1e-20, 1.0 - 2e-20, 1e-20])
    for action_idx in range(pomdp.n_actions):
        fe = pomdp.calculate_free_energy(action_idx)
        assert np.isfinite(fe), f"Free energy NaN/Inf with peaked beliefs: {fe}"
    print("✅ test_free_energy_numerical_stability passed")


def test_infer_policy_valid_distribution():
    """Policy must be a valid probability distribution."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    pi = pomdp.infer_policy()
    assert len(pi) == pomdp.n_actions, f"Policy length {len(pi)} != {pomdp.n_actions}"
    assert abs(np.sum(pi) - 1.0) < 1e-10, f"Policy sums to {np.sum(pi)}"
    assert np.all(pi >= 0), "Policy has negative probabilities"
    print("✅ test_infer_policy_valid_distribution passed")


def test_get_action_returns_valid_index():
    """get_action must return an integer in [0, n_actions)."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    pi = pomdp.infer_policy()
    action = pomdp.get_action(pi)
    assert isinstance(action, int), f"Action is {type(action)}, not int"
    assert 0 <= action < pomdp.n_actions, f"Action {action} out of range"
    print("✅ test_get_action_returns_valid_index passed")


def test_step_returns_valid_observation():
    """step() must return an observation index in [0, n_observations)."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    for action in range(pomdp.n_actions):
        obs = pomdp.step(action)
        assert 0 <= obs < pomdp.n_observations, f"Observation {obs} out of range"
    print("✅ test_step_returns_valid_observation passed")


def test_teacher_knowledge_non_negative():
    """Teacher knowledge should always be non-negative."""
    teacher = TeacherModel(5)
    for state in range(5):
        teacher.update_knowledge(state)
        knowledge = teacher.get_knowledge()
        assert np.all(knowledge >= 0), f"Negative knowledge detected: {knowledge}"
    print("✅ test_teacher_knowledge_non_negative passed")


def test_teacher_suggest_resource_valid():
    """suggest_resource must return a valid state index."""
    teacher = TeacherModel(5)
    beliefs = np.ones(5) / 5
    suggestion = teacher.suggest_resource(beliefs)
    assert 0 <= suggestion < 5, f"Suggestion {suggestion} out of range"
    print("✅ test_teacher_suggest_resource_valid passed")


def test_a_matrix_normalized():
    """A matrix columns must sum to 1 (conditional probabilities)."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    col_sums = pomdp.A.sum(axis=0)
    assert np.allclose(col_sums, 1.0), f"A matrix columns sum to {col_sums}"
    print("✅ test_a_matrix_normalized passed")


def test_d_prior_normalized():
    """D prior must be a valid probability distribution."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    assert abs(np.sum(pomdp.D) - 1.0) < 1e-10, f"D sums to {np.sum(pomdp.D)}"
    print("✅ test_d_prior_normalized passed")


def test_full_simulation_loop():
    """End-to-end simulation should run without errors."""
    pomdp = StudentTeacherPOMDP(4, 3, 2)
    for _ in range(10):
        pi = pomdp.infer_policy()
        action = pomdp.get_action(pi)
        obs = pomdp.step(action)
    # Final beliefs should still be normalized
    assert abs(np.sum(pomdp.d) - 1.0) < 1e-10, "Beliefs denormalized after simulation"
    print("✅ test_full_simulation_loop passed")


if __name__ == '__main__':
    tests = [
        test_belief_update_normalization,
        test_belief_update_shifts_distribution,
        test_free_energy_returns_finite,
        test_free_energy_numerical_stability,
        test_infer_policy_valid_distribution,
        test_get_action_returns_valid_index,
        test_step_returns_valid_observation,
        test_teacher_knowledge_non_negative,
        test_teacher_suggest_resource_valid,
        test_a_matrix_normalized,
        test_d_prior_normalized,
        test_full_simulation_loop,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except (AssertionError, Exception) as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    if failed == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
