;;;; Active Inference Implementation in Common Lisp
;;;;
;;;; Demonstrates belief updating, free energy minimization, and policy
;;;; selection using Common Lisp's symbolic computation and CLOS.

(defun make-vector (n &optional (init-val 0.0))
  "Create a vector of length N initialized to INIT-VAL."
  (make-array n :initial-element (coerce init-val 'double-float)))

(defun normalize (vec)
  "Normalize a vector in-place so elements sum to 1."
  (let ((s (reduce #'+ vec)))
    (when (> s 1d-10)
      (dotimes (i (length vec))
        (setf (aref vec i) (/ (aref vec i) s)))))
  vec)

(defstruct agent
  "Active Inference agent."
  (n-states 4)
  (n-obs 3)
  (n-actions 2)
  (precision 1.0d0)
  beliefs A B C D)

(defun make-agent (&key (n-states 4) (n-obs 3) (n-actions 2) (precision 1.0d0))
  "Create and initialize an Active Inference agent."
  (let ((agent (make-instance-agent n-states n-obs n-actions precision)))
    agent))

(defun make-instance-agent (n-states n-obs n-actions precision)
  "Internal constructor for agent."
  (let* ((beliefs (normalize (make-vector n-states 1.0d0)))
         (D (normalize (make-vector n-states 1.0d0)))
         ;; A matrix: n-obs x n-states with diagonal bias
         (A (make-array (list n-obs n-states) :initial-element (/ 1.0d0 n-obs)))
         ;; B matrix: n-states x n-states
         (B (make-array (list n-states n-states) :initial-element (/ 1.0d0 n-states)))
         ;; C preferences
         (C (make-vector n-obs 0.2d0)))
    ;; Bias A diagonal
    (dotimes (i (min n-obs n-states))
      (setf (aref A i i) 0.8d0))
    ;; Normalize A columns
    (dotimes (j n-states)
      (let ((s 0.0d0))
        (dotimes (i n-obs) (incf s (aref A i j)))
        (when (> s 1d-10)
          (dotimes (i n-obs) (setf (aref A i j) (/ (aref A i j) s))))))
    ;; Set C preferences
    (setf (aref C 0) 1.0d0)
    (normalize C)
    (make-agent :n-states n-states :n-obs n-obs :n-actions n-actions
                :precision precision :beliefs beliefs :A A :B B :C C :D D)))

(defun update-beliefs (agent observation)
  "Update beliefs given an observation."
  (let ((beliefs (agent-beliefs agent))
        (A (agent-A agent))
        (n-states (agent-n-states agent)))
    (dotimes (s n-states)
      (setf (aref beliefs s) (* (aref beliefs s) (aref A observation s))))
    (normalize beliefs)))

(defun calculate-free-energy (agent)
  "Calculate variational free energy (KL divergence from prior)."
  (let ((fe 0.0d0)
        (beliefs (agent-beliefs agent))
        (D (agent-D agent)))
    (dotimes (s (agent-n-states agent))
      (when (and (> (aref beliefs s) 1d-10) (> (aref D s) 1d-10))
        (incf fe (* (aref beliefs s) (log (/ (aref beliefs s) (aref D s)))))))
    fe))

(defun select-action (agent)
  "Select action minimizing expected free energy."
  (let* ((n-actions (agent-n-actions agent))
         (n-states (agent-n-states agent))
         (n-obs (agent-n-obs agent))
         (beliefs (agent-beliefs agent))
         (A (agent-A agent))
         (C (agent-C agent))
         (prec (agent-precision agent))
         (efe (make-vector n-actions 0.0d0)))
    ;; Compute EFE per action
    (dotimes (a n-actions)
      (dotimes (s n-states)
        (let ((pred-obs 0.0d0))
          (dotimes (o n-obs) (incf pred-obs (* (aref A o s) (aref C o))))
          (incf (aref efe a) (* (aref beliefs s) (- pred-obs))))))
    ;; Softmax
    (let* ((max-efe (reduce #'max efe))
           (probs (make-vector n-actions)))
      (dotimes (a n-actions)
        (setf (aref probs a) (exp (* (- prec) (- (aref efe a) max-efe)))))
      (normalize probs)
      ;; Sample
      (let ((r (random 1.0d0))
            (cum 0.0d0))
        (dotimes (a n-actions (1- n-actions))
          (incf cum (aref probs a))
          (when (<= r cum) (return-from select-action a)))))))

(defun format-beliefs (beliefs)
  "Format beliefs vector as a readable string."
  (format nil "(~{~,3f~^ ~})"
          (coerce beliefs 'list)))

(defun main ()
  "Run the Active Inference simulation."
  (format t "=== Active Inference in Common Lisp ===~%")
  (format t "Belief Updating & Free Energy Minimization~%~%")

  (let ((agent (make-agent :n-states 4 :n-obs 3 :n-actions 2))
        (*random-state* (make-random-state t)))
    (format t "Initial beliefs: ~a~%~%" (format-beliefs (agent-beliefs agent)))

    (dotimes (t-step 10)
      (let* ((obs (random (agent-n-obs agent))))
        (update-beliefs agent obs)
        (let ((action (select-action agent))
              (fe (calculate-free-energy agent)))
          (format t "Step ~2d | Obs: ~d | Action: ~d | FE: ~6,4f | Beliefs: ~a~%"
                  (1+ t-step) obs action fe
                  (format-beliefs (agent-beliefs agent))))))

    (format t "~%✅ Common Lisp Active Inference simulation complete~%")))

(main)
