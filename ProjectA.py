#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 10:18:36 2024


"""

import math
import matplotlib.pyplot as plt
"""
The function of main is to define the intial parameters
of the dynamics of the two molecules across the two compartments
It also defines simulate with these parameters
"""
def main():
    
    # Use these initial conditions for the application
    initial_B1_fast, initial_B1_slow = 200, 200
    initial_B2_fast, initial_B2_slow = 1, 1
    initial_P_fast, initial_P_slow = 0.01, 0.01
    sB2fast = 0.2  # B2 sensitivity parameter for fast compartment
    sB2slow = 0.1  # B2 sensitivity parameter for slow compartment
    sB1fast = 0.01  # B1 effectiveness parameter for fast compartment
    sB1slow = 0.005  # B1 effectiveness parameter for slow compartment
    B1p = 80  # Plasma B1 concentration
    B1t = 20  # Target B1 concentration
    delay_fast = 5  # Time delay for B2 action in fast compartment
    delay_slow = 20 # Time delay for B2 action in slow compartment
    beta = 3 # use 3 for normal and 1 for disease
    B1thres = 150
    
    dt = 0.1
    total_time = 60
    
    simulate(initial_B1_fast, initial_B1_slow,initial_B2_fast, 
                  initial_B2_slow,initial_P_fast, initial_P_slow,
                  sB2fast, sB2slow, sB1fast, sB1slow, B1p, B1t, 
                  delay_fast,delay_slow,beta, B1thres,dt,total_time)
    
 
"""These next 4 functions define the rate of change of B1 or B2 
concentration in fast and slow compartments. Molecule1 parameters is 
sensitivity, current concentration of B1 and B2, plasma B1 concentration and
production rate. The return value of the B1 concentration was d_B1slow or d_b1fast
Parameters of molecule2 was time delay, sensitivity parameter, current B1 and B2 
concentration and target B1 concentration. The return value was d_B2fast or d_B2 slow"""         

def molecule1_dynam_fast(sB1fast,B1fast, B1p, B2fast, Pfast):
    
    # ADD YOUR CODE
    dB1fast_dt = -sB1fast * (B1fast - B1p) - B2fast * B1fast + Pfast
    return dB1fast_dt


def molecule1_dynam_slow(sB1slow,B1slow, B1p, B2slow, Pslow):
    
    # ADD YOUR CODE 
    dB1slow_dt = -sB1slow * (B1slow - B1p) - B2slow * B1slow + Pslow
    return dB1slow_dt


def molecule2_dynam_fast(delay_fast,sB2fast,B1fast, B2fast,B1t):
    
    # ADD YOUR CODE
    dB2fastdt = (1 / delay_fast) * (sB2fast * (B1fast - B1t) - B2fast)
    return dB2fastdt


def molecule2_dynam_slow(delay_slow,sB2slow,B1slow, B2slow,B1t):
    
    # ADD YOUR CODE
    dB2slow_dt = (1 / delay_slow) * (sB2slow * (B1slow - B1t) - B2slow)
    return dB2slow_dt

""" Purpose of the next two functions is to find the rate of change in P for 
B2 in the fast and slow compartments with respect to B1 concentration threshold.
"""
def molecule2_sec_fast(beta,B1fast, B1thres,Pfast,t):
    
    # ADD YOUR CODE
    dPfastdt = beta * max(0, B1fast - B1thres) * Pfast * math.sin(0.1 * t)
    return dPfastdt


def molecule2_sec_slow(beta, B1slow, B1thres, Pslow,t):
    dPslowdt = beta * max(0, B1slow - B1thres) * Pslow * math.cos(0.1 * t)
    return dPslowdt
    
    # ADD YOUR CODE
"""
These last 6 functions are meant to update the concentration of B1 or B2 or P
in the fast or slow compartment using rate of change given by dB1fast or slow, 
you took the db or the derivative to find the rate of change of hte function.
The parameters of the function to calculate the rate of change in respect to 
senstivity, delay, current concentrations and time step dt. This show return an
updaated concentration of the molecule or P secretory factor within the given 
compartment"""

def update_mol1_fast(fun,sB1fast,B1fast, B1p, B2fast, Pfast,dt):
    
    # ADD YOUR CODE
    dB1fast = fun(sB1fast, B1fast, B1p, B2fast, Pfast) 
    B1fast_update = B1fast + (dB1fast * dt)   
    return B1fast_update

def update_mol1_slow(fun,sB1slow,B1slow, B1p, B2slow, Pslow,dt):
    
    # ADD YOUR CODE
    dB1slow = fun(sB1slow, B1slow, B1p, B2slow, Pslow)
    B1slow_update = B1slow + (dB1slow * dt)  
    return B1slow_update

def update_mol2_fast(fun,delay_fast,sB2fast,B1fast, B2fast,B1t,dt):
    
    # ADD YOUR CODE
    dB2fast = fun(delay_fast, sB2fast, B1fast, B2fast, B1t)
    B2fast_update = B2fast + (dB2fast * dt)
    return B2fast_update

def update_mol2_slow(fun,delay_slow,sB2slow,B1slow, B2slow,B1t,dt):
    
    # ADD YOUR CODE
    dB2slow = fun(delay_slow, sB2slow, B1slow, B2slow, B1t)
    B2slow_update = B2slow + (dB2slow * dt) 
    return B2slow_update

def update_mol2_sec_fast(fun,beta,B1fast, B1thres,Pfast,t,dt):
    
    # ADD YOUR CODE
    dPfast = fun(beta, B1fast, B1thres, Pfast, t)
    Pfast_update = Pfast + (dPfast * dt)
    return Pfast_update

def update_mol2_sec_slow(fun,beta, B1slow, B1thres, Pslow,t,dt):
    
    # ADD YOUR CODE
    dPslow = fun(beta, B1slow, B1thres, Pslow, t)
    Pslow_update = Pslow + (dPslow * dt)
    return Pslow_update
"""  
Simulate's purpose is to update the concentration in both fast and 
slow compartments within the parameters
Parameters are the initial concentrations for B1 and B2 in both 
compartments, sensitivity and effectiveness paramters for both
molecules in both compartments, concentration of B1 in plasma, time delays for
B2 in both compartments, beta ability to conrol secretion, B1 concentration threshold 
and time step and total time.Time was set to 0. The while loop 
updated the B1, B2 and P in fast and slow compartments to
have the return value is ax object for plotting.

The application plot creates a graph to B1 and B2 molecules in both compartments to 
indicat B1, B2  in both compartments given t time to show how molecules B1 and B2 are 
interacting within different compartments given their differential equation / rate
of change
"""
def simulate(initial_B1_fast, initial_B1_slow,initial_B2_fast, 
             initial_B2_slow,initial_P_fast, initial_P_slow,
             sB2fast, sB2slow, sB1fast, sB1slow, B1p, B1t, 
             delay_fast,delay_slow,beta, B1thres,dt,total_time):
    

    fig, ax = plt.subplots(1,2,figsize=(15, 7))

    #### ADD YOUR CODE BELOW ####
    
    B1fast = initial_B1_fast
    B1slow = initial_B1_slow
    B2fast = initial_B2_fast
    B2slow = initial_B2_slow
    Pfast = initial_P_fast
    Pslow = initial_P_slow
    t = 0

    while t <= total_time + dt:
        plot_result(ax, B1fast, B1slow, B2fast, B2slow, t)  
        
        B1fast_updated = update_mol1_fast(molecule1_dynam_fast, sB1fast, B1fast, B1p, B2fast, Pfast, dt)
        B1slow_updated = update_mol1_slow(molecule1_dynam_slow, sB1slow, B1slow, B1p, B2slow, Pslow, dt)
        B2fast_updated = update_mol2_fast(molecule2_dynam_fast, delay_fast, sB2fast, B1fast, B2fast, B1t, dt)
        B2slow_updated = update_mol2_slow(molecule2_dynam_slow, delay_slow, sB2slow, B1slow, B2slow, B1t, dt)
        Pfast_updated = update_mol2_sec_fast(molecule2_sec_fast, beta, B1fast, B1thres, Pfast, t, dt)
        Pslow_updated = update_mol2_sec_slow(molecule2_sec_slow, beta, B1slow, B1thres, Pslow, t, dt)
        
        B1fast = B1fast_updated
        B1slow = B1slow_updated
        B2fast = B2fast_updated
        B2slow = B2slow_updated
        Pfast = Pfast_updated
        Pslow = Pslow_updated
        
        t += dt

    plt.show()

      
    
    # Do not modify this return statement
    # This should ramain the last statement in
    # the simulate function
    return ax
    
    




    


### DO NOT CHANGE THIS FUNCTION ####  
### Use this function  in your simulate function 
### to plot the concentrations of B1 and B2 molecules 

def plot_result(ax,B1fast,B1slow,B2fast,B2slow,t):
    """
    Plot the concentrations of B1 and B2 over time.

    Parameters
    ----------
    ax : list of matplotlib.axes.Axes
        List containing two Axes objects for plotting B1 and B2 concentrations.
    B1fast : float
        Concentration of B1 in the fast compartment at time t.
    B1slow : float
        Concentration of B1 in the slow compartment at time t.
    B2fast : float
        Concentration of B2 in the fast compartment at time t.
    B2slow : float
        Concentration of B2 in the slow compartment at time t.
    t : float
        Time value for which concentrations are plotted.

    Returns
    -------
    None

    Notes
    -----
    This function plots the concentrations of B1 and B2 in the fast and slow compartments at a particular time point.
    """
    
    
    ax[0].plot(t, B1fast, 'bo')
    ax[0].plot(t, B1slow, 'go')
    ax[1].plot(t, B2fast, 'ro')
    ax[1].plot(t, B2slow, 'mo')
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('B1 Concentration')
    
    ax[0].set_title(f'Complex B1 Response Model at Time: {t:.1f}')
    
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('B2 Concentration')
    
    ax[1].set_title(f'Complex B2 Response Model at Time: {t:.1f}')
    
    # Uncomment to see an animation of B1 and B2 
    # concentrations at each time point as opposed
    # to see all at the end of the simulation
    # plt.pause(0.0001)  # Pause
    
    ax[0].legend(['B1 (Fast)','B1 (Slow)'],loc=1)
    ax[1].legend(['B2 (Fast)','B2 (Slow)'],loc=1)
   



if __name__ == '__main__':
    
    main()
    
    # You could test your individual functions here
    
    