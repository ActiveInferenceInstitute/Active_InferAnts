/**
 * Type definitions for Active Inference implementation
 */

// Mathematical types
export type Matrix = math.Matrix;
export type Vector = math.Matrix;
export type Scalar = number;

// Agent configuration types
export interface AgentConfig {
    readonly nStates: number;
    readonly nObservations: number;
    readonly nActions: number;
    readonly learningRate: number;
    readonly uncertaintyWeight: number;
    readonly precision: number;
}

// Generative model components
export interface GenerativeModel {
    readonly A: Matrix;  // Likelihood: p(o|s)
    readonly B: Matrix[]; // Transition: p(s'|s,a)
    readonly C: Vector;  // Preferences: p(o)
    readonly D: Vector;  // Prior beliefs: p(s)
}

// Belief state
export interface BeliefState {
    readonly current: Vector;
    readonly prior: Vector;
    readonly posterior: Vector;
}

// Action and observation types
export type Action = number;
export type Observation = number;
export type State = number;

// Free energy components
export interface FreeEnergy {
    readonly variational: number;
    readonly expected: number;
    readonly pragmatic: number;
    readonly epistemic: number;
}

// Agent history for analysis
export interface AgentHistory {
    readonly beliefs: Vector[];
    readonly actions: Action[];
    readonly observations: Observation[];
    readonly freeEnergy: number[];
    readonly timestamps: Date[];
}

// Environment types
export interface Position {
    readonly x: number;
    readonly y: number;
}

export interface PheromoneLevels {
    home: number;
    food: number;
}

export interface GridCell {
    food: number;
    obstacle: boolean;
    pheromones: PheromoneLevels;
}

export interface AntAgent {
    readonly id: number;
    position: Position;
    agent: ActiveInferenceAgent;
    carryingFood: boolean;
    energy: number;
}

// Environment configuration
export interface EnvironmentConfig {
    readonly gridSize: number;
    readonly nAnts: number;
    readonly foodSources: number;
    readonly pheromoneDecay: number;
    readonly maxSteps: number;
}

// Simulation results
export interface SimulationStep {
    readonly step: number;
    readonly totalPheromones: number;
    readonly foodCollected: number;
    readonly antPositions: Position[];
    readonly averageFreeEnergy: number;
    readonly timestamp: Date;
}

export interface SimulationResults {
    readonly steps: SimulationStep[];
    readonly finalState: EnvironmentState;
    readonly totalTime: number;
    readonly convergence: boolean;
}

export interface EnvironmentState {
    readonly grid: GridCell[][];
    readonly ants: ReadonlyArray<AntAgent>;
    readonly foodLocations: ReadonlyArray<Position>;
    readonly pheromoneGrid: PheromoneLevels[][];
}

// Error types
export class ActiveInferenceError extends Error {
    constructor(
        message: string,
        public readonly code: string,
        public readonly context?: Record<string, any>
    ) {
        super(message);
        this.name = 'ActiveInferenceError';
    }
}

export class BeliefUpdateError extends ActiveInferenceError {
    constructor(message: string, context?: Record<string, any>) {
        super(message, 'BELIEF_UPDATE_ERROR', context);
    }
}

export class PolicySelectionError extends ActiveInferenceError {
    constructor(message: string, context?: Record<string, any>) {
        super(message, 'POLICY_SELECTION_ERROR', context);
    }
}

// Utility types for type-safe operations
export type ReadonlyMatrix = Readonly<math.Matrix>;
export type ReadonlyVector = Readonly<math.Matrix>;

// Import mathjs for type augmentation
import * as math from 'mathjs';

// Augment mathjs types for better TypeScript support
declare module 'mathjs' {
    export interface Matrix {
        readonly size: readonly number[];
        get(index: readonly number[]): number;
        set(index: readonly number[], value: number): void;
        clone(): Matrix;
        toArray(): any[];
    }
}
