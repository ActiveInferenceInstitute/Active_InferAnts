;; Active Inference Implementation in Scheme (R7RS)
;;
;; Demonstrates belief updating, free energy minimization, and policy
;; selection using Scheme's functional paradigm and list processing.

(import (scheme base)
        (scheme write)
        (scheme inexact)
        (scheme process-context))

;; Vector utilities
(define (make-uniform-vector n)
  (make-vector n (/ 1.0 n)))

(define (vector-sum v)
  (let ((s 0.0))
    (vector-for-each (lambda (x) (set! s (+ s x))) v)
    s))

(define (normalize! v)
  (let ((s (vector-sum v)))
    (when (> s 1e-10)
      (let ((n (vector-length v)))
        (do ((i 0 (+ i 1))) ((= i n))
          (vector-set! v i (/ (vector-ref v i) s)))))
    v))

;; Agent structure as a list-based record
(define (make-agent n-states n-obs n-actions)
  (let* ((beliefs (make-uniform-vector n-states))
         (prior (make-uniform-vector n-states))
         ;; A matrix: vector of vectors (obs x states) with diagonal bias
         (A (let ((m (make-vector n-obs)))
              (do ((i 0 (+ i 1))) ((= i n-obs))
                (vector-set! m i (make-vector n-states (/ 1.0 n-obs)))
                (when (< i n-states)
                  (vector-set! (vector-ref m i) i 0.8)))
              ;; Normalize columns
              (do ((j 0 (+ j 1))) ((= j n-states))
                (let ((s 0.0))
                  (do ((i 0 (+ i 1))) ((= i n-obs))
                    (set! s (+ s (vector-ref (vector-ref m i) j))))
                  (do ((i 0 (+ i 1))) ((= i n-obs))
                    (vector-set! (vector-ref m i) j
                                 (/ (vector-ref (vector-ref m i) j) s)))))
              m))
         ;; Preferences
         (C (let ((v (make-vector n-obs 0.2)))
              (vector-set! v 0 1.0)
              (normalize! v))))
    (list beliefs prior A C n-states n-obs n-actions 1.0)))

;; Accessors
(define (agent-beliefs a) (list-ref a 0))
(define (agent-prior a) (list-ref a 1))
(define (agent-A a) (list-ref a 2))
(define (agent-C a) (list-ref a 3))
(define (agent-n-states a) (list-ref a 4))
(define (agent-n-obs a) (list-ref a 5))
(define (agent-n-actions a) (list-ref a 6))
(define (agent-precision a) (list-ref a 7))

(define (update-beliefs! agent obs)
  (let ((beliefs (agent-beliefs agent))
        (A (agent-A agent))
        (n (agent-n-states agent)))
    (do ((s 0 (+ s 1))) ((= s n))
      (vector-set! beliefs s
                   (* (vector-ref beliefs s)
                      (vector-ref (vector-ref A obs) s))))
    (normalize! beliefs)))

(define (calculate-free-energy agent)
  (let ((beliefs (agent-beliefs agent))
        (prior (agent-prior agent))
        (n (agent-n-states agent))
        (fe 0.0))
    (do ((s 0 (+ s 1))) ((= s n))
      (let ((b (vector-ref beliefs s))
            (d (vector-ref prior s)))
        (when (and (> b 1e-10) (> d 1e-10))
          (set! fe (+ fe (* b (log (/ b d))))))))
    fe))

(define *rng-state* 42)
(define (pseudo-random n)
  (set! *rng-state* (modulo (+ (* *rng-state* 1103515245) 12345) (expt 2 31)))
  (modulo (quotient *rng-state* 65536) n))

(define (pseudo-random-double)
  (set! *rng-state* (modulo (+ (* *rng-state* 1103515245) 12345) (expt 2 31)))
  (/ (exact->inexact *rng-state*) (exact->inexact (expt 2 31))))

(define (select-action agent)
  (let* ((n-actions (agent-n-actions agent))
         (n-states (agent-n-states agent))
         (n-obs (agent-n-obs agent))
         (beliefs (agent-beliefs agent))
         (A (agent-A agent))
         (C (agent-C agent))
         (prec (agent-precision agent))
         (efe (make-vector n-actions 0.0)))
    ;; Compute EFE
    (do ((a 0 (+ a 1))) ((= a n-actions))
      (do ((s 0 (+ s 1))) ((= s n-states))
        (let ((pred 0.0))
          (do ((o 0 (+ o 1))) ((= o n-obs))
            (set! pred (+ pred (* (vector-ref (vector-ref A o) s)
                                  (vector-ref C o)))))
          (vector-set! efe a (+ (vector-ref efe a)
                                (* (vector-ref beliefs s) (- pred)))))))
    ;; Softmax
    (let* ((max-e (let ((m -1e10))
                    (do ((a 0 (+ a 1))) ((= a n-actions) m)
                      (when (> (vector-ref efe a) m) (set! m (vector-ref efe a))))))
           (probs (make-vector n-actions)))
      (do ((a 0 (+ a 1))) ((= a n-actions))
        (vector-set! probs a (exp (* (- prec) (- (vector-ref efe a) max-e)))))
      (normalize! probs)
      ;; Sample
      (let ((r (pseudo-random-double)) (cum 0.0))
        (let loop ((a 0))
          (if (= a n-actions) (- n-actions 1)
              (begin
                (set! cum (+ cum (vector-ref probs a)))
                (if (<= r cum) a (loop (+ a 1))))))))))

(define (format-beliefs v)
  (let ((parts '()))
    (do ((i (- (vector-length v) 1) (- i 1))) ((< i 0))
      (set! parts (cons (number->string (/ (round (* (vector-ref v i) 1000)) 1000.0)) parts)))
    (string-append "(" (let loop ((lst parts) (acc ""))
                         (if (null? lst) acc
                             (loop (cdr lst)
                                   (string-append acc (if (string=? acc "") "" " ") (car lst))))) ")")))

;; Main
(display "=== Active Inference in Scheme ===\n")
(display "Belief Updating & Free Energy Minimization\n\n")

(let ((agent (make-agent 4 3 2)))
  (display (string-append "Initial beliefs: " (format-beliefs (agent-beliefs agent)) "\n\n"))
  (do ((t 1 (+ t 1))) ((> t 10))
    (let* ((obs (pseudo-random (agent-n-obs agent))))
      (update-beliefs! agent obs)
      (let ((action (select-action agent))
            (fe (calculate-free-energy agent)))
        (display (string-append "Step " (if (< t 10) " " "") (number->string t)
                                " | Obs: " (number->string obs)
                                " | Action: " (number->string action)
                                " | FE: " (number->string (/ (round (* fe 10000)) 10000.0))
                                " | Beliefs: " (format-beliefs (agent-beliefs agent)) "\n")))))
  (display "\n✅ Scheme Active Inference simulation complete\n"))
