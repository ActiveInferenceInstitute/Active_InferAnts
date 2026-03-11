package main

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"
)

// State represents the possible states of the agent.
type State string

// Observation represents the possible observations an agent can make.
type Observation string

// Constants defining agent states for type safety and clarity.
const (
	StateSearching  State = "searching"
	StateForaging   State = "foraging"
	StateReturning  State = "returning"
	StateResting    State = "resting"
	StateRecruiting State = "recruiting"

	ObservationFood      Observation = "food_found"
	ObservationNest      Observation = "nest_sighted"
	ObservationNone      Observation = "nothing"
	ObservationDanger    Observation = "danger"
	ObservationPheromone Observation = "pheromone"
)

// StateTransition encapsulates the transition and observation probabilities for a state.
type StateTransition struct {
	Transitions  map[State]float64
	Observations map[Observation]float64
}

// Probabilities defines the state transitions and observations for each state.
var probabilities = map[State]StateTransition{
	StateSearching: {
		Transitions: map[State]float64{
			StateForaging:  0.3,
			StateReturning: 0.1,
			StateSearching: 0.6,
		},
		Observations: map[Observation]float64{
			ObservationFood: 0.2,
			ObservationNest: 0.1,
			ObservationNone: 0.7,
		},
	},
	StateForaging: {
		Transitions: map[State]float64{
			StateForaging:  0.5, // Corrected from State(0.5) to float64
			StateReturning: 0.4, // Corrected from State(0.4) to float64
			StateSearching: 0.1, // Corrected from State(0.1) to float64
		},
		Observations: map[Observation]float64{
			ObservationFood: 0.6,
			ObservationNest: 0.1,
			ObservationNone: 0.3,
		},
	},
	StateReturning: {
		Transitions: map[State]float64{
			StateForaging:  0.2,
			StateReturning: 0.7,
			StateSearching: 0.1,
		},
		Observations: map[Observation]float64{
			ObservationFood: 0.1,
			ObservationNest: 0.8,
			ObservationNone: 0.1,
		},
	},
	StateResting: {
		Transitions: map[State]float64{
			StateRecruiting: 0.5,
			StateResting:    0.5,
		},
		Observations: map[Observation]float64{
			ObservationNone: 1.0,
		},
	},
	StateRecruiting: {
		Transitions: map[State]float64{
			StateResting:    0.5,
			StateRecruiting: 0.5,
		},
		Observations: map[Observation]float64{
			ObservationNone: 1.0,
		},
	},
}

// AgentConfig holds configuration parameters for the agent
type AgentConfig struct {
	InitialState    State
	SimulationSteps int
	TransitionNoise float64
	RestProbability float64
}

// DefaultConfig returns default configuration values
func DefaultConfig() AgentConfig {
	return AgentConfig{
		InitialState:    StateSearching,
		SimulationSteps: 10,
		TransitionNoise: 0.1,
		RestProbability: 0.2,
	}
}

// Metrics tracks agent behavior statistics
type Metrics struct {
	StateTransitions  map[State]int
	ObservationCounts map[Observation]int
	TimeInStates      map[State]time.Duration
	mu                sync.Mutex
}

// ActiveInferenceAgent represents an agent with a current state and metrics
type ActiveInferenceAgent struct {
	currentState State
	config       AgentConfig
	metrics      *Metrics
	startTime    time.Time
	logger       *log.Logger
}

// NewActiveInferenceAgent initializes an agent with the given configuration
func NewActiveInferenceAgent(config AgentConfig, logger *log.Logger) (*ActiveInferenceAgent, error) {
	if _, exists := probabilities[config.InitialState]; !exists {
		return nil, fmt.Errorf("invalid initial state: %s", config.InitialState)
	}

	metrics := &Metrics{
		StateTransitions:  make(map[State]int),
		ObservationCounts: make(map[Observation]int),
		TimeInStates:      make(map[State]time.Duration),
	}

	return &ActiveInferenceAgent{
		currentState: config.InitialState,
		config:       config,
		metrics:      metrics,
		startTime:    time.Now(),
		logger:       logger,
	}, nil
}

// SimulationResult contains the final metrics from a simulation run
type SimulationResult struct {
	FinalState     State
	Metrics        Metrics
	TotalDuration  time.Duration
	CompletedSteps int
	Errors         []error
}

// simulateAntBehavior now returns results and accepts context for cancellation
func simulateAntBehavior(ctx context.Context, config AgentConfig, resultChan chan<- SimulationResult) {
	logger := log.New(log.Writer(), "[ANT-AGENT] ", log.LstdFlags)

	agent, err := NewActiveInferenceAgent(config, logger)
	if err != nil {
		logger.Printf("Failed to initialize agent: %v", err)
		resultChan <- SimulationResult{Errors: []error{err}}
		return
	}

	result := SimulationResult{
		CompletedSteps: 0,
		Errors:         make([]error, 0),
	}

	for i := 0; i < config.SimulationSteps; i++ {
		select {
		case <-ctx.Done():
			logger.Println("Simulation cancelled")
			result.Errors = append(result.Errors, ctx.Err())
			resultChan <- result
			return
		default:
			if err := agent.simulateStep(&result); err != nil {
				logger.Printf("Error in simulation step %d: %v", i, err)
				result.Errors = append(result.Errors, err)
				resultChan <- result
				return
			}
			result.CompletedSteps++
		}
	}

	result.FinalState = agent.currentState
	result.TotalDuration = time.Since(agent.startTime)
	agent.metrics.mu.Lock()
	result.Metrics = *agent.metrics
	agent.metrics.mu.Unlock()

	resultChan <- result
}

func main() {
	// rand.Seed is deprecated since Go 1.20; global rand auto-seeds with random value

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	config := DefaultConfig()
	resultChan := make(chan SimulationResult, 1)

	go simulateAntBehavior(ctx, config, resultChan)

	result := <-resultChan
	if len(result.Errors) > 0 {
		log.Printf("Simulation completed with errors: %v", result.Errors)
	}

	// Print simulation results
	fmt.Printf("Simulation completed:\n")
	fmt.Printf("Steps completed: %d\n", result.CompletedSteps)
	fmt.Printf("Final state: %s\n", result.FinalState)
	fmt.Printf("Total duration: %v\n", result.TotalDuration)

	// Print metrics
	fmt.Println("\nMetrics:")
	for state, count := range result.Metrics.StateTransitions {
		fmt.Printf("State %s transitions: %d\n", state, count)
	}
	for obs, count := range result.Metrics.ObservationCounts {
		fmt.Printf("Observation %s count: %d\n", obs, count)
	}
}
