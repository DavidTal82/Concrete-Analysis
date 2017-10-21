"""
This script extract abaqus odb results and calculate stress and strain

the script gets the path to the odb from 'path.txt'
"""
f = open('path.txt','r')

odbPath = f.readline()
jobName = f.readline()
scriptPath = f.readline()

f.close()
if odbPath[-1] == '\n': odbPath = odbPath[:-1] 
if jobName[-1] == '\n': jobName = jobName[:-1]

odbName = odbPath + '/' + jobName + '.odb'


from abaqus import *
from abaqusConstants import *
from odbAccess import* 
import numpy as np


resultsName = odbName[:-3] + 'txt'

Odb = openOdb(path = odbName)
#assembly = odb.rootAssembly
instance = Odb.rootAssembly.instances[ Odb.rootAssembly.instances.keys()[-1]]

minX = np.min([n.coordinates[0] for n in instance.nodes])
minY = np.min([n.coordinates[1] for n in instance.nodes])
minZ = np.min([n.coordinates[2] for n in instance.nodes])

maxX = np.max([n.coordinates[0] for n in instance.nodes])
maxY = np.max([n.coordinates[1] for n in instance.nodes])
maxZ = np.max([n.coordinates[2] for n in instance.nodes])

Lx = maxX - minX
Ly = maxY - minY
Lz = maxZ - minZ


Ay = np.pi * np.power(Lx, 2)
#Ax = Ly * Lz
#Az = Lx * Ly

# Getting the node sets in the odb file
nSet_Bottom = Odb.rootAssembly.nodeSets['SET-BOTTOM']
nSet_Top = Odb.rootAssembly.nodeSets['SET-TOP']

# Accessing the first step
firstStep = Odb.steps['Step-1']
# Getting the number of frames
nFrames = len(firstStep.frames)
# Declarting the displacement and force variables
Uy = np.zeros(nFrames)
Fy = np.zeros(nFrames)

#Ux = np.zeros(nFrames)
#Uz = np.zeros(nFrames)
#Fx = np.zeros(nFrames)
#Fz = np.zeros(nFrames)

#Getting force and displacement from all frames
for i in range(nFrames): 
    U = firstStep.frames[i].fieldOutputs['U']
    U2 = U.getScalarField(componentLabel='U2').getSubset(region=nSet_Top).values
    #U1 = U.getScalarField(componentLabel='U1').getSubset(region=nSetX_l).values
    #U3 = U.getScalarField(componentLabel='U3').getSubset(region=nSetZ_l).values
    Uy[i] = np.mean([u.data for u in U2])    
    #Ux[i] = np.mean([u.data for u in U1])
    #Uz[i] = np.mean([u.data for u in U3])
    
    # RF is the reaction force F = -RF    
    RF = firstStep.frames[i].fieldOutputs['RF']
    RF2 = RF.getScalarField(componentLabel='RF2').getSubset(region=nSet_Bottom).values
    #RF1 = RF.getScalarField(componentLabel='RF1').getSubset(region=nSetX_0).values
    #RF3 = RF.getScalarField(componentLabel='RF3').getSubset(region=nSetZ_0).values
    # F = - RF
    Fy[i] = -np.sum([f.data for f in RF2])    
    #Fx[i] = -np.sum([f.data for f in RF1])
    #Fz[i] = -np.sum([f.data for f in RF3])

#Calculating Strain and Stress
S22 = Fy/Ay
#S11 = Fx/Ax
#S33 = Fz/Az

E22 = Uy/Ly
#E11 = Ux/Lx
#E33 = Uz/Lz

Results = np.transpose([np.linspace(0,nFrames-1,nFrames), E22, S22, Uy, Fy])
                        
# Frame,   E22, S22, U2, F2
ResultsFormat = '%03d,    %1.3e,  %1.3e,  %1.3e,  %1.3e'
np.savetxt(resultsName, Results, fmt = ResultsFormat)

Odb.close()


