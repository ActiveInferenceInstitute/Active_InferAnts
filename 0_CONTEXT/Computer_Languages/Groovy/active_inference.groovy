/**
 * Active Inference Implementation in Groovy
 *
 * Demonstrates belief updating, free energy minimization, and policy
 * selection using Groovy's dynamic features and GDK enhancements.
 */

class ActiveInferenceAgent {
    int nStates, nObs, nActions
    double precision = 1.0
    double[] beliefs
    double[][] A, B
    double[] C, D
    Random rng

    ActiveInferenceAgent(int nStates, int nObs, int nActions, long seed = 42) {
        this.nStates = nStates
        this.nObs = nObs
        this.nActions = nActions
        this.rng = new Random(seed)

        beliefs = new double[nStates]
        Arrays.fill(beliefs, 1.0 / nStates)
        D = new double[nStates]
        Arrays.fill(D, 1.0 / nStates)

        // Observation model with diagonal bias
        A = new double[nObs][nStates]
        for (int i = 0; i < nObs; i++)
            Arrays.fill(A[i], 1.0 / nObs)
        for (int i = 0; i < Math.min(nObs, nStates); i++)
            A[i][i] = 0.8
        normalizeColumns(A)

        // Transition model
        B = new double[nStates][nStates]
        for (int i = 0; i < nStates; i++)
            Arrays.fill(B[i], 1.0 / nStates)

        // Preferences
        C = new double[nObs]
        C[0] = 1.0
        for (int i = 1; i < nObs; i++) C[i] = 0.2
        normalize(C)
    }

    void normalize(double[] v) {
        double s = v.sum()
        if (s > 1e-10) for (int i = 0; i < v.length; i++) v[i] /= s
    }

    void normalizeColumns(double[][] m) {
        for (int j = 0; j < m[0].length; j++) {
            double s = (0..<m.length).collect { m[it][j] }.sum()
            if (s > 1e-10) for (int i = 0; i < m.length; i++) m[i][j] /= s
        }
    }

    void updateBeliefs(int observation) {
        for (int s = 0; s < nStates; s++)
            beliefs[s] *= A[observation][s]
        normalize(beliefs)
    }

    double calculateFreeEnergy() {
        double fe = 0
        for (int s = 0; s < nStates; s++)
            if (beliefs[s] > 1e-10 && D[s] > 1e-10)
                fe += beliefs[s] * Math.log(beliefs[s] / D[s])
        return fe
    }

    int selectAction() {
        double[] efe = new double[nActions]
        for (int a = 0; a < nActions; a++)
            for (int s = 0; s < nStates; s++) {
                double predObs = (0..<nObs).collect { A[it][s] * C[it] }.sum()
                efe[a] += beliefs[s] * (-predObs)
            }
        // Softmax
        double maxE = efe.max()
        double[] probs = efe.collect { Math.exp(-precision * (it - maxE)) } as double[]
        normalize(probs)

        double r = rng.nextDouble()
        double cum = 0
        for (int a = 0; a < nActions; a++) {
            cum += probs[a]
            if (r <= cum) return a
        }
        return nActions - 1
    }

    String beliefsStr() { beliefs.collect { String.format('%.3f', it) }.toString() }
}

// Main
println '=== Active Inference in Groovy ==='
println 'Belief Updating & Free Energy Minimization\n'

def agent = new ActiveInferenceAgent(4, 3, 2)
def rng = new Random(42)

println "Initial beliefs: ${agent.beliefsStr()}\n"

(1..10).each { t ->
    int obs = rng.nextInt(agent.nObs)
    agent.updateBeliefs(obs)
    int action = agent.selectAction()
    double fe = agent.calculateFreeEnergy()
    printf("Step %2d | Obs: %d | Action: %d | FE: %6.4f | Beliefs: %s%n",
           t, obs, action, fe, agent.beliefsStr())
}

println '\n✅ Groovy Active Inference simulation complete'
