'''
Created on Sep 28, 2013

@author: alfredroney
'''
import numpy as np

def getMeanSquareDisplacement(x,n):
    ''' given (u,s): E[(x-x0)^2] = s^2*t + u^2*t^2 '''
    ni,nj = x.shape
    rv = np.zeros((n,nj))
    for i in range(ni-n):
        for j in range(n):
            rv[j,:] += np.square(x[i+j,:] - x[i,:])
    rv /= ni - n
    return rv
