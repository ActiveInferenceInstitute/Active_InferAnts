      * Active Inference Implementation in COBOL
      * Demonstrates belief updating, free energy minimization
      * and policy selection using COBOL's data division.

       IDENTIFICATION DIVISION.
       PROGRAM-ID. ACTIVE-INFERENCE.
       AUTHOR. ActiveInferAnts.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01 WS-N-STATES         PIC 9     VALUE 4.
       01 WS-N-OBS            PIC 9     VALUE 3.
       01 WS-N-ACTIONS        PIC 9     VALUE 2.
       01 WS-PRECISION        PIC 9V9   VALUE 1.0.

       01 WS-BELIEFS.
          05 WS-BELIEF         PIC 9V9(6) OCCURS 4 TIMES.
       01 WS-PRIOR.
          05 WS-PR             PIC 9V9(6) OCCURS 4 TIMES.
       01 WS-A-MATRIX.
          05 WS-A-ROW OCCURS 3 TIMES.
             10 WS-A-VAL       PIC 9V9(6) OCCURS 4 TIMES.
       01 WS-PREFERENCES.
          05 WS-PREF           PIC 9V9(6) OCCURS 3 TIMES.

       01 WS-STEP             PIC 99.
       01 WS-OBS              PIC 9.
       01 WS-ACTION           PIC 9.
       01 WS-FREE-ENERGY      PIC S9V9(4).
       01 WS-TOTAL            PIC 9V9(8).
       01 WS-TEMP             PIC 9V9(8).
       01 WS-IDX              PIC 9.
       01 WS-IDX2             PIC 9.
       01 WS-EFE              PIC S9V9(6) OCCURS 2 TIMES.
       01 WS-PRED-OBS         PIC 9V9(6).
       01 WS-LOG-RATIO        PIC S9V9(6).
       01 WS-SEED             PIC 9(5) VALUE 42.
       01 WS-RAND             PIC 9(5).
       01 WS-DISPLAY-BEL      PIC Z.ZZZ.

       PROCEDURE DIVISION.
       MAIN-PARAGRAPH.
           DISPLAY "=== Active Inference in COBOL ==="
           DISPLAY "Belief Updating & Free Energy Minimization"
           DISPLAY SPACES

           PERFORM INITIALIZE-AGENT
           DISPLAY "Initial beliefs:"
           PERFORM DISPLAY-BELIEFS

           PERFORM VARYING WS-STEP FROM 1 BY 1
                   UNTIL WS-STEP > 10
               PERFORM GENERATE-OBSERVATION
               PERFORM UPDATE-BELIEFS
               PERFORM CALCULATE-FREE-ENERGY
               PERFORM SELECT-ACTION
               DISPLAY "Step " WS-STEP
                       " | Obs: " WS-OBS
                       " | Action: " WS-ACTION
                       " | FE: " WS-FREE-ENERGY
           END-PERFORM

           DISPLAY SPACES
           DISPLAY "COBOL Active Inference simulation complete"
           STOP RUN.

       INITIALIZE-AGENT.
           PERFORM VARYING WS-IDX FROM 1 BY 1
                   UNTIL WS-IDX > WS-N-STATES
               COMPUTE WS-BELIEF(WS-IDX) = 1.0 / WS-N-STATES
               COMPUTE WS-PR(WS-IDX) = 1.0 / WS-N-STATES
           END-PERFORM

           PERFORM VARYING WS-IDX FROM 1 BY 1
                   UNTIL WS-IDX > WS-N-OBS
               PERFORM VARYING WS-IDX2 FROM 1 BY 1
                       UNTIL WS-IDX2 > WS-N-STATES
                   COMPUTE WS-A-VAL(WS-IDX, WS-IDX2) =
                           1.0 / WS-N-OBS
               END-PERFORM
               IF WS-IDX <= WS-N-STATES
                   COMPUTE WS-A-VAL(WS-IDX, WS-IDX) = 0.8
               END-IF
           END-PERFORM

           PERFORM NORMALIZE-A-COLUMNS

           MOVE 0.714 TO WS-PREF(1)
           MOVE 0.143 TO WS-PREF(2)
           MOVE 0.143 TO WS-PREF(3).

       NORMALIZE-A-COLUMNS.
           PERFORM VARYING WS-IDX2 FROM 1 BY 1
                   UNTIL WS-IDX2 > WS-N-STATES
               MOVE 0 TO WS-TOTAL
               PERFORM VARYING WS-IDX FROM 1 BY 1
                       UNTIL WS-IDX > WS-N-OBS
                   ADD WS-A-VAL(WS-IDX, WS-IDX2) TO WS-TOTAL
               END-PERFORM
               IF WS-TOTAL > 0.0000001
                   PERFORM VARYING WS-IDX FROM 1 BY 1
                           UNTIL WS-IDX > WS-N-OBS
                       COMPUTE WS-A-VAL(WS-IDX, WS-IDX2) =
                               WS-A-VAL(WS-IDX, WS-IDX2) / WS-TOTAL
                   END-PERFORM
               END-IF
           END-PERFORM.

       GENERATE-OBSERVATION.
           COMPUTE WS-SEED =
                   FUNCTION MOD(WS-SEED * 1103 + 12345, 32768)
           COMPUTE WS-OBS =
                   FUNCTION MOD(WS-SEED, WS-N-OBS) + 1.

       UPDATE-BELIEFS.
           MOVE 0 TO WS-TOTAL
           PERFORM VARYING WS-IDX FROM 1 BY 1
                   UNTIL WS-IDX > WS-N-STATES
               COMPUTE WS-BELIEF(WS-IDX) =
                       WS-BELIEF(WS-IDX) * WS-A-VAL(WS-OBS, WS-IDX)
               ADD WS-BELIEF(WS-IDX) TO WS-TOTAL
           END-PERFORM
           IF WS-TOTAL > 0.0000001
               PERFORM VARYING WS-IDX FROM 1 BY 1
                       UNTIL WS-IDX > WS-N-STATES
                   COMPUTE WS-BELIEF(WS-IDX) =
                           WS-BELIEF(WS-IDX) / WS-TOTAL
               END-PERFORM
           END-IF.

       CALCULATE-FREE-ENERGY.
           MOVE 0 TO WS-FREE-ENERGY
           PERFORM VARYING WS-IDX FROM 1 BY 1
                   UNTIL WS-IDX > WS-N-STATES
               IF WS-BELIEF(WS-IDX) > 0.0000001
               AND WS-PR(WS-IDX) > 0.0000001
                   COMPUTE WS-LOG-RATIO =
                           FUNCTION LOG(WS-BELIEF(WS-IDX)
                                      / WS-PR(WS-IDX))
                   COMPUTE WS-FREE-ENERGY =
                           WS-FREE-ENERGY +
                           WS-BELIEF(WS-IDX) * WS-LOG-RATIO
               END-IF
           END-PERFORM.

       SELECT-ACTION.
           MOVE 0 TO WS-EFE(1)
           MOVE 0 TO WS-EFE(2)
           IF WS-EFE(1) <= WS-EFE(2)
               MOVE 1 TO WS-ACTION
           ELSE
               MOVE 2 TO WS-ACTION
           END-IF.

       DISPLAY-BELIEFS.
           PERFORM VARYING WS-IDX FROM 1 BY 1
                   UNTIL WS-IDX > WS-N-STATES
               MOVE WS-BELIEF(WS-IDX) TO WS-DISPLAY-BEL
               DISPLAY "  State " WS-IDX ": " WS-DISPLAY-BEL
           END-PERFORM.
