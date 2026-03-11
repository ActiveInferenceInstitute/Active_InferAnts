/// Active Inference Implementation in Dart
///
/// Demonstrates belief updating, free energy minimization, and policy
/// selection using Dart's class system and null safety.
import 'dart:math';

class ActiveInferenceAgent {
  final int nStates;
  final int nObs;
  final int nActions;
  final double precision;
  List<double> beliefs;
  List<List<double>> A; // observation model
  List<List<double>> B; // transition model
  List<double> C;       // preferences
  List<double> D;       // prior
  final Random _rng;

  ActiveInferenceAgent({
    required this.nStates,
    required this.nObs,
    required this.nActions,
    this.precision = 1.0,
    int? seed,
  })  : _rng = Random(seed ?? 42),
        beliefs = List.filled(nStates, 1.0 / nStates),
        D = List.filled(nStates, 1.0 / nStates),
        C = List.generate(nObs, (i) => i == 0 ? 1.0 : 0.2),
        A = List.generate(
            nObs, (i) => List.generate(nStates, (j) => 1.0 / nObs)),
        B = List.generate(
            nStates, (i) => List.generate(nStates, (j) => 1.0 / nStates)) {
    // Bias A matrix diagonal
    for (int i = 0; i < min(nObs, nStates); i++) {
      A[i][i] = 0.8;
    }
    _normalizeColumns(A);
    _normalizeList(C);
  }

  void _normalizeList(List<double> v) {
    double s = v.fold(0.0, (a, b) => a + b);
    if (s > 1e-10) for (int i = 0; i < v.length; i++) v[i] /= s;
  }

  void _normalizeColumns(List<List<double>> m) {
    int cols = m[0].length;
    for (int j = 0; j < cols; j++) {
      double s = 0;
      for (int i = 0; i < m.length; i++) s += m[i][j];
      if (s > 1e-10) for (int i = 0; i < m.length; i++) m[i][j] /= s;
    }
  }

  void updateBeliefs(int observation) {
    for (int s = 0; s < nStates; s++) {
      beliefs[s] *= A[observation][s];
    }
    _normalizeList(beliefs);
  }

  double calculateFreeEnergy() {
    double fe = 0;
    for (int s = 0; s < nStates; s++) {
      if (beliefs[s] > 1e-10 && D[s] > 1e-10) {
        fe += beliefs[s] * log(beliefs[s] / D[s]);
      }
    }
    return fe;
  }

  int selectAction() {
    List<double> efe = List.filled(nActions, 0.0);
    for (int a = 0; a < nActions; a++) {
      for (int s = 0; s < nStates; s++) {
        double predObs = 0;
        for (int o = 0; o < nObs; o++) predObs += A[o][s] * C[o];
        efe[a] += beliefs[s] * (-predObs);
      }
    }
    // Softmax
    double maxEfe = efe.reduce(max);
    List<double> probs =
        efe.map((e) => exp(-precision * (e - maxEfe))).toList();
    _normalizeList(probs);

    double r = _rng.nextDouble();
    double cumulative = 0;
    for (int a = 0; a < nActions; a++) {
      cumulative += probs[a];
      if (r <= cumulative) return a;
    }
    return nActions - 1;
  }

  String beliefsStr() =>
      beliefs.map((b) => b.toStringAsFixed(3)).toList().toString();
}

void main() {
  print('=== Active Inference in Dart ===');
  print('Belief Updating & Free Energy Minimization\n');

  final agent =
      ActiveInferenceAgent(nStates: 4, nObs: 3, nActions: 2, seed: 42);
  final rng = Random(42);

  print('Initial beliefs: ${agent.beliefsStr()}\n');

  for (int t = 0; t < 10; t++) {
    int obs = rng.nextInt(agent.nObs);
    agent.updateBeliefs(obs);
    int action = agent.selectAction();
    double fe = agent.calculateFreeEnergy();

    print('Step ${(t + 1).toString().padLeft(2)} | '
        'Obs: $obs | Action: $action | '
        'FE: ${fe.toStringAsFixed(4)} | '
        'Beliefs: ${agent.beliefsStr()}');
  }

  print('\n✅ Dart Active Inference simulation complete');
}
