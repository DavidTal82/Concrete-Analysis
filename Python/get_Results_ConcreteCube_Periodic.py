"""
This script extract abaqus odb results and calculate stress and strain

the script gets the path to the odb from 'path.txt'
"""
f = open('path.txt','r')

odbPath = f.readline()
jobName = f.readline()
resultsName = f.readline()

f.close()

if odbPath[-1] == '\n': odbPath = odbPath[:-1]
    
if jobName[-1] == '\n': jobName = jobName[:-1]

if resultsName[-1] == '\n': resultsName = resultsName[:-1]

odbName = odbPath + '/' + jobName + '.odb'


from abaqus import *
from abaqusConstants import *
from odbAccess import* 
import numpy as np

Odb = openOdb(path = odbName)
#assembly = odb.rootAssembly
instance = Odb.rootAssembly.instances['PART-1-1']

minX = np.min([n.coordinates[0] for n in instance.nodes])
minY = np.min([n.coordinates[1] for n in instance.nodes])
minZ = np.min([n.coordinates[2] for n in instance.nodes])

maxX = np.max([n.coordinates[0] for n in instance.nodes])
maxY = np.max([n.coordinates[1] for n in instance.nodes])
maxZ = np.max([n.coordinates[2] for n in instance.nodes])

Lx = maxX - minX
Ly = maxY - minY
Lz = maxZ - minZ

Ax = Ly * Lz
Ay = Lx * Lz
Az = Lx * Ly

# Getting the node sets in the odb file
nSetX_0 = Odb.rootAssembly.nodeSets['SET-X_0']
nSetX_l = Odb.rootAssembly.nodeSets['SET-X_L']
nSetY_0 = Odb.rootAssembly.nodeSets['SET-Y_0']
nSetY_l = Odb.rootAssembly.nodeSets['SET-Y_L']
nSetZ_0 = Odb.rootAssembly.nodeSets['SET-Z_0']
nSetZ_l = Odb.rootAssembly.nodeSets['SET-Z_L']
nSetRef1 = Odb.rootAssembly.nodeSets['REFPOINT-0']
nSetRef2 = Odb.rootAssembly.nodeSets['REFPOINT-1']
nSetRef3 = Odb.rootAssembly.nodeSets['REFPOINT-2']

# Accessing the first step
firstStep = Odb.steps['Step-1']
# Getting the number of frames
nFrames = len(firstStep.frames)
# Declarting the displacement and force variables
Ux = np.zeros(nFrames)
Uy = np.zeros(nFrames)
Uz = np.zeros(nFrames)
Fx = np.zeros(nFrames)
Fy = np.zeros(nFrames)
Fz = np.zeros(nFrames)


#Getting force and displacement from all frames
for i in range(nFrames):
	U = firstStep.frames[i].fieldOutputs['U']
	U1_l = U.getScalarField(componentLabel='U1').getSubset(region=nSetX_l).values
	U1_0 = U.getScalarField(componentLabel='U1').getSubset(region=nSetX_0).values
	U2_l = U.getScalarField(componentLabel='U2').getSubset(region=nSetY_l).values
	U2_0 = U.getScalarField(componentLabel='U2').getSubset(region=nSetY_0).values
	U3_l = U.getScalarField(componentLabel='U3').getSubset(region=nSetZ_l).values
	U3_0 = U.getScalarField(componentLabel='U3').getSubset(region=nSetZ_0).values
	Ux[i] = np.mean([u.data for u in U1_l]) - np.mean([u.data for u in U1_0])
	Uy[i] = np.mean([u.data for u in U2_l]) - np.mean([u.data for u in U2_0])
	Uz[i] = np.mean([u.data for u in U3_l]) - np.mean([u.data for u in U3_0])
	# RF is the reaction force F = -RF
	RF = firstStep.frames[i].fieldOutputs['RF']
	RF1 = RF.getScalarField(componentLabel='RF1').getSubset(region=nSetRef1).values
	RF2 = RF.getScalarField(componentLabel='RF2').getSubset(region=nSetRef2).values
	RF3 = RF.getScalarField(componentLabel='RF3').getSubset(region=nSetRef3).values
	# F = - RF
	Fx[i] = np.sum([f.data for f in RF1])
	Fy[i] = np.sum([f.data for f in RF2])
	Fz[i] = np.sum([f.data for f in RF3])

#Calculating Strain and Stress
S11 = Fx/Ax
S22 = Fy/Ay
S33 = Fz/Az

E11 = Ux/Lx
E22 = Uy/Ly
E33 = Uz/Lz

Results = np.transpose([np.linspace(0,nFrames-1,nFrames), E11, E22, E33,
                        S11, S22, S33, Ux, Uy, Uz, Fx, Fy, Fz])
                        
# Frame,   E11, E22, E33, S11, S22, S33, U1, U2, U3, F1, F2, F3
ResultsFormat = '%03d,    %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e'
np.savetxt(resultsName, Results, fmt = ResultsFormat)

Odb.close()

