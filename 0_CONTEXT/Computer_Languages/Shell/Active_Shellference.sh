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

#########################################################################
# Initialize simulation parameters
# Sets up the simulation environment, initial beliefs, preferences,
# transition probabilities, time steps, and precision based on the
# configuration provided in config.sh.
#########################################################################
initialize_simulation() {
    simulation[environment]="${CONFIG_ENVIRONMENT}"
    simulation[beliefs]="${CONFIG_INITIAL_BELIEFS}"
    simulation[preferences]="${CONFIG_PREFERENCES}"
    simulation[transition_probs]="${CONFIG_TRANSITION_PROBS}"
    time_steps="${CONFIG_TIME_STEPS}"
    precision="${CONFIG_PRECISION}"
}

#########################################################################
# Calculate Kullback-Leibler Divergence
# Computes the KL divergence between the agent's current beliefs and
# its preferences.
# Arguments:
#   $1 - Name reference to the beliefs array
#   $2 - Name reference to the preferences array
# Returns:
#   The calculated KL divergence value
#########################################################################
calculate_kl_divergence() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local kl_divergence=0

    for i in "${!beliefs_ref[@]}"; do
        local belief=${beliefs_ref[$i]}
        local preference=${preferences_ref[$i]}
        kl_divergence=$(echo "scale=$precision; $kl_divergence + $belief * (l($belief) - l($preference))" | bc -l)
    done

    echo "$kl_divergence"
}

#########################################################################
# Calculate Variational Free Energy
# Computes the Variational Free Energy based on current beliefs and preferences.
# Arguments:
#   $1 - Name reference to the beliefs array
#   $2 - Name reference to the preferences array
# Returns:
#   The calculated Variational Free Energy
#########################################################################
calculate_vfe() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local vfe

    vfe=$(calculate_kl_divergence beliefs_ref preferences_ref)
    echo "$vfe"
}

#########################################################################
# Calculate Expected Free Energy
# Computes the Expected Free Energy based on beliefs, preferences,
# and transition probabilities.
# Arguments:
#   $1 - Name reference to the beliefs array
#   $2 - Name reference to the preferences array
#   $3 - Name reference to the transition_probs array
# Returns:
#   The calculated Expected Free Energy
#########################################################################
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
            expected_surprise=$(echo "scale=$precision; $expected_surprise + ${transition_probs_ref[$idx]} * (${preferences_ref[$j]} - l(${beliefs_ref[$i]}))" | bc -l)
        done
        efe=$(echo "scale=$precision; $efe + ${beliefs_ref[$i]} * $expected_surprise" | bc -l)
    done

    echo "$efe"
}

#########################################################################
# Update Beliefs
# Updates the agent's beliefs based on current beliefs, preferences,
# and transition probabilities. Normalizes the updated beliefs to ensure
# they sum to 1.
# Arguments:
#   $1 - Name reference to the current_beliefs array
#   $2 - Name reference to the current_preferences array
#   $3 - Name reference to the current_transition_probs array
# Returns:
#   A space-separated string of updated beliefs
#########################################################################
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
            posterior=$(echo "scale=$precision; $posterior + ${beliefs_ref[$i]} * ${transition_probs_ref[$idx]}" | bc -l)
        done
        posterior=$(echo "scale=$precision; $posterior * ${preferences_ref[$i]}" | bc -l)
        updated_beliefs+=("$posterior")
    done

    # Normalize the beliefs
    local total_belief
    total_belief=$(IFS=+; echo "scale=$precision; ${updated_beliefs[*]}" | bc -l)

    for i in "${!updated_beliefs[@]}"; do
        updated_beliefs[$i]=$(echo "scale=$precision; ${updated_beliefs[$i]} / $total_belief" | bc -l)
    done

    echo "${updated_beliefs[*]}"
}

#########################################################################
# Select Action Based on Expected Free Energy
# Chooses the action that minimizes the Expected Free Energy.
# Arguments:
#   $1 - Name reference to the current_beliefs array
#   $2 - Name reference to the current_preferences array
#   $3 - Name reference to the current_transition_probs array
#   $4 - Name reference to the environment array
# Returns:
#   The selected action with the lowest Expected Free Energy
#########################################################################
select_action() {
    local -n beliefs_ref=$1
    local -n preferences_ref=$2
    local -n transition_probs_ref=$3
    local -n environment_ref=$4
    local min_efe=1000000
    local selected_action=""

    for action in "${environment_ref[@]}"; do
        local efe
        efe=$(calculate_efe beliefs_ref preferences_ref transition_probs_ref)
        if (( $(echo "$efe < $min_efe" | bc -l) )); then
            min_efe=$efe
            selected_action=$action
        fi
    done

    echo "$selected_action"
}

#########################################################################
# Run Simulation
# Executes the main simulation loop for the specified number of time steps.
# Initializes the simulation, updates beliefs, calculates free energies,
# and selects actions at each step.
#########################################################################
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
        vfe=$(calculate_vfe beliefs preferences)
        echo "Variational Free Energy: $vfe"

        # Select action based on Expected Free Energy
        local selected_action
        selected_action=$(select_action beliefs preferences transition_probs environment)
        echo "Selected Action: $selected_action"

        # TODO: Implement action effects on environment

        echo "--------------------------------------"
    done

    echo "Simulation completed"
}

# Execute the simulation
run_simulation

# TODO: Add error handling, logging, and command-line argument parsing for more robustness
