# -*- coding: utf-8 -*-
"""
Model Construction
Created on Fri Aug 19 15:02:24 2016

@author: operator
"""

import numpy as np

from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *


######################
#Mesh path and load
######################
MeshPath = 'C:/Users/operator/Documents/MATLAB/MATLAB_Research/Concrete_Analysis/Data/UC/Testing/'

Nodes = np.loadtxt(MeshPath + '/Nodes.txt', delimiter=",")
Elements = np.loadtxt(MeshPath + '/Elements.txt', delimiter=",").astype(int)

UC_boundary = np.concatenate(([np.amin(Nodes[:,1:], axis=0)], 
                               [np.amax(Nodes[:,1:], axis=0)]), axis=0)

dU1 = 0.2 * UC_boundary[1,0]
dU2 = 0.2 * UC_boundary[1,1]
dU3 = 0.2 * UC_boundary[1,2]

#Creating an empty Mdb object
Mdb()
execfile('AbaqusScriptFuncDUDU.py')

###############################################################################
#CREATE PART
###############################################################################
#Creating a 3D deformable part
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-2', type=
    DEFORMABLE_BODY)
    
    
###############################################################################
#CREATE MESH PART - the mesh is in the part not the assembly
###############################################################################
for n in Nodes:
    mdb.models['Model-1'].parts['Part-2'].Node(coordinates = n[1:],
        label = int(n[0]))
        
[num_el,num_nodes_in_el] = Elements.shape

num_el = int(num_el)
num_nodes_in_el = int(num_nodes_in_el)
num_nodes_in_el -= 1

#Generating mesh
for el in Elements:
    el_label = el[0]#elemnt label
    nodesArray = []    
    
    for n in el[1:]:
        nodesArray.append(mdb.models['Model-1'].parts['Part-2'].nodes.getFromLabel(n))
        
    mdb.models['Model-1'].parts['Part-2'].Element(nodes = nodesArray,
        elemShape = TET4, label = el_label )
    

###############################################################################
#DEFINE MATERIAL AND SECTION 
###############################################################################
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((1.0, 0.3), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)

mdb.models['Model-1'].Material(name='Material-2')
mdb.models['Model-1'].materials['Material-2'].Elastic(table=((1.0, 0.3), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-2', name=
    'Section-2', thickness=None)
    
    
mdb.models['Model-1'].parts['Part-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    elements=mdb.models['Model-1'].parts['Part-2'].elements), 
    sectionName='Section-1', thicknessAssignment=FROM_SECTION)
    
mdb.models['Model-1'].parts['Part-2'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    elements=mdb.models['Model-1'].parts['Part-2'].elements), 
    sectionName='Section-2', thicknessAssignment=FROM_SECTION)

###############################################################################
#Assembly
###############################################################################
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-2-1', 
    part=mdb.models['Model-1'].parts['Part-2'])
    

    
###################################################################################
##CREATE PERIODIC BOUNDARY CONDITIONS
###################################################################################
mdb.models['Model-1'].rootAssembly.Set(nodes=(
    mdb.models['Model-1'].rootAssembly.instances['Part-2-1'].nodes,), name='PerBound')

(CoorFixNode,NameRef1, NameRef2,NameRef3)=PeriodicBound3D(mdb,'Model-1',
    'PerBound',[(UC_boundary[1,0],0.0,0.0),(0.0,UC_boundary[1,1],0.0),(0.0,0.0,UC_boundary[1,2])],)
    
##################################################################################
#CREATE STEP AND APPLY BC
##################################################################################
mdb.models['Model-1'].StaticStep(name='Step-1', nlgeom=ON, previous='Initial')
#Apply boundary conditions on reference nodes
DefMat=[(dU1,0.0,0.0),(0.0,0.0,0.0), (0.0,0.0,0.0)]
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-REF-1', region=Region(referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances[NameRef1].referencePoints[1], 
    )), u1=DefMat[0][0], u2=DefMat[0][1], u3=DefMat[0][2], ur1=UNSET,ur2=UNSET,ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-REF-2', region=Region(referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances[NameRef2].referencePoints[1], 
    )), u1=DefMat[1][0], u2=DefMat[1][1], u3=DefMat[1][2], ur1=UNSET,ur2=UNSET,ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-REF-3', region=Region(referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances[NameRef3].referencePoints[1], 
    )), u1=DefMat[2][0], u2=DefMat[2][1], u3=DefMat[2][2], ur1=UNSET,ur2=UNSET,ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-FIXNODE', region=Region(
    nodes=mdb.models['Model-1'].rootAssembly.instances['Part-2-1'].nodes.getByBoundingSphere(center=CoorFixNode, radius=0.001)), u1=0.0, u2=0.0, u3=0.0, ur1=UNSET, ur2=UNSET,ur3=UNSET)

##################################################################################
#JOB AND RUN
##################################################################################
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)