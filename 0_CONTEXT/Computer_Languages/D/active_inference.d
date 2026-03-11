/**
 * Active Inference Implementation in D
 *
 * Demonstrates belief updating, free energy minimization, and policy
 * selection using D's metaprogramming and compile-time features.
 */
import std.stdio;
import std.math;
import std.random;
import std.algorithm;
import std.range;
import std.array;
import std.format;

struct ActiveInferenceAgent {
    double[] beliefs;
    double[][] A; // observation model
    double[][] B; // transition model
    double[] C;   // preferences
    double[] D;   // prior
    int nStates;
    int nObs;
    int nActions;
    double precision;

    static ActiveInferenceAgent create(int nStates, int nObs, int nActions) {
        ActiveInferenceAgent agent;
        agent.nStates = nStates;
        agent.nObs = nObs;
        agent.nActions = nActions;
        agent.precision = 1.0;

        // Initialize uniform beliefs
        agent.beliefs = new double[nStates];
        agent.beliefs[] = 1.0 / nStates;

        // Initialize D prior
        agent.D = new double[nStates];
        agent.D[] = 1.0 / nStates;

        // Initialize A matrix (observation likelihood)
        agent.A = new double[][](nObs, nStates);
        foreach (ref row; agent.A)
            row[] = 1.0 / nObs;
        // Bias diagonal
        foreach (i; 0 .. min(nObs, nStates))
            agent.A[i][i] = 0.8;
        // Renormalize columns
        foreach (j; 0 .. nStates) {
            double sum = 0;
            foreach (i; 0 .. nObs) sum += agent.A[i][j];
            foreach (i; 0 .. nObs) agent.A[i][j] /= sum;
        }

        // Initialize B matrix (transition)
        agent.B = new double[][](nStates, nStates);
        foreach (ref row; agent.B)
            row[] = 1.0 / nStates;

        // Initialize C preferences (prefer first observation)
        agent.C = new double[nObs];
        agent.C[0] = 1.0;
        foreach (i; 1 .. nObs) agent.C[i] = 0.2;
        double cSum = agent.C[].sum;
        agent.C[] /= cSum;

        return agent;
    }

    void updateBeliefs(int observation) {
        double[] likelihood = new double[nStates];
        foreach (s; 0 .. nStates)
            likelihood[s] = A[observation][s];

        foreach (s; 0 .. nStates)
            beliefs[s] *= likelihood[s];

        double total = beliefs[].sum;
        if (total > 1e-10)
            beliefs[] /= total;
        else
            beliefs[] = 1.0 / nStates;
    }

    double calculateFreeEnergy() {
        double fe = 0;
        foreach (s; 0 .. nStates) {
            if (beliefs[s] > 1e-10 && D[s] > 1e-10)
                fe += beliefs[s] * log(beliefs[s] / D[s]);
        }
        return fe;
    }

    int selectAction() {
        auto rng = Random(unpredictableSeed);
        double[] efe = new double[nActions];
        foreach (a; 0 .. nActions) {
            // Expected free energy per action
            foreach (s; 0 .. nStates) {
                double predObs = 0;
                foreach (o; 0 .. nObs)
                    predObs += A[o][s] * C[o];
                efe[a] += beliefs[s] * (-predObs);
            }
        }
        // Softmax selection
        double[] probs = new double[nActions];
        double maxEfe = efe[].reduce!max;
        foreach (a; 0 .. nActions)
            probs[a] = exp(-precision * (efe[a] - maxEfe));
        double pSum = probs[].sum;
        probs[] /= pSum;

        double r = uniform(0.0, 1.0, rng);
        double cumulative = 0;
        foreach (a; 0 .. nActions) {
            cumulative += probs[a];
            if (r <= cumulative) return a;
        }
        return nActions - 1;
    }
}

void main() {
    writeln("=== Active Inference in D ===");
    writeln("Belief Updating & Free Energy Minimization\n");

    auto agent = ActiveInferenceAgent.create(4, 3, 2);
    auto rng = Random(42);

    writeln("Initial beliefs: ", agent.beliefs.map!(b => format("%.3f", b)));
    writeln();

    foreach (t; 0 .. 10) {
        int obs = uniform(0, agent.nObs, rng);
        agent.updateBeliefs(obs);
        int action = agent.selectAction();
        double fe = agent.calculateFreeEnergy();

        writefln("Step %2d | Obs: %d | Action: %d | FE: %6.4f | Beliefs: %s",
                 t + 1, obs, action, fe,
                 agent.beliefs.map!(b => format("%.3f", b)));
    }

    writeln("\n✅ D Active Inference simulation complete");
}
