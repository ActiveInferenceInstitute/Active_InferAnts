import { ActiveInferenceAgent } from './ActiveInferenceAgent.js';
import { AgentConfig, BeliefUpdateError, PolicySelectionError } from './types.js';

const config: AgentConfig = {
    nStates: 4,
    nObservations: 3,
    nActions: 4,
    learningRate: 0.1,
    uncertaintyWeight: 0.2,
    precision: 1.0
};

describe('ActiveInferenceAgent', () => {
    it('normalizes posterior beliefs after an observation', () => {
        const agent = new ActiveInferenceAgent(config);

        const beliefs = agent.updateBeliefs(1);
        const row = beliefs.toArray()[0] as number[];

        expect(row).toHaveLength(config.nStates);
        expect(row.every(probability => probability >= 0)).toBe(true);
        expect(row.reduce((total, probability) => total + probability, 0)).toBeCloseTo(1, 10);
    });

    it('records a full perception-action step with an in-range action', () => {
        const agent = new ActiveInferenceAgent(config);

        const action = agent.step(2);
        const history = agent.getHistory();
        const statistics = agent.getStatistics();

        expect(action).toBeGreaterThanOrEqual(0);
        expect(action).toBeLessThan(config.nActions);
        expect(history.actions).toEqual([action]);
        expect(history.observations).toEqual([2]);
        expect(history.beliefs).toHaveLength(1);
        expect(statistics.totalSteps).toBe(1);
    });

    it('reports finite free energy components', () => {
        const agent = new ActiveInferenceAgent(config);
        agent.step(0);

        const expectedFreeEnergy = agent.calculateExpectedFreeEnergy(1);

        expect(Number.isFinite(agent.calculateVariationalFreeEnergy())).toBe(true);
        expect(Number.isFinite(expectedFreeEnergy.expected)).toBe(true);
        expect(Number.isFinite(expectedFreeEnergy.pragmatic)).toBe(true);
        expect(Number.isFinite(expectedFreeEnergy.epistemic)).toBe(true);
    });

    it('rejects invalid state and action counts', () => {
        expect(() => new ActiveInferenceAgent({ ...config, nStates: 0 })).toThrow(BeliefUpdateError);
        expect(() => new ActiveInferenceAgent({ ...config, nActions: 0 })).toThrow(PolicySelectionError);
    });
});
