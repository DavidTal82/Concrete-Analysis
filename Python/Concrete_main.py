# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 19:11:10 2016

@author: operator
"""

import os
import time
import numpy as np
import matplotlib.pyplot as plt

runfile('C:/ABAQUS/Scripting/Concrete_Analysis.py', wdir='C:/ABAQUS/Scripting')


main_dir = 'C:/Users/operator/Documents/MATLAB/MATLAB_Research/Concrete_Analysis/MonteCarlo/Models'
inp_folder = main_dir + '/inp'
run_folder = main_dir + '/AbaqusRun'
results_folder = main_dir + '/AbaqusResults'

model_folder = os.listdir(inp_folder)

model_list = model_folder[521:]

for m in model_list:
    
    t = time.time()
   
    modelName = m[:-4]
    
    #copying the file to the running folder
    file_in = inp_folder + '/' + modelName + '.inp'
    file_out = run_folder + '/' + modelName + '.inp'
    copy_file(file_in,file_out)
    
    #running the simulation - add number of cpus
    run_inp(run_folder,modelName,5)
    
    #getting results from the odb file and saving to a text file
    get_results_CUBE(run_folder,modelName,results_folder,1)
    
    #cleaning the folder
    clean_folder(run_folder)
    
    dt = time.time() - t
    
    print('model: ' + modelName + ' | Time: ' + str(int(dt)))



