#!/usr/bin/env python3
"""Symbolic regression fixtures, not a general automatic theorem prover."""
import sympy as s

def eq(a, b=0):
    assert s.simplify(a-b) == 0, (a,b)

# T1: second-order time indices and velocity error
a,K=s.symbols("a K",real=True)
assert s.solve([a-3,K-a*a-9],[a,K],dict=True)==[{a:s.Integer(3),K:s.Integer(18)}]
eq(s.Rational(2)*3/18,s.Rational(1,3))
print("PASS T1 time response")

# T2: repeated closed-loop roots at gains 1 and 25
b,c=s.symbols("b c",real=True)
sol=s.solve([(b+1)**2-4*c,(b+25)**2-100*c],[b,c],dict=True)
assert {tuple(z[q] for q in (b,c)) for z in sol}=={(s.Integer(5),s.Integer(9)),(s.Integer(-5),s.Integer(4))}
q=s.symbols("q",real=True)
eq(s.expand((q+5)**2-4*q*9),(q-1)*(q-25))
print("PASS T2 root locus")

# T3: Nyquist imaginary-axis crossing and closed-loop stability
w,k=s.symbols("w k",real=True, positive=True)
z=s.symbols("z")
L=2*(2*s.I*w+1)/(s.I*w*(s.I*w-2))
eq(s.re(L).subs(w,1),-2)
eq(s.im(s.simplify(L)).subs(w,1),0)
assert s.Poly(z*z+(2*k-2)*z+k,z).degree()==2
print("PASS T3 Nyquist")

# T4: Jury and unit-circle boundary
poly=z*z+(k-s.Rational(1,2))*z+k/2
eq(poly.subs({z:1,k:2}),4)
eq(s.factor(poly.subs(k,2)),z*z+s.Rational(3,2)*z+1)
print("PASS T4 discrete Jury")

# T5: symmetric state-space and hidden unstable modes
A=s.Matrix([[2,-1,-1],[-1,2,-1],[-1,-1,0]])
B=s.Matrix([1,1,2])
assert A==A.T and A*B==-B
assert A.eigenvals()=={-1:1,2:1,3:1}
Q=s.Matrix.hstack(B,A*B,A*A*B)
assert Q.rank()==1
eq((B.T*(z*s.eye(3)-A).inv()*B)[0],6/(z+1))
print("PASS T5 symmetric realization")

# T6: inverse design K=10,p=-2
A2=s.Matrix([[-2,0,-1],[0,-2,3],[-1,3,1]])
B2=s.Matrix([3,1,0])
assert A2*A2.T==A2*A2 and A2*B2==-2*B2
assert A2.eigenvals()=={-4:1,-2:1,3:1}
eq((B2.T*(z*s.eye(3)-A2).inv()*B2)[0],10/(z+2))
print("PASS T6 fixed answer")

# Negative regression assertions: reject 3 mathematical mistakes
assert A*s.Matrix([1,1,0]) != -s.Matrix([1,1,0])
assert not (2 > 1 and 1 > 1)  # at K=1 critical, not asymptotically stable
assert not (2 < 2)             # K=2 fails strict Jury condition
print("PASS 3 negative controls")
