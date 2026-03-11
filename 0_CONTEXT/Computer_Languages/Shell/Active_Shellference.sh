#!/bin/bash

#########################################################################
# Active Inference Simulation in Shell
# This script simulates an active inference process, demonstrating how an
# agent updates its beliefs and selects actions based on the Free Energy
# Principle.
#########################################################################

# Load configuration from script-relative path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! source "${SCRIPT_DIR}/config.sh"; then
    echo "Error: Failed to source config.sh" >&2
    exit 1
fi

# Define global variables
declare -A simulation
declare -i time_steps
declare -i precision

# Load CONFIG_* values into simulation associative array and scalar variables.
initialize_simulation() {
    simulation[environment]="${CONFIG_ENVIRONMENT}"
    simulation[beliefs]="${CONFIG_INITIAL_BELIEFS}"
    simulation[preferences]="${CONFIG_PREFERENCES}"
    simulation[transition_probs]="${CONFIG_TRANSITION_PROBS}"
    time_steps="${CONFIG_TIME_STEPS}"
    precision="${CONFIG_PRECISION}"
}

# KL divergence: sum of belief_i * log(belief_i / preference_i) across states.
calculate_kl_divergence() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local kl_divergence=0

    for i in "${!beliefs_ref[@]}"; do
        local belief=${beliefs_ref[$i]}
        local preference=${preferences_ref[$i]}
        local term
        term=$(echo "scale=$precision; $kl_divergence + $belief * (l($belief) - l($preference))" | bc -l)
        if [ -z "$term" ]; then
            echo "ERROR: KL divergence computation failed at index $i" >&2
            return 1
        fi
        kl_divergence=$term
    done

    echo "$kl_divergence"
}

# Expected free energy: sum over states of belief_i * expected_surprise_i,
# where expected_surprise uses transition probs and log-preferences.
calculate_efe() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local -n transition_probs_ref=$3
    local efe=0
    local env_size=${#beliefs_ref[@]}

    for i in "${!beliefs_ref[@]}"; do
        local expected_surprise=0
        for j in "${!beliefs_ref[@]}"; do
            local idx=$((i * env_size + j))
            local term
            term=$(echo "scale=$precision; $expected_surprise + ${transition_probs_ref[$idx]} * (${preferences_ref[$j]} - l(${beliefs_ref[$i]}))" | bc -l)
            if [ -z "$term" ]; then
                echo "ERROR: EFE inner computation failed at [$i,$j]" >&2
                return 1
            fi
            expected_surprise=$term
        done
        local efe_term
        efe_term=$(echo "scale=$precision; $efe + ${beliefs_ref[$i]} * $expected_surprise" | bc -l)
        if [ -z "$efe_term" ]; then
            echo "ERROR: EFE outer computation failed at state $i" >&2
            return 1
        fi
        efe=$efe_term
    done

    echo "$efe"
}

# Bayes update: new_belief_i = sum_j(belief_j * T[j,i]) * preference_i, then normalize.
update_beliefs() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local -n transition_probs_ref=$3
    local env_size=${#beliefs_ref[@]}
    local updated_beliefs=()

    for i in "${!beliefs_ref[@]}"; do
        local posterior=0
        for j in "${!beliefs_ref[@]}"; do
            local idx=$((i * env_size + j))
            local inner_term
            inner_term=$(echo "scale=$precision; $posterior + ${beliefs_ref[$i]} * ${transition_probs_ref[$idx]}" | bc -l)
            if [ -z "$inner_term" ]; then
                echo "ERROR: update_beliefs inner computation failed at [$i,$j]" >&2
                return 1
            fi
            posterior=$inner_term
        done
        local outer_term
        outer_term=$(echo "scale=$precision; $posterior * ${preferences_ref[$i]}" | bc -l)
        if [ -z "$outer_term" ]; then
            echo "ERROR: update_beliefs outer computation failed at state $i" >&2
            return 1
        fi
        updated_beliefs+=("$outer_term")
    done

    # Normalize the beliefs
    local total_belief
    total_belief=$(IFS=+; echo "scale=$precision; ${updated_beliefs[*]}" | bc -l)
    if [ -z "$total_belief" ] || [ "$total_belief" = "0" ]; then
        echo "ERROR: update_beliefs normalization failed (zero or empty total)" >&2
        return 1
    fi

    for i in "${!updated_beliefs[@]}"; do
        updated_beliefs[$i]=$(echo "scale=$precision; ${updated_beliefs[$i]} / $total_belief" | bc -l)
    done

    echo "${updated_beliefs[*]}"
}

# Pick action minimizing EFE; each action uses its own transition-prob slice.
select_action() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local -n transition_probs_ref=$3
    local -n environment_ref=$4
    local min_efe=1000000  # Sentinel: larger than any realistic EFE for this simulation
    local selected_action=""
    local env_size=${#beliefs_ref[@]}
    local action_idx=0

    for action in "${environment_ref[@]}"; do
        # Extract transition probs for this action (offset = action_idx * env_size^2)
        local action_offset=$(( action_idx * env_size * env_size ))
        local action_trans=()
        for k in $(seq 0 $(( env_size * env_size - 1 ))); do
            action_trans+=("${transition_probs_ref[$((action_offset + k))]}")
        done

        local efe
        efe=$(calculate_efe beliefs_ref preferences_ref action_trans)
        if (( $(echo "$efe < $min_efe" | bc -l) )); then
            min_efe=$efe
            selected_action=$action
        fi
        (( action_idx++ )) || true
    done

    echo "$selected_action"
}

# Main loop: update beliefs, compute VFE, select action at each time step.
run_simulation() {
    initialize_simulation

    echo "Starting Active Inference Simulation"
    echo "======================================"

    for ((t=1; t<=time_steps; t++)); do
        echo "Time step: $t"

        # Convert space-separated strings to arrays
        read -ra beliefs <<< "${simulation[beliefs]}"
        read -ra environment <<< "${simulation[environment]}"
        read -ra preferences <<< "${simulation[preferences]}"
        read -ra transition_probs <<< "${simulation[transition_probs]}"

        # Update beliefs based on current state
        local updated_beliefs
        updated_beliefs=$(update_beliefs beliefs preferences transition_probs)
        simulation[beliefs]="$updated_beliefs"

        # Calculate Variational Free Energy
        local vfe
        vfe=$(calculate_kl_divergence beliefs preferences)
        echo "Variational Free Energy: $vfe"

        # Select action based on Expected Free Energy
        local selected_action
        selected_action=$(select_action beliefs preferences transition_probs environment)
        echo "Selected Action: $selected_action"

        echo "--------------------------------------"
    done

    echo "Simulation completed"
}

# Execute the simulation
run_simulation
