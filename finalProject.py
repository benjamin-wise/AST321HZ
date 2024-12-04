# -*- coding: utf-8 -*-
"""
Benjamin Wise
AST 321 Final Project Graphs
Based off Dr. Young's Code for Coding Assignment 5
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

#starName = ['hr.0A', 'hr.1A','hr.2A', 'hr.5A', 'hr.6A', 'hr.7A', 'hr.8A', 'hr.9A'] #hot to cold order
#starName = ['hr.9A', 'hr.8A','hr.7A', 'hr.6A', 'hr.5A', 'hr.2A', 'hr.1A', 'hr.0A'] #cold to hot order
#starName = ['hr.5A', 'hr.6A','hr.7A', 'hr.8A', 'hr.9A', 'hr.0A', 'hr.1A', 'hr.2A'] #least to most massive
starName = ['hr.2A', 'hr.1A','hr.0A', 'hr.9A', 'hr.8A', 'hr.7A', 'hr.6A', 'hr.5A'] #most to least massive

starMass = [1,2,3,4,5,6,7,8]#getting the mass for the stars, calculated independently so various orders can be used
s = 0
for s in range(8):
    match starName[s]:
        case 'hr.2A':
            starMass[s] = 1.2
        case 'hr.1A':
            starMass[s] = 1.1
        case 'hr.0A':
            starMass[s] = 1.0
        case 'hr.9A':
            starMass[s] = 0.9
        case 'hr.8A':
            starMass[s] = 0.8
        case 'hr.7A':
            starMass[s] = 0.7
        case 'hr.6A':
            starMass[s] = 0.6
        case 'hr.5A':
            starMass[s] = 0.5

#for holding rgb values of proper colors
colorsList = ['#ff00ff','#8a2be2','#0000ff','#00ffff','#00ff00','#f0c700','#ff7f00','#ff0000']

#for holding symbols for datapoints so that colorblind people can still tell data apart
markersList = ['v','<','^','>','d','s','o','x']

#for standard graph size
stdX = 8
stdY = 8

#this holds the names of each of the stars as their stellar classifications
stellarModel = []
#this holds the files for each of the stars, directly corresponding to the names from starName
    
#Code reads in log(temperature) (T), log(luminosity/Lsol) (L), time in seconds (t), and stellar radius in cm (r).
T_array_hr = [[],[],[],[],[],[],[],[]]
L_array_hr = [[],[],[],[],[],[],[],[]]
t_array_hr = [[],[],[],[],[],[],[],[]]
r_array_hr = [[],[],[],[],[],[],[],[]]
#I'm using the same name formatting as the professor-provided ones for fun
Si_array_hr = [[],[],[],[],[],[],[],[]]#inner flux (effective)
So_array_hr = [[],[],[],[],[],[],[],[]]#outer flux (effective)
Di_array_hr = [[],[],[],[],[],[],[],[]]#distance of inner edge of habitable zone
Do_array_hr = [[],[],[],[],[],[],[],[]]#distance of outer edge of habitable zone
y_array_hr = [[],[],[],[],[],[],[],[]]#time in years
Tr_array_hr = [[],[],[],[],[],[],[],[]]#temperature* for the flux equation
    
#various constants required for the effective flux eq
seffSolInner = float(1.107)#value of effective flux for Sol (inner)
seffSolOuter = float(0.356)#value of effective flux for Sol (outer)
aInner = float(1.332*float(10**(-4)))
aOuter = float(6.171*float(10**(-5)))
bInner = float(1.580*float(10**(-8)))
bOuter = float(1.698*float(10**(-9)))
cInner = float(-8.308*float(10**(-12)))
cOuter = float(-3.198*float(10**(-12)))
dInner = float(-1.931*float(10**(-15)))
dOuter = float(-5.575*float(10**(-16)))

starNum = 0
for starNum in range(8):#for each of the stars
    stellarModel.append(open(starName[starNum],'r'))#open the file
    
starNum = 0
for starNum in range(8):
    i = 1
    tstep = 0

    #I don't really know exactly what these two lines do, they're from the professors code, and I didn't mess with them very much
    dataframe_hr = pd.read_table(stellarModel[starNum],delim_whitespace=True,names=np.arange(14))
    nrows = np.shape(dataframe_hr)[0]
    
    for i in range(nrows):
            if i%19 == 0:
                #T_array_hr[starNum].append(dataframe_hr[8][i]) #dont use this actually, use the un-logged version
                T_array_hr[starNum].append(float(10**(dataframe_hr[8][i])))
                #L_array_hr[starNum].append(dataframe_hr[7][i]) #dont use this actually, use the un-logged version
                L_array_hr[starNum].append(float(10**(dataframe_hr[7][i])))
                t_array_hr[starNum].append(float(dataframe_hr[2][i]))
                r_array_hr[starNum].append(float(dataframe_hr[4][i]))
    j = 0
    tempTemp = float(0)
    for j in range(len(T_array_hr[starNum])):
        #calculating the reduced temperature
        Tr_array_hr[starNum].append(float((T_array_hr[starNum][j]) - 5780))
        #calculating flux of habitable zone edges (i for inner, o for outer) from reduced Temperature and the given constants
        Si_array_hr[starNum].append(float(seffSolInner + float(aInner*(Tr_array_hr[starNum][j])) + float(bInner*((Tr_array_hr[starNum][j])**2)) + float(cInner*((Tr_array_hr[starNum][j])**3)) + float(dInner*((Tr_array_hr[starNum][j])**4))))
        So_array_hr[starNum].append(float(seffSolOuter + float(aOuter*(Tr_array_hr[starNum][j])) + float(bOuter*((Tr_array_hr[starNum][j])**2)) + float(cOuter*((Tr_array_hr[starNum][j])**3)) + float(dOuter*((Tr_array_hr[starNum][j])**4))))
        #calculating distance of habitable zone edges(i for inner, o for outer) from flux and luminosity
        Di_array_hr[starNum].append(float(float((L_array_hr[starNum][j])/(Si_array_hr[starNum][j]))**(float(0.5))))
        Do_array_hr[starNum].append(float(float((L_array_hr[starNum][j])/(So_array_hr[starNum][j]))**(float(0.5))))
        #calculating time in terms of years
        y_array_hr[starNum].append(float((t_array_hr[starNum][j])/float(365*24*60*60)))
                

    stellarModel[starNum].close()#close the file since we dont need the data and dont want io errors
    
starNum = 0    
for starNum in range(8):

    #graphing individual HR diagrams
    fig, ax = plt.subplots()
    ax.plot(T_array_hr[starNum],L_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax.set_title('HR Diagram for ' + starName[starNum] + ' with ' + str(starMass[starNum]) + ' Solar Masses')
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Luminosity (L/sol L)')
    #ax.set_yscale('log')
    #ax.set_xlim(3.775,3.62) #this was for log scale
    bax = ax.secondary_xaxis('top',transform=ax.transData)
    cax = ax.secondary_yaxis('right',transform=ax.transData)
    ax.grid(True,'both','both')
    ax.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax.yaxis.set_minor_locator(AutoMinorLocator(6))
    ax.tick_params(axis='both',which='major',grid_linewidth=2)
    ax.invert_xaxis()#HR diagrams are weird in terms of axis
    fig.set_size_inches(stdX,stdY)
    
    #graphing individual evolution
    fig2, ax2 = plt.subplots()
    ax2.plot(t_array_hr[starNum],r_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax2.set_title('Stellar Evolution Track for ' + starName[starNum] + ' with ' + str(starMass[starNum]) + ' Solar Masses')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Stellar Radius (cm)')
    ax2.set_xscale('log')
    bax2 = ax2.secondary_xaxis('top',transform=ax2.transData)
    cax2 = ax2.secondary_yaxis('right',transform=ax2.transData)
    ax2.grid(True,'both','both')
    ax2.yaxis.set_minor_locator(AutoMinorLocator(6))
    ax2.tick_params(axis='both',which='major',grid_linewidth=2)
    fig2.set_size_inches(stdX,stdY)
    
    #graphing individual luminosity
    fig3, ax3 = plt.subplots()
    ax3.plot(y_array_hr[starNum],L_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax3.set_title('Luminosity over Time of ' + starName[starNum] + ' with ' + str(starMass[starNum]) + ' Solar Masses')
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('Luminosity (L/sol L)')
    bax3 = ax3.secondary_xaxis('top',transform=ax3.transData)
    cax3 = ax3.secondary_yaxis('right',transform=ax3.transData)
    ax3.grid(True,'both','both')
    ax3.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax3.yaxis.set_minor_locator(AutoMinorLocator(6))
    ax3.tick_params(axis='both',which='major',grid_linewidth=2)
    fig3.set_size_inches(stdX,stdY)
    
    #graphing individual temperatures
    fig4, ax4 = plt.subplots()
    ax4.plot(y_array_hr[starNum],T_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax4.set_title('Temperature over Time of ' + starName[starNum] + ' with ' + str(starMass[starNum]) + ' Solar Masses')
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Temperature (K)')
    bax4 = ax4.secondary_xaxis('top',transform=ax4.transData)
    cax4 = ax4.secondary_yaxis('right',transform=ax4.transData)
    ax4.grid(True,'both','both')
    ax4.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax4.yaxis.set_minor_locator(AutoMinorLocator(6))
    ax4.tick_params(axis='both',which='major',grid_linewidth=2)
    fig4.set_size_inches(stdX,stdY)
    
    #graphing individual habitable zones
    fig5,ax5 = plt.subplots()
    ax5.plot(y_array_hr[starNum],Di_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax5.plot(y_array_hr[starNum],Do_array_hr[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    ax5.set_title('Distance of Habitable Zone for ' + starName[starNum] + ' with ' + str(starMass[starNum]) + ' Solar Masses')
    ax5.set_xlabel('Time (years)')
    ax5.set_ylabel('Distance (AU)')
    bax5 = ax5.secondary_xaxis('top',transform=ax5.transData)
    cax5 = ax5.secondary_yaxis('right',transform=ax5.transData)
    ax5.fill_between(y_array_hr[starNum],Di_array_hr[starNum],Do_array_hr[starNum], alpha=.1, linewidth=0,color=colorsList[starNum])
    ax5.grid(True,'both','both')
    ax5.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax5.yaxis.set_minor_locator(AutoMinorLocator(6))
    ax5.tick_params(axis='both',which='major',grid_linewidth=2)
    #ax5.legend(loc='center right')
    fig5.set_size_inches(stdX,stdY)
    
    plt.show()

#more complex graphs need larger sizes
largeX = 15
largeY = 15

#graphing consolidated temperature(T), luminosity(L), habitable zones (D), and HR lines (HR)

#graph formatting
figT,axT = plt.subplots()
axT.set_title('Temperature over Time for all Stars in Set')
axT.set_xlabel('Time (seconds)')
axT.set_ylabel('Temperature (K)')
axT.set_xscale('log')
axT.secondary_xaxis('top',transform=axT.transData)
axT.secondary_yaxis('right',transform=axT.transData)
figT.set_size_inches(largeX,largeY)

figL,axL = plt.subplots()
axL.set_title('Luminosity over Time for all Stars in Set')
axL.set_xlabel('Time (seconds)')
axL.set_ylabel('Luminosity (L/sol L)')
axL.set_xscale('log')
axL.secondary_xaxis('top',transform=axL.transData)
axL.secondary_yaxis('right',transform=axL.transData)
figL.set_size_inches(largeX,largeY)

figD,axD = plt.subplots()
axD.set_title('Habitable Zones over Time for all Stars in Set')
axD.set_xlabel('Time (seconds)')
axD.set_ylabel('Distance to Habitable Zone (AU)')
axD.set_xscale('log')
axD.secondary_xaxis('top',transform=axD.transData)
axD.secondary_yaxis('right',transform=axD.transData)
figD.set_size_inches(largeX,largeY)

figHR,axHR = plt.subplots()
axHR.set_title('HR Diagram for all Stars in Set')
axHR.set_xlabel('Temperature (K)')
axHR.set_ylabel('Luminosity (L/sol L)')
axHR.secondary_xaxis('top',transform=axHR.transData)
axHR.secondary_yaxis('right',transform=axHR.transData)
#axL.set_yscale('log')
axHR.invert_xaxis()#HR diagrams are weird in terms of axis
figHR.set_size_inches(largeX,largeY)

starNum = 0
for starNum in range(8):#adding all of the data to the big graphs
    axT.plot(t_array_hr[starNum],T_array_hr[starNum],label=starName[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    axL.plot(t_array_hr[starNum],L_array_hr[starNum],label=starName[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])
    axD.plot(t_array_hr[starNum],Di_array_hr[starNum],label=starName[starNum],color=colorsList[starNum],linestyle='dashed',linewidth=1,marker=markersList[starNum])
    axD.plot(t_array_hr[starNum],Do_array_hr[starNum],color=colorsList[starNum],linestyle='dotted',linewidth=1,marker=markersList[starNum])
    axD.fill_between(t_array_hr[starNum],Di_array_hr[starNum],Do_array_hr[starNum], alpha=.1, linewidth=0,color=colorsList[starNum])
    axHR.plot(T_array_hr[starNum],L_array_hr[starNum],label=starName[starNum],color=colorsList[starNum],linewidth=1,marker=markersList[starNum])

#more graph formatting
axT.legend(loc='upper right')
axT.grid(True,'both','both')
axT.yaxis.set_minor_locator(AutoMinorLocator(6))
axT.tick_params(axis='both',which='major',grid_linewidth=2)

axL.legend(loc='upper right')
axL.grid(True,'both','both')
axL.yaxis.set_minor_locator(AutoMinorLocator(6))
axL.tick_params(axis='both',which='major',grid_linewidth=2)

axD.legend(loc='upper right')
axD.grid(True,'both','both')
axD.yaxis.set_minor_locator(AutoMinorLocator(6))
axD.tick_params(axis='both',which='major',grid_linewidth=2)

axHR.legend(loc='upper right')
axHR.grid(True,'both','both')
axHR.xaxis.set_minor_locator(AutoMinorLocator(6))
axHR.yaxis.set_minor_locator(AutoMinorLocator(6))
axHR.tick_params(axis='both',which='major',grid_linewidth=2)

plt.show()
