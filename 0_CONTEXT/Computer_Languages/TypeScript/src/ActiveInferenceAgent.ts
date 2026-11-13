import * as math from 'mathjs';
import {
    AgentConfig,
    GenerativeModel,
    BeliefState,
    Action,
    Observation,
    FreeEnergy,
    AgentHistory,
    BeliefUpdateError,
    PolicySelectionError,
    Vector,
    Matrix,
    AgentStatistics
} from './types.js';

/**
 * Extract a readable message from an unknown thrown value.
 */
function describeError(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
}

/**
 * Type-safe Active Inference Agent implementation
 *
 * This class implements the core active inference algorithm with strong typing,
 * comprehensive error handling, and detailed logging for educational purposes.
 */
export class ActiveInferenceAgent {
    private readonly config: AgentConfig;
    private readonly generativeModel: GenerativeModel;
    private beliefState: BeliefState;
    private history: AgentHistory;

    constructor(config: AgentConfig) {
        this.config = this.validateConfig(config);
        this.generativeModel = this.initializeGenerativeModel();
        this.beliefState = this.initializeBeliefState();
        this.history = this.initializeHistory();
    }

    /**
     * Validate agent configuration
     */
    private validateConfig(config: AgentConfig): AgentConfig {
        if (config.nStates < 1) {
            throw new BeliefUpdateError('Number of states must be positive');
        }
        if (config.nObservations < 1) {
            throw new BeliefUpdateError('Number of observations must be positive');
        }
        if (config.nActions < 1) {
            throw new PolicySelectionError('Number of actions must be positive');
        }
        if (config.learningRate <= 0 || config.learningRate > 1) {
            throw new BeliefUpdateError('Learning rate must be in (0, 1]');
        }
        if (config.uncertaintyWeight < 0) {
            throw new BeliefUpdateError('Uncertainty weight must be non-negative');
        }

        return config;
    }

    /**
     * Initialize the generative model (A, B, C, D matrices)
     */
    private initializeGenerativeModel(): GenerativeModel {
        const { nStates, nObservations, nActions } = this.config;

        // Initialize A matrix (Likelihood: p(o|s))
        const A = this.initializeLikelihoodMatrix(nObservations, nStates);

        // Initialize B matrices (Transition: p(s'|s,a))
        const B = this.initializeTransitionMatrices(nStates, nActions);

        // Initialize C vector (Preferences: p(o))
        const C = this.initializePreferenceVector(nObservations);

        // Initialize D vector (Prior beliefs: p(s))
        const D = this.initializePriorVector(nStates);

        return { A, B, C, D };
    }

    /**
     * Initialize likelihood matrix A
     */
    private initializeLikelihoodMatrix(nObservations: number, nStates: number): Matrix {
        const data: number[][] = [];

        for (let obs = 0; obs < nObservations; obs++) {
            const row: number[] = [];
            for (let state = 0; state < nStates; state++) {
                // Simple diagonal structure with noise
                const isDiagonal = obs === state % nObservations;
                const baseProb = isDiagonal ? 0.7 : 0.1;
                const noise = (Math.random() - 0.5) * 0.2;
                row.push(Math.max(0, Math.min(1, baseProb + noise)));
            }
            // Normalize row
            const sum = row.reduce((a, b) => a + b, 0);
            data.push(row.map(x => x / sum));
        }

        return math.matrix(data);
    }

    /**
     * Initialize transition matrices B
     */
    private initializeTransitionMatrices(nStates: number, nActions: number): Matrix[] {
        const matrices: Matrix[] = [];

        for (let action = 0; action < nActions; action++) {
            const data: number[][] = [];

            for (let fromState = 0; fromState < nStates; fromState++) {
                const row: number[] = [];

                for (let toState = 0; toState < nStates; toState++) {
                    let prob = 0.1; // Base probability

                    // Action-specific transition patterns
                    if (action === 0) { // Stay/move left
                        if (toState === fromState) prob = 0.6;
                        else if (toState === Math.max(0, fromState - 1)) prob = 0.3;
                    } else if (action === 1) { // Move right
                        if (toState === Math.min(nStates - 1, fromState + 1)) prob = 0.6;
                        else if (toState === fromState) prob = 0.3;
                    } else { // Random exploration
                        prob = 1.0 / nStates;
                    }

                    row.push(prob);
                }

                // Normalize row
                const sum = row.reduce((a, b) => a + b, 0);
                data.push(row.map(x => x / sum));
            }

            matrices.push(math.matrix(data));
        }

        return matrices;
    }

    /**
     * Initialize preference vector C
     */
    private initializePreferenceVector(nObservations: number): Vector {
        const data: number[] = [];

        for (let obs = 0; obs < nObservations; obs++) {
            // Prefer certain observations (e.g., food, safety)
            const preference = obs < nObservations / 2 ? 1.0 : 0.1;
            data.push(preference);
        }

        return math.matrix([data]);
    }

    /**
     * Initialize prior belief vector D
     */
    private initializePriorVector(nStates: number): Vector {
        const data: number[] = [];
        const uniformProb = 1.0 / nStates;

        for (let state = 0; state < nStates; state++) {
            data.push(uniformProb);
        }

        return math.matrix([data]);
    }

    /**
     * Initialize belief state
     */
    private initializeBeliefState(): BeliefState {
        return {
            current: math.clone(this.generativeModel.D),
            prior: math.clone(this.generativeModel.D),
            posterior: math.clone(this.generativeModel.D)
        };
    }

    /**
     * Initialize history tracking
     */
    private initializeHistory(): AgentHistory {
        return {
            beliefs: [],
            actions: [],
            observations: [],
            freeEnergy: [],
            timestamps: []
        };
    }

    /**
     * Update beliefs given an observation using Bayesian inference
     */
    public updateBeliefs(observation: Observation): Vector {
        try {
            // Get likelihood for this observation
            const likelihood = this.getObservationLikelihood(observation);

            // Bayesian update: posterior = prior * likelihood
            const posterior = math.dotMultiply(this.beliefState.current, likelihood);

            // Normalize
            const sum = math.sum(posterior);
            if (sum === 0) {
                throw new BeliefUpdateError('Invalid likelihood - posterior sums to zero');
            }

            this.beliefState.posterior = math.dotDivide(posterior, sum);
            this.beliefState.current = math.clone(this.beliefState.posterior);

            // Record in history
            this.history.beliefs.push(math.clone(this.beliefState.current));
            this.history.timestamps.push(new Date());

            return math.clone(this.beliefState.current);

        } catch (error) {
            throw new BeliefUpdateError(
                `Failed to update beliefs: ${describeError(error)}`,
                { observation, currentBeliefs: this.beliefState.current.toArray() }
            );
        }
    }

    /**
     * Get likelihood vector for a given observation
     */
    private getObservationLikelihood(observation: Observation): Vector {
        const likelihoodRow = this.generativeModel.A.subset(
            math.index(observation, math.range(0, this.config.nStates))
        );
        return math.matrix([likelihoodRow.toArray()]);
    }

    /**
     * Calculate variational free energy
     */
    public calculateVariationalFreeEnergy(): number {
        // F = E_q[ln q(s) - ln p(o|s)] = -E_q[ln p(o|s)] + E_q[ln q(s)]
        const expectedLikelihood = this.calculateExpectedLikelihood();
        const entropy = this.calculateEntropy(this.beliefState.current);

        return -expectedLikelihood - entropy;
    }

    /**
     * Calculate expected free energy for a given action
     */
    public calculateExpectedFreeEnergy(action: Action): FreeEnergy {
        try {
            // Predict next beliefs
            const predictedBeliefs = this.predictBeliefs(action);

            // Calculate pragmatic value (surprise about preferred observations)
            const pragmaticValue = this.calculatePragmaticValue(predictedBeliefs);

            // Calculate epistemic value (information gain)
            const epistemicValue = this.calculateEpistemicValue(predictedBeliefs);

            // Total EFE
            const expectedFE = pragmaticValue - this.config.uncertaintyWeight * epistemicValue;

            return {
                variational: this.calculateVariationalFreeEnergy(),
                expected: expectedFE,
                pragmatic: pragmaticValue,
                epistemic: epistemicValue
            };

        } catch (error) {
            throw new PolicySelectionError(
                `Failed to calculate expected free energy: ${describeError(error)}`,
                { action }
            );
        }
    }

    /**
     * Predict beliefs after taking an action
     */
    private predictBeliefs(action: Action): Vector {
        const transition = this.generativeModel.B[action];
        if (!transition) {
            throw new PolicySelectionError(`No transition matrix for action ${action}`);
        }
        return math.multiply(this.beliefState.current, transition);
    }

    /**
     * Calculate pragmatic value
     */
    private calculatePragmaticValue(predictedBeliefs: Vector): number {
        let pragmaticValue = 0;

        for (let state = 0; state < this.config.nStates; state++) {
            const stateProb = predictedBeliefs.get([0, state]);
            if (stateProb > 0) {
                // Expected surprise about preferred observations
                for (let obs = 0; obs < this.config.nObservations; obs++) {
                    const obsProb = this.generativeModel.A.get([obs, state]);
                    const preference = this.generativeModel.C.get([0, obs]);
                    pragmaticValue += stateProb * obsProb * preference;
                }
            }
        }

        return pragmaticValue;
    }

    /**
     * Calculate epistemic value (information gain)
     */
    private calculateEpistemicValue(predictedBeliefs: Vector): number {
        return this.calculateEntropy(predictedBeliefs);
    }

    /**
     * Calculate Shannon entropy of belief distribution
     */
    private calculateEntropy(beliefs: Vector): number {
        let entropy = 0;
        const width = beliefs.size()[1];
        if (width === undefined) {
            return 0;
        }

        for (let i = 0; i < width; i++) {
            const prob = math.number(beliefs.get([0, i]));
            if (prob > 0) {
                entropy -= prob * Math.log2(prob);
            }
        }

        return entropy;
    }

    /**
     * Calculate expected likelihood
     */
    private calculateExpectedLikelihood(): number {
        let expectedLikelihood = 0;

        for (let obs = 0; obs < this.config.nObservations; obs++) {
            const likelihood = this.getObservationLikelihood(obs);
            const expectedObsProb = Number(math.sum(math.dotMultiply(this.beliefState.current, likelihood)));
            if (expectedObsProb > 0) {
                expectedLikelihood += expectedObsProb * Math.log(expectedObsProb);
            }
        }

        return expectedLikelihood;
    }

    /**
     * Select the best action by minimizing expected free energy
     */
    public selectAction(): Action {
        try {
            const efes: FreeEnergy[] = [];

            // Calculate EFE for each action
            for (let action = 0; action < this.config.nActions; action++) {
                const efe = this.calculateExpectedFreeEnergy(action);
                efes.push(efe);
            }

            // Select action with minimum expected free energy
            const bestAction = efes.reduce((best, current, index) => {
                const bestEfe = efes[best];
                return bestEfe === undefined || current.expected < bestEfe.expected ? index : best;
            }, 0);

            return bestAction;

        } catch (error) {
            throw new PolicySelectionError(
                `Failed to select action: ${describeError(error)}`,
                { availableActions: this.config.nActions }
            );
        }
    }

    /**
     * Execute one step of the perception-action loop
     */
    public step(observation: Observation): Action {
        // Update beliefs based on observation
        this.updateBeliefs(observation);

        // Calculate free energy
        const fe = this.calculateVariationalFreeEnergy();
        this.history.freeEnergy.push(fe);

        // Select and return action
        const action = this.selectAction();
        this.history.actions.push(action);
        this.history.observations.push(observation);
        this.history.timestamps.push(new Date());

        return action;
    }

    /**
     * Get current belief state
     */
    public getBeliefState(): BeliefState {
        return {
            current: math.clone(this.beliefState.current),
            prior: math.clone(this.beliefState.prior),
            posterior: math.clone(this.beliefState.posterior)
        };
    }

    /**
     * Get agent configuration
     */
    public getConfig(): AgentConfig {
        return { ...this.config };
    }

    /**
     * Get generative model
     */
    public getGenerativeModel(): GenerativeModel {
        return {
            A: math.clone(this.generativeModel.A),
            B: this.generativeModel.B.map(B => math.clone(B)),
            C: math.clone(this.generativeModel.C),
            D: math.clone(this.generativeModel.D)
        };
    }

    /**
     * Get history for analysis
     */
    public getHistory(): AgentHistory {
        return {
            beliefs: [...this.history.beliefs],
            actions: [...this.history.actions],
            observations: [...this.history.observations],
            freeEnergy: [...this.history.freeEnergy],
            timestamps: [...this.history.timestamps]
        };
    }

    /**
     * Reset agent to initial state
     */
    public reset(): void {
        this.beliefState = this.initializeBeliefState();
        this.history = this.initializeHistory();
    }

    /**
     * Get statistics about agent behavior
     */
    public getStatistics(): AgentStatistics {
        if (this.history.actions.length === 0) {
            return { message: 'No actions recorded yet' };
        }

        const actionCounts: Record<number, number> = {};
        this.history.actions.forEach(action => {
            actionCounts[action] = (actionCounts[action] || 0) + 1;
        });

        return {
            totalSteps: this.history.actions.length,
            averageFreeEnergy: this.history.freeEnergy.reduce((a, b) => a + b, 0) / this.history.freeEnergy.length,
            actionDistribution: actionCounts,
            finalBeliefs: Array.from({ length: this.config.nStates }, (_, state) =>
                math.number(this.beliefState.current.get([0, state]))
            ),
            observationDistribution: this.getDistribution(this.history.observations)
        };
    }

    /**
     * Get distribution of values
     */
    private getDistribution(values: number[]): Record<number, number> {
        const distribution: Record<number, number> = {};
        values.forEach(value => {
            distribution[value] = (distribution[value] || 0) + 1;
        });
        return distribution;
    }
}
