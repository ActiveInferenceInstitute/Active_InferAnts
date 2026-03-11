<#
.SYNOPSIS
    Active Inference Implementation in PowerShell

.DESCRIPTION
    Demonstrates belief updating, free energy minimization, and policy
    selection using PowerShell's object pipeline and .NET integration.
#>

class ActiveInferenceAgent {
    [int]$NStates
    [int]$NObs
    [int]$NActions
    [double]$Precision
    [double[]]$Beliefs
    [double[,]]$A
    [double[]]$C
    [double[]]$D

    ActiveInferenceAgent([int]$nStates, [int]$nObs, [int]$nActions) {
        $this.NStates = $nStates
        $this.NObs = $nObs
        $this.NActions = $nActions
        $this.Precision = 1.0

        $this.Beliefs = @(1.0 / $nStates) * $nStates
        $this.D = @(1.0 / $nStates) * $nStates

        # Preferences
        $this.C = @(0.2) * $nObs
        $this.C[0] = 1.0
        $sum = ($this.C | Measure-Object -Sum).Sum
        $this.C = $this.C | ForEach-Object { $_ / $sum }

        # A matrix with diagonal bias
        $this.A = [double[,]]::new($nObs, $nStates)
        for ($i = 0; $i -lt $nObs; $i++) {
            for ($j = 0; $j -lt $nStates; $j++) {
                $this.A[$i, $j] = 1.0 / $nObs
            }
        }
        $minDim = [Math]::Min($nObs, $nStates)
        for ($i = 0; $i -lt $minDim; $i++) { $this.A[$i, $i] = 0.8 }
        # Normalize columns
        for ($j = 0; $j -lt $nStates; $j++) {
            $s = 0.0
            for ($i = 0; $i -lt $nObs; $i++) { $s += $this.A[$i, $j] }
            for ($i = 0; $i -lt $nObs; $i++) { $this.A[$i, $j] /= $s }
        }
    }

    [void]UpdateBeliefs([int]$obs) {
        $total = 0.0
        for ($s = 0; $s -lt $this.NStates; $s++) {
            $this.Beliefs[$s] *= $this.A[$obs, $s]
            $total += $this.Beliefs[$s]
        }
        if ($total -gt 1e-10) {
            for ($s = 0; $s -lt $this.NStates; $s++) {
                $this.Beliefs[$s] /= $total
            }
        }
    }

    [double]CalculateFreeEnergy() {
        $fe = 0.0
        for ($s = 0; $s -lt $this.NStates; $s++) {
            $b = $this.Beliefs[$s]; $d = $this.D[$s]
            if ($b -gt 1e-10 -and $d -gt 1e-10) {
                $fe += $b * [Math]::Log($b / $d)
            }
        }
        return $fe
    }

    [int]SelectAction() {
        $efe = @(0.0) * $this.NActions
        for ($a = 0; $a -lt $this.NActions; $a++) {
            for ($s = 0; $s -lt $this.NStates; $s++) {
                $predObs = 0.0
                for ($o = 0; $o -lt $this.NObs; $o++) {
                    $predObs += $this.A[$o, $s] * $this.C[$o]
                }
                $efe[$a] += $this.Beliefs[$s] * (-$predObs)
            }
        }
        $maxE = ($efe | Measure-Object -Maximum).Maximum
        $probs = $efe | ForEach-Object { [Math]::Exp(-$this.Precision * ($_ - $maxE)) }
        $pSum = ($probs | Measure-Object -Sum).Sum
        $probs = $probs | ForEach-Object { $_ / $pSum }

        $r = (Get-Random -Minimum 0.0 -Maximum 1.0)
        $cum = 0.0
        for ($a = 0; $a -lt $this.NActions; $a++) {
            $cum += $probs[$a]
            if ($r -le $cum) { return $a }
        }
        return $this.NActions - 1
    }

    [string]BeliefsStr() {
        return "[" + (($this.Beliefs | ForEach-Object { "{0:F3}" -f $_ }) -join ", ") + "]"
    }
}

# Main
Write-Host "=== Active Inference in PowerShell ==="
Write-Host "Belief Updating & Free Energy Minimization`n"

$agent = [ActiveInferenceAgent]::new(4, 3, 2)
$rng = [System.Random]::new(42)

Write-Host "Initial beliefs: $($agent.BeliefsStr())`n"

for ($t = 1; $t -le 10; $t++) {
    $obs = $rng.Next($agent.NObs)
    $agent.UpdateBeliefs($obs)
    $action = $agent.SelectAction()
    $fe = $agent.CalculateFreeEnergy()
    Write-Host ("Step {0,2} | Obs: {1} | Action: {2} | FE: {3:F4} | Beliefs: {4}" -f $t, $obs, $action, $fe, $agent.BeliefsStr())
}

Write-Host "`n✅ PowerShell Active Inference simulation complete"
