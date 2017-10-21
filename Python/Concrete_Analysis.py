import os
import numpy as np
import matplotlib.pyplot as plt

################################################

def copy_file(file_in,file_out):    
    f_in = open(file_in, 'r')
    f_out = open(file_out, 'w')
    for line in f_in:
        f_out.write(line)    
    f_in.close()
    f_out.close()

################################################

def write_path(odbPath,jobName,resultsName):
    f = open('path.txt','w')
    f.write(odbPath)
    f.write('\n')
    f.write(jobName)
    f.write('\n')
    f.write(resultsName)
    f.write('\n')
    f.close()
    
################################################    
    
def run_inp(inpPath,modelName,cpus=1):
    command1 = 'cd ' +  inpPath + ' && abaqus job='
    command2 = ' int'
    if cpus!=1:
        command2 = ' cpus=' + str(cpus) + command2
    command = command1 + modelName + command2
    #print(command)
    os.system(command)

################################################

def get_results_CUBE(odbPath,jobName,resultsPath,case):
    if case==3:
        resultsName = resultsPath + '/' + jobName + '_Stress.txt'
    else:
        resultsName = resultsPath + '/' + jobName + '.txt'
    #if not(os.path.exists(resultsPath + '.txt')):
    write_path(odbPath,jobName,resultsName)
    
    if case==1:
        os.system('abaqus cae noGUI=C:\ABAQUS\Scripting\get_Results_ConcreteCube.py')
    if case==2:
        os.system('abaqus cae noGUI=C:\ABAQUS\Scripting\get_Results_ConcreteCube_Periodic.py')
    if case==3:
        os.system('abaqus cae noGUI=C:\ABAQUS\Scripting\get_Results_ConcreteCube_Periodic_Stress.py')
#    Frame, E11, E22, E33, S11, S22, S33, U1, U2, U3, F1, F2, F3
#    results_temp = np.loadtxt(resultsName, delimiter=',',)
#    E11S11[jobName] = results_temp[:,[1,4]]
#    return (E11S11)

################################################

def get_results_CYLINDER(jobList,odbPath):    
    E22S22 = {}
    for jobName in jobList:        
        resultsPath = odbPath + '/' + jobName        
        if not(os.path.exists(resultsPath + '.txt')):
            write_path(odbPath,jobName)            
            os.system('abaqus cae noGUI=C:\ABAQUS\Scripting\get_Results_ConcreteCylinder.py')                
        # Frame,   E22, S22, U2, F2
        results_temp = np.loadtxt(resultsPath + '.txt', delimiter=',',)
        E22S22[jobName] = results_temp[:,[1,2]]
    return (E22S22)

################################################

def read_results(resultsName):    
    results = np.loadtxt(resultsName, delimiter=',',)
    # Frame, E11, E22, E33, S11, S22, S33, U1, U2, U3, F1, F2, F3
    return (results)
    
###############################################

def clean_folder(folder_path):
    files_list = os.listdir(folder_path)
    for f in files_list:
        file2delete = folder_path + '/' + f
        os.remove(file2delete)
        





###############################################
################################################
################################################

##jobList = ['Job-C-1','Job-D-1','Job-E-1']
##scriptPath = 'C:\ABAQUS\Scripting'
#
#odbPath = 'C:/ABAQUS/WorkingDirectory'
#jobList = ['Job-Gurson-Calibrated']
#
## 1-Sym BC
## 2-Periodic BC
## 3-Periodic BC - Stress
#E11S11 = get_results_CUBE(jobList,odbPath,1)
#A = -E11S11[jobList[0]]
#
#plt.plot(-E11S11[jobList[0]][:,0],-E11S11[jobList[0]][:,1], 'b-')
#plt.xlabel('Strain [mm/mm]')
#plt.ylabel('Stress [GPa (?)]')
#plt.show()







