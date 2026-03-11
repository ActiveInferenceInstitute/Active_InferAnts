// SPDX-License-Identifier: CC-BY-NC-ND-4.0
pragma solidity ^0.8.0;

/**
 * @title Active Inference in Solidity
 * @notice Demonstrates belief updating, free energy minimization, and policy
 *         selection using Solidity's fixed-point arithmetic on-chain.
 * @dev Uses uint256 with 1e18 precision (WAD) for fixed-point math.
 */
contract ActiveInference {
    uint256 constant WAD = 1e18;
    uint256 constant N_STATES = 4;
    uint256 constant N_OBS = 3;
    uint256 constant N_ACTIONS = 2;

    uint256[N_STATES] public beliefs;
    uint256[N_STATES] public prior;
    uint256[N_OBS] public preferences;
    uint256[N_OBS][N_STATES] public A; // A[state][obs] for gas efficiency

    uint256 public step;
    uint256 public lastAction;
    uint256 public lastFreeEnergy;

    event StepCompleted(
        uint256 indexed stepNum,
        uint256 observation,
        uint256 action,
        uint256 freeEnergy,
        uint256[N_STATES] beliefs
    );

    constructor() {
        // Initialize uniform beliefs and prior
        for (uint256 i = 0; i < N_STATES; i++) {
            beliefs[i] = WAD / N_STATES;
            prior[i] = WAD / N_STATES;
        }
        // Initialize preferences (prefer first observation)
        uint256 prefSum = 0;
        for (uint256 i = 0; i < N_OBS; i++) {
            preferences[i] = (i == 0) ? WAD : WAD / 5;
            prefSum += preferences[i];
        }
        for (uint256 i = 0; i < N_OBS; i++)
            preferences[i] = (preferences[i] * WAD) / prefSum;

        // Initialize A matrix with diagonal bias
        for (uint256 s = 0; s < N_STATES; s++) {
            uint256 colSum = 0;
            for (uint256 o = 0; o < N_OBS; o++) {
                A[s][o] = (o == s && s < N_OBS) ? (WAD * 8) / 10 : WAD / N_OBS;
                colSum += A[s][o];
            }
            // Normalize column
            for (uint256 o = 0; o < N_OBS; o++)
                A[s][o] = (A[s][o] * WAD) / colSum;
        }
    }

    function updateBeliefs(uint256 observation) external {
        require(observation < N_OBS, "Invalid observation");
        uint256 total = 0;
        for (uint256 s = 0; s < N_STATES; s++) {
            beliefs[s] = (beliefs[s] * A[s][observation]) / WAD;
            total += beliefs[s];
        }
        require(total > 0, "Beliefs collapsed");
        for (uint256 s = 0; s < N_STATES; s++)
            beliefs[s] = (beliefs[s] * WAD) / total;

        // Calculate free energy (simplified — absolute deviation from prior)
        lastFreeEnergy = 0;
        for (uint256 s = 0; s < N_STATES; s++) {
            if (beliefs[s] > prior[s])
                lastFreeEnergy += beliefs[s] - prior[s];
            else
                lastFreeEnergy += prior[s] - beliefs[s];
        }

        // Select action (deterministic: argmin EFE)
        uint256 bestAction = 0;
        uint256 bestEfe = type(uint256).max;
        for (uint256 a = 0; a < N_ACTIONS; a++) {
            uint256 efe = 0;
            for (uint256 s = 0; s < N_STATES; s++) {
                uint256 predObs = 0;
                for (uint256 o = 0; o < N_OBS; o++)
                    predObs += (A[s][o] * preferences[o]) / WAD;
                efe += (beliefs[s] * (WAD - predObs)) / WAD;
            }
            if (efe < bestEfe) { bestEfe = efe; bestAction = a; }
        }

        lastAction = bestAction;
        step++;

        emit StepCompleted(step, observation, lastAction, lastFreeEnergy, beliefs);
    }

    function getBeliefs() external view returns (uint256[N_STATES] memory) {
        return beliefs;
    }

    function getState() external view returns (
        uint256 currentStep,
        uint256 action,
        uint256 freeEnergy,
        uint256[N_STATES] memory currentBeliefs
    ) {
        return (step, lastAction, lastFreeEnergy, beliefs);
    }
}
