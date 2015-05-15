hasType(weight, double).
hasType(name, string).
hasType(void, void).

infer(Val, Y, X) :- hasType(Z, Y, X).

hasType(nameLen, string, integer).
hasType(getName, void, string).
hasType(getBMI, double, double).


canExecute(X, Y) :- hasType(Y, W), hasType(X, W, Z).

hasMethod(animal, getName).
hasMethod(animal, nameLen).
hasMethod(animal, getBMI).
hasMethod(X,Y) :- isSubclass(X,Z), hasMethod(Z,Y).

isSubclass(kitten, cat).
isSubclass(cat, animal).
hasSubclass(X,Y) :- isSubclass(Y,X).

/** a comment! **/


