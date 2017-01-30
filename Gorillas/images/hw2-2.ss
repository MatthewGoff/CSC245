;;homework 2 problem 2
(load "hw2-1.ss")

;;Grade
(define times10
  (lambda (nums)
    (map (lambda (x) (* 10 x)) nums)))

(add-batch-tests! "EX1" '((times10 '(1 2 3 4 5)) => '(10 20 30 40 50)
			  (times10 '(25)) => '(250)
			  (times10 '()) => '()))

;;Grade
(define pair-up
  (lambda (elt ls)
    (if (null? ls)
	'()
	(map (lambda (y) (cons elt y)) ls))))

(add-batch-tests! "EX2" '((pair-up 'x '(a b c d))
			  =>  '((x . a) (x . b) (x . c) (x . d))))
(add-batch-tests! "EX2" '((pair-up 'a '(1 2 3))
			  =>
			  '((a . 1) (a . 2) (a . 3))))
(add-batch-tests! "EX2" '((pair-up 'a '())  =>  '()))


;;Grade
(define isodd?
  (lambda (num)
    (if (eq? (modulo num 2) 1) 'x num)))

(define x-odds
  (lambda (nums)
    (map isodd? nums)))

(add-batch-tests! "EX3" '((x-odds '(1 2 3 4 5 9))  =>  '(x 2 x 4 x x)))
(add-batch-tests! "EX3" '((x-odds '(1 3 5))  =>  '(x x x)))

;;Grade
(define replace
  (lambda (old new syms)
    (map (lambda (x) (if (eqv? x old) new x)) syms)))

(add-batch-tests! "EX4" '((replace 'red 'blue '(red fish blue fish))
			  =>
			  '(blue fish blue fish)))

;;Grade
(define remove
  (lambda (elt ls)
    (define elt?
      (lambda (x)
	(if (eqv? x elt) #f #t)))
    (filter elt? ls)))

(add-batch-tests! "EX5" '((remove 'cream '(i scream for ice cream))
			  =>  '(i scream for ice)))

  
;;Grade
(define length
  (lambda (ls)
    (fold-left (lambda (acc head) (+ acc 1)) 0 ls)))

;;Grade
(define average
  (lambda (nums)
    (/ (fold-right (lambda (acc head) (+ acc head)) 0 nums) (length nums))))

(add-batch-tests! "EX7" '((average '(1 2 3)) => 2))
