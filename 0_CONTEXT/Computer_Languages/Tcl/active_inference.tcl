#!/usr/bin/env tclsh
# Active Inference Implementation in Tcl
#
# Demonstrates belief updating, free energy minimization, and policy
# selection using Tcl's dynamic typing and list operations.

package require Tcl 8.5

# --- Vector Utilities ---
proc make_uniform {n} {
    set v {}
    set val [expr {1.0 / $n}]
    for {set i 0} {$i < $n} {incr i} { lappend v $val }
    return $v
}

proc normalize {vec} {
    set s 0.0
    foreach x $vec { set s [expr {$s + $x}] }
    if {$s < 1e-10} { return $vec }
    set result {}
    foreach x $vec { lappend result [expr {$x / $s}] }
    return $result
}

proc vec_str {vec} {
    set parts {}
    foreach x $vec { lappend parts [format "%.3f" $x] }
    return "\[[join $parts {, }]\]"
}

# --- Agent ---
proc create_agent {n_states n_obs n_actions} {
    set beliefs [make_uniform $n_states]
    set prior [make_uniform $n_states]

    # Preferences: prefer first obs
    set C {}
    for {set i 0} {$i < $n_obs} {incr i} {
        if {$i == 0} { lappend C 1.0 } else { lappend C 0.2 }
    }
    set C [normalize $C]

    # A matrix: list of lists (obs x states), diagonal bias
    set A {}
    for {set i 0} {$i < $n_obs} {incr i} {
        set row {}
        for {set j 0} {$j < $n_states} {incr j} {
            if {$i == $j && $j < $n_obs} {
                lappend row 0.8
            } else {
                lappend row [expr {1.0 / $n_obs}]
            }
        }
        lappend A $row
    }
    # Normalize columns
    for {set j 0} {$j < $n_states} {incr j} {
        set s 0.0
        for {set i 0} {$i < $n_obs} {incr i} {
            set s [expr {$s + [lindex [lindex $A $i] $j]}]
        }
        for {set i 0} {$i < $n_obs} {incr i} {
            set row [lindex $A $i]
            lset row $j [expr {[lindex $row $j] / $s}]
            lset A $i $row
        }
    }

    return [dict create beliefs $beliefs prior $prior A $A C $C \
        n_states $n_states n_obs $n_obs n_actions $n_actions precision 1.0]
}

proc update_beliefs {agentVar obs} {
    upvar $agentVar agent
    set beliefs [dict get $agent beliefs]
    set A [dict get $agent A]
    set n [dict get $agent n_states]

    set new_beliefs {}
    set total 0.0
    for {set s 0} {$s < $n} {incr s} {
        set v [expr {[lindex $beliefs $s] * [lindex [lindex $A $obs] $s]}]
        lappend new_beliefs $v
        set total [expr {$total + $v}]
    }
    if {$total > 1e-10} {
        set normalized {}
        foreach b $new_beliefs { lappend normalized [expr {$b / $total}] }
        dict set agent beliefs $normalized
    } else {
        dict set agent beliefs [make_uniform $n]
    }
}

proc calculate_free_energy {agent} {
    set beliefs [dict get $agent beliefs]
    set prior [dict get $agent prior]
    set n [dict get $agent n_states]
    set fe 0.0
    for {set s 0} {$s < $n} {incr s} {
        set b [lindex $beliefs $s]
        set d [lindex $prior $s]
        if {$b > 1e-10 && $d > 1e-10} {
            set fe [expr {$fe + $b * log($b / $d)}]
        }
    }
    return $fe
}

proc select_action {agent} {
    set n_actions [dict get $agent n_actions]
    set n_states [dict get $agent n_states]
    set n_obs [dict get $agent n_obs]
    set beliefs [dict get $agent beliefs]
    set A [dict get $agent A]
    set C [dict get $agent C]
    set prec [dict get $agent precision]

    set efe {}
    for {set a 0} {$a < $n_actions} {incr a} {
        set e 0.0
        for {set s 0} {$s < $n_states} {incr s} {
            set pred 0.0
            for {set o 0} {$o < $n_obs} {incr o} {
                set pred [expr {$pred + [lindex [lindex $A $o] $s] * [lindex $C $o]}]
            }
            set e [expr {$e + [lindex $beliefs $s] * (-$pred)}]
        }
        lappend efe $e
    }
    # Softmax
    set max_e [lindex $efe 0]
    foreach e $efe { if {$e > $max_e} { set max_e $e } }
    set probs {}
    set psum 0.0
    foreach e $efe {
        set p [expr {exp(-$prec * ($e - $max_e))}]
        lappend probs $p
        set psum [expr {$psum + $p}]
    }
    set probs_norm {}
    foreach p $probs { lappend probs_norm [expr {$p / $psum}] }

    set r [expr {rand()}]
    set cum 0.0
    for {set a 0} {$a < $n_actions} {incr a} {
        set cum [expr {$cum + [lindex $probs_norm $a]}]
        if {$r <= $cum} { return $a }
    }
    return [expr {$n_actions - 1}]
}

# --- Main ---
puts "=== Active Inference in Tcl ==="
puts "Belief Updating & Free Energy Minimization\n"

set agent [create_agent 4 3 2]
expr {srand(42)}

puts "Initial beliefs: [vec_str [dict get $agent beliefs]]\n"

for {set t 1} {$t <= 10} {incr t} {
    set obs [expr {int(rand() * [dict get $agent n_obs])}]
    update_beliefs agent $obs
    set action [select_action $agent]
    set fe [calculate_free_energy $agent]
    puts [format "Step %2d | Obs: %d | Action: %d | FE: %6.4f | Beliefs: %s" \
        $t $obs $action $fe [vec_str [dict get $agent beliefs]]]
}

puts "\n✅ Tcl Active Inference simulation complete"
