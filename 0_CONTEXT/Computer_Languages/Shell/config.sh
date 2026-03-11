#!/bin/bash

#########################################################################
# Configuration File for Active Inference Simulation in Shell
# This file contains all configurable parameters for the simulation
#########################################################################

# Environment Configuration
export CONFIG_ENVIRONMENT="ShellActiveInference_v1.0"

# Initial Beliefs (probabilities for 4 states)
export CONFIG_INITIAL_BELIEFS="0.25 0.25 0.25 0.25"

# Agent Preferences (desired observations for 3 observation types)
export CONFIG_PREFERENCES="0.7 0.2 0.1"

# Transition Probabilities (state transitions for 2 actions)
export CONFIG_TRANSITION_PROBS="0.8 0.2 0.6 0.4 0.3 0.7 0.9 0.1"

# Simulation Parameters
export CONFIG_TIME_STEPS=15
export CONFIG_PRECISION=1000


#########################################################################
# Validation Functions
#########################################################################

validate_config() {
    # Validate probability arrays
    local beliefs_sum=0
    for belief in ${CONFIG_INITIAL_BELIEFS}; do
        beliefs_sum=$(echo "$beliefs_sum + $belief" | bc -l)
    done

    if (( $(echo "$beliefs_sum < 0.99 || $beliefs_sum > 1.01" | bc -l) )); then
        echo "ERROR: Initial beliefs must sum to 1.0, got $beliefs_sum" >&2
        return 1
    fi

    local prefs_sum=0
    for pref in ${CONFIG_PREFERENCES}; do
        prefs_sum=$(echo "$prefs_sum + $pref" | bc -l)
    done

    if (( $(echo "$prefs_sum < 0.99 || $prefs_sum > 1.01" | bc -l) )); then
        echo "ERROR: Preferences must sum to 1.0, got $prefs_sum" >&2
        return 1
    fi

    # Validate ranges
    if (( CONFIG_TIME_STEPS < 1 || CONFIG_TIME_STEPS > 1000 )); then
        echo "ERROR: Time steps must be between 1 and 1000" >&2
        return 1
    fi

    if (( CONFIG_PRECISION < 1 || CONFIG_PRECISION > 10000 )); then
        echo "ERROR: Precision must be between 1 and 10000" >&2
        return 1
    fi

    return 0
}

# Validate configuration on load
if ! validate_config; then
    echo "Configuration validation failed!" >&2
    exit 1
fi

echo "Configuration loaded and validated successfully"
