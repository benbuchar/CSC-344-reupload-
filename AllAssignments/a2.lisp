(defvar e1)
(defvar e2)
(defun andex (e1 e2) (list 'and e1 e2))
(defun orexp (e1 e2) (list 'or e1 e2))
(defun notexp (e1) (list 'not e1))

(setq p1 '(and x (or x (and y (not z)))))
(setq p2 '(and (and z nil) (or x 1)))
(setq p3 '(or 1 a))



;;(defun evalexp (bindings exp) (simplify (bind-values bindings exp)))


(defun simplifyOr(l)
	(setq e1 (car l))
	(setq e2 (cadr l))
	(cond
		((null e1) e2)
		((null e2) e1)
		((or (eq e1 1) (eq e2 1))1)
		((eq e1 e2) e1)
		(T (list 'or e1 e2))))


(defun simplifyAnd(l)
	(setq e1 (car l))
	(setq e2 (cadr l))
	(cond 
		((or (null e1) (null e2)) nil)
		((and (eq e1 1) (eq e2 1)) 1)
		((eq e1 e2) e1)
		((eq e1 1) e2)
		((eq e2 1) e1)
		(T (list 'and e1 e2))))


(defun simplifyNot(l)
	;;simplify its argument first
	(cond
	((eq  l 'nil) 1)
	((eq l 1) nil)
	(T (list 'not l))))

(defun reduceNot(l)
	(cond
		((null l) (simplifyNot l))
		((atom l) (simplifyNot l))
		;;((eq l 1) (simplifyNot (l)))
		((listp (car l)) (reduceNot(append (car l) (cdr l))))
		((listp l)
			(cond
				((eq (car l) 'and) (list 'or (simplifyNot(cadr l)) (simplifyNot(caddr l))))
				((eq (car l) 'or) (list 'and (simplifyNot(cadr l)) (simplifyNot(caddr l))))
				((simplifyNot(car l)))

				))))


(defun simplify(l)
	(cond
	((null l) nil)
	((atom l) l)
	((eq (car l) 'and) (simplifyAnd(simplify(cdr l))))
	((eq (car l) 'or) (simplifyOr(simplify(cdr l))))
	((eq (car l) 'not) (reduceNot(cdr l)))

	;;((listp (car l)) (append (simplify (car l)) (simplify (cdr l))))

	(T(cons (simplify(car l)) (simplify(cdr l))))))






(defun substitute (target replacement l)
	(cond	
	((null l) nil)
	((atom l) l)
	;;((listp l)(cons (car l) (substitute target replacement (cdr l))))
	((listp (car l)) (cons (substitute target replacement (car l)) (cdr l)))
	((eq (car l) 'nil) (cons (substitute target replacement (car l)) (cdr l)))
	((eq (car l) target) (cons replacement (substitute target replacement (cdr l))))
	(T (cons (car l) (substitute target replacement (cdr l))))))



(defun bind (bindings expression)
	(cond
	((eq bindings 'nil) expression)
	((null bindings) expression)
	((listp (car bindings)) (substitute (car bindings) (cadr bindings) expression))
	(T (substitute (car bindings) (cadr bindings) expression) )))

	;;call substitute on each list
	;;substitute should bind the car with the cdr

	;;Apply the bindings on the result of the recursive
;;	call on the cdr of the list

(defun evalexp (expression bindings)
		(cond
		((null bindings) expression)
		((listp (car bindings)) (simplify(cons (bind (cadr bindings) (bind (car bindings) (bind (caddr bindings) expression)))(cdddr bindings))))
		(T (simplify (bind bindings expression)))))





