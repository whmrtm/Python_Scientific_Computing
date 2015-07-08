import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

x = np.arange(0,20,0.01)
a0 = 1
def P10(u):
    return 4*u**2*np.exp(-2*u)
def P20(u):
    return 0.5*u**(2)*(1-0.5*u)**2*np.exp(-u) 
def P21(u):
    return 1.0/24.0*(u**4)*np.exp(-u)
 
print(quad(P10,0,2)[0])
print(quad(P20,0,2)[0])
print(quad(P21,0,2)[0])
plt.plot(x,P10(x),label="P10")
plt.plot(x,P20(x),label="P20")
plt.plot(x,P21(x),label="P21")
plt.xlabel('r')
plt.ylabel('P')
plt.legend()
plt.show()
