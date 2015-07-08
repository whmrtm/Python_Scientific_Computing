from pylab import *
from sympy import *
import numpy as np

## Author: Heming Wang


## constants:
# N is the number of eigenstates
N = 200


## Initialization
# fai -> eigenstate
# A, A_d -> laddar operator
fai = np.zeros((N,N))
for i in range(N):
    fai[i] = np.zeros(N)
    fai[i][i] = 1

A = np.copy(fai)
A_d = np.copy(fai)

for i in range(N):
    if i == 0:
        A[i][0] = 0
    else:
        A[i] = sqrt(i)*fai[i-1]
A = A.transpose()

for i in range(N):
    if i<N-1:
        A_d[i] = sqrt(i+1)*fai[i+1]
    else:
        A_d[i][i] = 0
A_d = A_d.transpose()


## construct X and P in matrix
X = 1/sqrt(2)*(A + A_d)
P = I*1/sqrt(2)*(A - A_d)


## contruct Hamiltonian and estimate eigenvalues
# where H -> H     H_prime -> H'    H_dprime -> H''
H = 0.5 * X.dot(X) + 0.5*P.dot(P)
print("H is: " + str(H))
E0 = fai[0].dot(H).dot(fai[0].transpose())
print("E0 is: "+str(E0))
E1 = fai[1].dot(H).dot(fai[1].transpose())
print("E1 is: "+str(E1))

print("")

H_prime = 0.5*P.dot(P) + 4*0.5*X.dot(X)
print("H_prime is: " + str(H_prime)) 
E0_prime = fai[0].dot(H_prime).dot(fai[0].transpose())
print("E0_prime is: "+str(E0_prime))
E1_prime = fai[1].dot(H_prime).dot(fai[1].transpose())
print("E1_prime is: "+str(E1_prime))
print(linalg.eigvalsh(H_prime))
print("")

H_dprime = 0.5*P.dot(P) + 1.0*X.dot(X).dot(X).dot(X)
print("H_dprime is: " + str(H_dprime))
E0_dprime = fai[0].dot(H_dprime).dot(fai[0].transpose())
print("E0_dprime is: "+str(E0_dprime))
print(linalg.eigvalsh(H_dprime))

#print(H_dprime)  
#print(H_prime)