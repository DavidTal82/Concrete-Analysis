# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:02:24 2016

@author: operator
"""

import os

def copy_file(file_in,file_out):
    
    f_in = open(file_in, 'r')
    f_out = open(file_out, 'w')
    
    for line in f_in:
        f_out.write(line)
    
    f_in.close()
    f_out.close()


dir_path = 'C:/Users/operator/Documents/MATLAB/MATLAB_Research/Concrete_Analysis/MonteCarlo'
dir_old = dir_path + '/Models/Temp'
dir_new = dir_path + '/Models'

dir_AggDef = dir_old + '/AggDef'
dir_geo = dir_old + '/geo'
dir_msh = dir_old + '/msh'

files_list = os.listdir(dir_msh)




original_msh = []


for fileName in files_list:    
    if fileName[-3:] == 'msh':
        original_msh.append(int(fileName[:4]))
        

file_count = 793 

for i in original_msh:
    file_count +=1
    nameOld = '%04d' %i
    nameNew = '%04d' %file_count
    f_Agg_in = dir_AggDef + '/' + nameOld + 'Agg.txt'
    f_Def_in = dir_AggDef + '/' + nameOld + 'Def.txt'
    f_geo_in = dir_geo + '/' + nameOld + 'UC.geo'
    f_msh_in = dir_msh + '/' + nameOld + 'UC.msh'
    f_Agg_out = dir_new + '/AggDef/' + nameNew + 'Agg.txt'
    f_Def_out = dir_new + '/AggDef/' + nameNew + 'Def.txt'
    f_geo_out = dir_new + '/geo/' + nameNew + 'UC.geo'
    f_msh_out = dir_new + '/msh/' + nameNew + 'UC.msh'
    copy_file(f_Agg_in,f_Agg_out)
    copy_file(f_Def_in,f_Def_out)
    copy_file(f_geo_in,f_geo_out)
    copy_file(f_msh_in,f_msh_out)



