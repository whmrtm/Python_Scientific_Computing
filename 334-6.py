# quantum physics
# plot (normalized) variational wavefunction against the true wavefunction
# from the citation .Gea-Banacloche, Am.  J. Phys.67, 776 (1999) 
# Calculate the probability for a particle in the best variational wavefunction to be in the true ground state,
# PHYS334 Assignment 6
from scipy.special import airy
from scipy.integrate import quad
from pylab import *

x = linspace(0, 20, 10000)

# exact solution
zn = 2.32
def new_airy(z):
    zn = 2.32
    return (airy(z-zn)[0])**2
coeff = quad(new_airy, 0, Inf)[0] ** (-0.5)
print("After normalization, the coefficient = " + str(coeff))
y = coeff*airy(x - zn)[0]


# variational method
A = 0.8735
yprime = 2*A**(1.5)*x*exp(-A*x)


## print the plots
figure()
plot(x,y,label="True wavefunction")
plot(x,yprime,label="Variational wavefunction")
xlabel("x")
ylabel("$\psi(x)$")
title("variation wavefunction & true wavefunction")
legend()
#y_div = true_divide(y,yprime)
#plot(x,y_div)
show()

        
# calculate the probability        
def F(z):
    zn = 2.32
    return (coeff*(airy(z-zn)[0])*2*A**(1.5)*z*exp(-A*z))**2
print("The probability is " + str(quad(F, 0, Inf)[0]))
        
    