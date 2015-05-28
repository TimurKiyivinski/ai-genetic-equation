#!/usr/bin/env python3

import random, copy

# Constants
TOKEN = 'X'
MINNO = 0
MAXNO = 256
TOKENS = ['+', '-', '*', '/', ' ', TOKEN]
NUMBERS = [str(i) for i in range(0, 256)]
ALLOWED = TOKENS + NUMBERS
NNUM = 0
NUNK = 1
NOPR = 2
GENRATE = 6
MUTRATE = 9

class Equation():
    class EquationNode:
        def __init__(self, value, ntype = NNUM):
            self.ntype = ntype
            if self.ntype < NOPR:
                self.value = float(value)
            else:
                self.value = str(value)
        def mutate(self):
            if self.ntype == NUNK:
                self.value = float(random.randrange(MINNO, MAXNO))
        def breed(self, partner):
            child = Equation.EquationNode(random.randrange(min(self.value, partner.value), max(self.value, partner.value)))
            return child
    def __init__(self, equation, nodes = []):
        self.equation = equation
        self.nodes = nodes
        if len(self.nodes) == 0:
            self.populate()
    # Create nodes based on equation
    def populate(self):
        self.nodes.clear()
        for c in self.equation.split():
            if c == TOKEN:
                self.nodes.append(self.EquationNode(random.randrange(MINNO, MAXNO), NUNK))
            elif c in TOKENS:
                self.nodes.append(self.EquationNode(c, NOPR))
            else:
                self.nodes.append(self.EquationNode(c))
    # Breed two equations by splitting and combining nodes
    def breed(self, partner):
        split = random.randrange(0, len(self.nodes))
        nodes = []
        for i in range(0, split):
            nodes.append(self.nodes[i])
        for i in range(split, len(self.nodes)):
            nodes.append(partner.nodes[i])
        newEquation = Equation(self.equation, nodes)
        return newEquation
    # Mutates all contained unknowns
    def mutate(self):
        unknowns = [t for t in self.nodes if t.ntype == NUNK]
        for t in unknowns:
            t.mutate()
    # Generates a string from nodes
    def str(self):
        equation = ''
        for n in self.nodes:
            equation += str(n.value)
        return equation
    # Evaluates the equation
    def get(self):
        return eval(self.str())
    
# Fitness function based on which equation has the closest outcome
def fitEquation(equations, outcome):
    roulette = random.uniform(0, outcome)
    for eq in equations:
        roulette -= abs(eq.get() - outcome)
        if roulette <= 0:
            return eq

def main():
    print('Please input any equation, followed by the expected outcome')
    print('Unknowns are to be presented with X')
    print('Allowed operators:\t+ | - | * | /')
    print('Number range:\t\t0-255')
    print('Example:\t\t2 + X - 4')
    print('Equation:')
    
    # Get the equation
    equation=input()
    
    print('Outcome:')
    
    # Get the outcome
    outcome=input()


    print('The input equation is %s = %s' % (equation, outcome))

    # Check syntax
    hasToken = False
    # Look if character in equation is allowed
    for c in equation:
        if not c in ALLOWED:
            print('Error detected parsing token: %s' % c)
            return 'Invalid equation.'
        # Check if equation contains a TOKEN
        if c == TOKEN:
            hasToken = True
    if not hasToken:
        print('At least one unknown is expected.')
    if not outcome in NUMBERS:
        return 'Invalid outcome.'
    
    # Generate equation class
    userEquations = []
    userEquation = Equation(equation)
    userEquations.append(userEquation)
    for i in range(0, GENRATE):
        newEquation = Equation(equation)
        newEquation.mutate()
        userEquations.append(newEquation)

    # Keep evolving until a solution is found
    solved = False
    solution = False
    generations = 0
    while not solved:
        print('Currently at generation %i' % generations)

        # Check for solution
        for eq in userEquations:
            if eq.get() == float(outcome):
                solved = True
                solution = eq
                break
        
        pairA = []
        pairB = []
        for i in range(0, GENRATE):
            pairA.append(fitEquation(userEquations, float(outcome)))
            pairB.append(fitEquation(userEquations, float(outcome)))
        
        newEquations = []
        for i in range(0, GENRATE):
            newEquation = copy.deepcopy(pairA[i].breed(pairB[i]))
            if random.randrange(0, 10) % MUTRATE == 1:
                newEquation.mutate()
            newEquations.append(newEquation)
        
        userEquations = newEquations
 
        generations += 1
 
    print('Solution equation is: %s' % solution.str())

if __name__ == '__main__':
    quit(main())
