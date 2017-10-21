#Created by J.T.B. Overvelde
#2015/07/07
#http://www.overvelde.com
#CREATED IN ABAQUS VERSION 6.11-1.

#FUNCTION TO APPLY PERIODIC BOUNDARY CONDITIONS IN 2D
#mdb: model database
#NameModel: 	A string with the name of your model
#NameSet: 	A string with the name of your set (for a faster script, this set 
#		should only contain those nodes that will have periodic boundary conditions applied to them)
#LatticeVec:	An array with the lattice vectors, for example [(1.0, 0.0), (1.0, 1.0)] for a square lattice
def PeriodicBound2D(mdb,NameModel,NameSet,LatticeVec):
    from part import TWO_D_PLANAR, DEFORMABLE_BODY
    #Create reference parts and assemble
    NameRef1='RefPoint-0'; NameRef2='RefPoint-1'
    mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef1, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].Part(dimensionality=TWO_D_PLANAR, name=NameRef2, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef2].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
        part=mdb.models[NameModel].parts[NameRef1])
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef2, 
        part=mdb.models[NameModel].parts[NameRef2])

    #Create set of reference points
    mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))
    mdb.models[NameModel].rootAssembly.Set(name=NameRef2, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef2].referencePoints[1],))

    #Get all nodes
    nodesAll=mdb.models[NameModel].rootAssembly.sets[NameSet].nodes
    nodesAllCoor=[]
    for nod in mdb.models[NameModel].rootAssembly.sets[NameSet].nodes:
        nodesAllCoor.append(nod.coordinates)
    repConst=0
    #Find periodically located nodes and apply equation constraints
    ranNodes=range(0,len(nodesAll))	#Index array of nodes not used in equations constraint
    for repnod1 in range(0,len(nodesAll)):
        stop=False			#Stop will become true when equation constraint is made between nodes
        Coor1=nodesAllCoor[repnod1]		#Coordinates of Node 1
        for repnod2 in ranNodes:	#Loop over all available nodes
            Coor2=nodesAllCoor[repnod2]	#Coordinates of Node 2
            dx=Coor2[0]-Coor1[0]; dy=Coor2[1]-Coor1[1]	#X and Y Distance between nodes
            for comb in range(0,len(LatticeVec)):	#Check if nodes are located exactly the vector lattice apart
                if int(round(1000.0*(LatticeVec[comb][0]-dx)))==0:
                    if int(round(1000.0*(LatticeVec[comb][1]-dy)))==0:
                        #Correct combination found
                        #Create sets for use in equations constraints
                        mdb.models[NameModel].rootAssembly.Set(name='Node-1-'+str(repConst), nodes=
                            mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod1:repnod1+1])
                        mdb.models[NameModel].rootAssembly.Set(name='Node-2-'+str(repConst), nodes=
                            mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod2:repnod2+1])
                        #Create equations constraints for each dof
                        for Dim1 in [1,2]:
                            mdb.models[NameModel].Equation(name='PerConst'+str(Dim1)+'-'+str(repConst),
	                        terms=((1.0,'Node-1-'+str(repConst), Dim1),(-1.0, 'Node-2-'+str(repConst), Dim1) ,
                                (1.0, 'RefPoint-'+str(comb), Dim1)))
                        repConst=repConst+1	#Increase integer for naming equation constraint
                        ranNodes.remove(repnod1)#Remove used node from available list
                        stop=True		#Don't look further, go to following node.
                        break
            if stop:
                break
    #Return coordinates of free node so that it can be fixed
    return (nodesAll[ranNodes[0]].coordinates, NameRef1, NameRef2)

#FUNCTION TO APPLY PERIODIC BOUNDARY CONDITIONS IN 2D
#mdb: model database
#NameModel: 	A string with the name of your model
#NameSet: 	A string with the name of your set (for a faster script, this set 
#		should only contain those nodes that will have periodic boundary conditions applied to them)
#LatticeVec:	An array with the lattice vectors, for example [(1.0,0.0,0.0),(0.0,1.0,0.0),(0.0,0.0,1.0)] for a cubic lattice
def PeriodicBound3D(mdb,NameModel,NameSet,LatticeVec):
    import time
    start1 = time.time()

    from part import THREE_D, DEFORMABLE_BODY
    #Create reference parts and assemble
    NameRef1='RefPoint-0'; NameRef2='RefPoint-1'; NameRef3='RefPoint-2'
    mdb.models[NameModel].Part(dimensionality=THREE_D, name=NameRef1, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].Part(dimensionality=THREE_D, name=NameRef2, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef2].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].Part(dimensionality=THREE_D, name=NameRef3, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef3].ReferencePoint(point=(0.0, 0.0, 0.0))
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
        part=mdb.models[NameModel].parts[NameRef1])
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef2, 
        part=mdb.models[NameModel].parts[NameRef2])
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef3, 
        part=mdb.models[NameModel].parts[NameRef3])

    #Create set of reference points
    mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))
    mdb.models[NameModel].rootAssembly.Set(name=NameRef2, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef2].referencePoints[1],))
    mdb.models[NameModel].rootAssembly.Set(name=NameRef3, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef3].referencePoints[1],))
    end1 = time.time()
    print end1 - start1
    start2 = time.time()
    #Get all nodes
    nodesAll=mdb.models[NameModel].rootAssembly.sets[NameSet].nodes
    nodesAllCoor=[]
    for nod in mdb.models[NameModel].rootAssembly.sets[NameSet].nodes:
        nodesAllCoor.append(nod.coordinates)
    end2 = time.time()
    print end2 - start2
    start3 = time.time()
    repConst=0
    #Find periodically located nodes and apply equation constraints
    ranNodes=range(0,len(nodesAll))	#Index array of nodes not used in equations constraint
    print len(nodesAll)
    for repnod1 in range(0,len(nodesAll)):
        stop=False			#Stop will become true when equation constraint is made between nodes
        Coor1=nodesAllCoor[repnod1]		#Coordinates of Node 1
        for repnod2 in ranNodes:	#Loop over all available nodes
            Coor2=nodesAllCoor[repnod2]	#Coordinates of Node 2
            for comb in range(0,len(LatticeVec)):	#Check if nodes are located exactly the vector lattice apart
                if int(1000.0*(LatticeVec[comb][0]-Coor2[0]+Coor1[0]))==0 and int(1000.0*(LatticeVec[comb][1]-Coor2[1]+Coor1[1]))==0 and int(1000.0*(LatticeVec[comb][2]-Coor2[2]+Coor1[2]))==0:
                    #Correct combination found
                    #Create sets for use in equations constraints
                    mdb.models[NameModel].rootAssembly.Set(name='Node-1-'+str(repConst), nodes=
                       mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod1:repnod1+1])
                    mdb.models[NameModel].rootAssembly.Set(name='Node-2-'+str(repConst), nodes=
                       mdb.models[NameModel].rootAssembly.sets[NameSet].nodes[repnod2:repnod2+1])
                    #Create equations constraints for each dof
                    for Dim1 in [1,2,3]:
                       mdb.models[NameModel].Equation(name='PerConst'+str(Dim1)+'-'+str(repConst),
	                      terms=((1.0,'Node-1-'+str(repConst), Dim1),(-1.0, 'Node-2-'+str(repConst), Dim1) ,
                            (1.0, 'RefPoint-'+str(comb), Dim1)))
                    repConst=repConst+1	#Increase integer for naming equation constraint
                    ranNodes.remove(repnod1)#Remove used node from available list
                    stop=True		#Don't look further, go to following node.
                    break
            if stop:
                break
    end3 = time.time()
    print end3 - start3
    #Return coordinates of free node so that it can be fixed
    return (nodesAll[ranNodes[0]].coordinates, NameRef1, NameRef2,NameRef3)
