/**
 * Tests for Active Inference Agent Implementation
 *
 * Validates core algorithmic correctness:
 * - Agent creation and initialization
 * - Belief update normalization
 * - Action selection bounds
 * - Free energy computation
 * - History tracking and reset
 */

import { ActiveInferenceAgent } from './active_inference.js';

let passed = 0;
let failed = 0;

function assert(condition, message) {
    if (!condition) {
        throw new Error(message);
    }
}

function runTest(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
        passed++;
    } catch (e) {
        console.log(`❌ ${name}: ${e.message}`);
        failed++;
    }
}

// Test 1: Agent creation with default config
runTest('Agent creation with defaults', () => {
    const agent = new ActiveInferenceAgent();
    assert(agent.nStates === 3, `nStates=${agent.nStates}, expected 3`);
    assert(agent.nObservations === 3, `nObservations=${agent.nObservations}, expected 3`);
    assert(agent.nActions === 3, `nActions=${agent.nActions}, expected 3`);
});

// Test 2: Agent creation with custom config
runTest('Agent creation with custom config', () => {
    const agent = new ActiveInferenceAgent({ nStates: 5, nObservations: 4, nActions: 3 });
    assert(agent.nStates === 5, `nStates=${agent.nStates}, expected 5`);
    assert(agent.nObservations === 4, `nObservations=${agent.nObservations}, expected 4`);
});

// Test 3: Belief update produces normalized distribution
runTest('Belief update normalization', () => {
    const agent = new ActiveInferenceAgent();
    agent.updateBeliefs(0);
    const beliefs = agent.getBeliefs();
    // Sum should be approximately 1
    let sum = 0;
    for (let i = 0; i < beliefs.size()[1]; i++) {
        sum += beliefs.get([0, i]);
    }
    assert(Math.abs(sum - 1.0) < 1e-8, `Belief sum=${sum}, expected ~1.0`);
});

// Test 4: Action selection returns valid index
runTest('Action selection returns valid index', () => {
    const agent = new ActiveInferenceAgent();
    agent.updateBeliefs(0);
    const action = agent.selectAction();
    assert(Number.isInteger(action), `Action is not integer: ${action}`);
    assert(action >= 0 && action < agent.nActions, `Action ${action} out of range [0, ${agent.nActions})`);
});

// Test 5: Step returns valid action
runTest('Step returns valid action', () => {
    const agent = new ActiveInferenceAgent();
    const action = agent.step(0);
    assert(Number.isInteger(action), `Step returned non-integer: ${action}`);
    assert(action >= 0 && action < agent.nActions, `Action ${action} out of range`);
});

// Test 6: History tracks observations and actions
runTest('History tracks data', () => {
    const agent = new ActiveInferenceAgent();
    agent.step(0);
    agent.step(1);
    const history = agent.getHistory();
    assert(history.observations.length === 2, `Expected 2 observations, got ${history.observations.length}`);
    assert(history.actions.length === 2, `Expected 2 actions, got ${history.actions.length}`);
    assert(history.freeEnergy.length === 2, `Expected 2 FE values, got ${history.freeEnergy.length}`);
});

// Test 7: Reset clears history
runTest('Reset clears history', () => {
    const agent = new ActiveInferenceAgent();
    agent.step(0);
    agent.step(1);
    agent.reset();
    const history = agent.getHistory();
    assert(history.observations.length === 0, 'Observations not cleared');
    assert(history.actions.length === 0, 'Actions not cleared');
});

// Test 8: Free energy is finite
runTest('Free energy is finite', () => {
    const agent = new ActiveInferenceAgent();
    agent.updateBeliefs(0);
    const fe = agent.calculateVariationalFreeEnergy();
    assert(Number.isFinite(fe), `Free energy is not finite: ${fe}`);
});

// Test 9: Expected free energy is finite for all actions
runTest('Expected free energy finite for all actions', () => {
    const agent = new ActiveInferenceAgent();
    for (let action = 0; action < agent.nActions; action++) {
        const efe = agent.calculateExpectedFreeEnergy(action);
        assert(Number.isFinite(efe), `EFE for action ${action} is not finite: ${efe}`);
    }
});

// Test 10: Multiple steps do not crash
runTest('Multiple simulation steps', () => {
    const agent = new ActiveInferenceAgent();
    for (let i = 0; i < 20; i++) {
        const obs = i % agent.nObservations;
        agent.step(obs);
    }
    const history = agent.getHistory();
    assert(history.actions.length === 20, `Expected 20 actions, got ${history.actions.length}`);
});

// Summary
console.log(`\n${'='.repeat(50)}`);
console.log(`Results: ${passed} passed, ${failed} failed, ${passed + failed} total`);
if (failed === 0) {
    console.log('✅ All tests passed!');
} else {
    console.log('❌ Some tests failed!');
    process.exit(1);
}
