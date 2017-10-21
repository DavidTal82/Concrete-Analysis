# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:02:35 2016

@author: operator
"""

import os

dir_Path = 'C:/Users/operator/Documents/MATLAB/MATLAB_Research/Concrete_Analysis'

command_1 = 'cd C:\Users\operator\Documents\Gmesh'
command_2a = 'gmsh '


good = []
bad = []

for i in range(3001,4719):
    
    name = '%04d' %i + 'UC.geo' 
    
    model = '/' + name
    
    command_2b = dir_Path + '/MonteCarlo/Models/Temp/geo' + model + ' -3' 
    
    command = command_1 + ' && ' + command_2a +command_2b
    
    try:
        out = os.system(command)
        if not(out):
            good.append(i)
            print(str(i) + ': good')
        else:
            bad.append(i)
            print(str(i) + ': bad')
    except:
        print('except')
        