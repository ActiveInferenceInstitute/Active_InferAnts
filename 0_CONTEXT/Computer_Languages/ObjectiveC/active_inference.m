/**
 * Active Inference Implementation in Objective-C
 *
 * Demonstrates belief updating, free energy minimization, and policy
 * selection using Objective-C's object system and Foundation framework.
 */
#import <Foundation/Foundation.h>
#include <math.h>
#include <stdlib.h>

@interface ActiveInferenceAgent : NSObject
@property (nonatomic) int nStates, nObs, nActions;
@property (nonatomic) double precision;
@property (nonatomic, strong) NSMutableArray<NSNumber *> *beliefs;
@property (nonatomic, strong) NSMutableArray<NSNumber *> *prior;
@property (nonatomic, strong) NSMutableArray<NSNumber *> *preferences;
@property (nonatomic, strong) NSMutableArray<NSMutableArray<NSNumber *> *> *A;
- (instancetype)initWithStates:(int)s obs:(int)o actions:(int)a;
- (void)updateBeliefsWithObservation:(int)obs;
- (double)calculateFreeEnergy;
- (int)selectAction;
- (NSString *)beliefsString;
@end

@implementation ActiveInferenceAgent

- (instancetype)initWithStates:(int)s obs:(int)o actions:(int)a {
    self = [super init];
    if (self) {
        _nStates = s; _nObs = o; _nActions = a; _precision = 1.0;
        _beliefs = [NSMutableArray arrayWithCapacity:s];
        _prior = [NSMutableArray arrayWithCapacity:s];
        for (int i = 0; i < s; i++) {
            [_beliefs addObject:@(1.0 / s)];
            [_prior addObject:@(1.0 / s)];
        }
        _preferences = [NSMutableArray arrayWithCapacity:o];
        double pSum = 0;
        for (int i = 0; i < o; i++) {
            double v = (i == 0) ? 1.0 : 0.2;
            [_preferences addObject:@(v)];
            pSum += v;
        }
        for (int i = 0; i < o; i++)
            _preferences[i] = @(_preferences[i].doubleValue / pSum);

        _A = [NSMutableArray arrayWithCapacity:o];
        for (int i = 0; i < o; i++) {
            NSMutableArray *row = [NSMutableArray arrayWithCapacity:s];
            for (int j = 0; j < s; j++)
                [row addObject:@(1.0 / o)];
            [_A addObject:row];
        }
        for (int i = 0; i < MIN(o, s); i++)
            _A[i][i] = @(0.8);
        // Normalize columns
        for (int j = 0; j < s; j++) {
            double sum = 0;
            for (int i = 0; i < o; i++) sum += _A[i][j].doubleValue;
            for (int i = 0; i < o; i++)
                _A[i][j] = @(_A[i][j].doubleValue / sum);
        }
    }
    return self;
}

- (void)updateBeliefsWithObservation:(int)obs {
    double total = 0;
    for (int s = 0; s < _nStates; s++) {
        double v = _beliefs[s].doubleValue * _A[obs][s].doubleValue;
        _beliefs[s] = @(v);
        total += v;
    }
    if (total > 1e-10)
        for (int s = 0; s < _nStates; s++)
            _beliefs[s] = @(_beliefs[s].doubleValue / total);
}

- (double)calculateFreeEnergy {
    double fe = 0;
    for (int s = 0; s < _nStates; s++) {
        double b = _beliefs[s].doubleValue;
        double d = _prior[s].doubleValue;
        if (b > 1e-10 && d > 1e-10)
            fe += b * log(b / d);
    }
    return fe;
}

- (int)selectAction {
    double efe[_nActions];
    for (int a = 0; a < _nActions; a++) {
        efe[a] = 0;
        for (int s = 0; s < _nStates; s++) {
            double predObs = 0;
            for (int o = 0; o < _nObs; o++)
                predObs += _A[o][s].doubleValue * _preferences[o].doubleValue;
            efe[a] += _beliefs[s].doubleValue * (-predObs);
        }
    }
    double maxE = efe[0];
    for (int a = 1; a < _nActions; a++) if (efe[a] > maxE) maxE = efe[a];
    double probs[_nActions], pSum = 0;
    for (int a = 0; a < _nActions; a++) {
        probs[a] = exp(-_precision * (efe[a] - maxE));
        pSum += probs[a];
    }
    for (int a = 0; a < _nActions; a++) probs[a] /= pSum;
    double r = (double)arc4random() / UINT32_MAX;
    double cum = 0;
    for (int a = 0; a < _nActions; a++) {
        cum += probs[a];
        if (r <= cum) return a;
    }
    return _nActions - 1;
}

- (NSString *)beliefsString {
    NSMutableArray *strs = [NSMutableArray array];
    for (NSNumber *b in _beliefs)
        [strs addObject:[NSString stringWithFormat:@"%.3f", b.doubleValue]];
    return [NSString stringWithFormat:@"[%@]", [strs componentsJoinedByString:@", "]];
}
@end

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        NSLog(@"=== Active Inference in Objective-C ===");
        NSLog(@"Belief Updating & Free Energy Minimization\n");
        ActiveInferenceAgent *agent =
            [[ActiveInferenceAgent alloc] initWithStates:4 obs:3 actions:2];
        srand(42);
        NSLog(@"Initial beliefs: %@\n", [agent beliefsString]);
        for (int t = 0; t < 10; t++) {
            int obs = rand() % agent.nObs;
            [agent updateBeliefsWithObservation:obs];
            int action = [agent selectAction];
            double fe = [agent calculateFreeEnergy];
            NSLog(@"Step %2d | Obs: %d | Action: %d | FE: %6.4f | Beliefs: %@",
                  t + 1, obs, action, fe, [agent beliefsString]);
        }
        NSLog(@"\n✅ Objective-C Active Inference simulation complete");
    }
    return 0;
}
