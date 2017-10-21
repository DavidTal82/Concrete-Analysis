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
E11 = np.zeros(nFrames)
E22 = np.zeros(nFrames)
E33 = np.zeros(nFrames)
S11 = np.zeros(nFrames)
S22 = np.zeros(nFrames)
S33 = np.zeros(nFrames)


#Getting force and displacement from all frames
for i in range(nFrames):
	LE = firstStep.frames[i].fieldOutputs['LE']
	PE = firstStep.frames[i].fieldOutputs['PE']
	S = firstStep.frames[i].fieldOutputs['S']
	LE11_v = LE.getScalarField(componentLabel='LE11').values
	LE22_v = LE.getScalarField(componentLabel='LE22').values
	LE33_v = LE.getScalarField(componentLabel='LE33').values
	PE11_v = PE.getScalarField(componentLabel='PE11').values
	PE22_v = PE.getScalarField(componentLabel='PE22').values
	PE33_v = PE.getScalarField(componentLabel='PE33').values
	S11_v = S.getScalarField(componentLabel='S11').values
	S22_v = S.getScalarField(componentLabel='S22').values
	S33_v = S.getScalarField(componentLabel='S33').values
	E11[i] = np.mean([le11.data for le11 in LE11_v]) + np.mean([pe11.data for pe11 in PE11_v])
	E22[i] = np.mean([le22.data for le22 in LE22_v]) + np.mean([pe22.data for pe22 in PE22_v])
	E33[i] = np.mean([le33.data for le33 in LE33_v]) + np.mean([pe33.data for pe33 in PE33_v])
	S11[i] = np.mean([s11.data for s11 in S11_v])
	S22[i] = np.mean([s22.data for s22 in S22_v])
	S33[i] = np.mean([s33.data for s33 in S33_v])

Results = np.transpose([np.linspace(0,nFrames-1,nFrames), E11, E22, E33,
                        S11, S22, S33])
                        
# Frame,   E11, E22, E33, S11, S22, S33
ResultsFormat = '%03d,    %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e,  %1.3e'
np.savetxt(resultsName, Results, fmt = ResultsFormat)

Odb.close()

