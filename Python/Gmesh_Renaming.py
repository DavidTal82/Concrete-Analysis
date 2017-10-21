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


dir_path = 'C:\Users\operator\Documents\MATLAB\MATLAB_Research\Concrete_Analysis\MonteCarlo'
dir_New = dir_path + '\Models\Temp'

dir_AggDef = dir_New + '\AggDef'
dir_geo = dir_New + '\geo'

files_list = os.listdir(dir_path)

Agg = []
Def = []

for fileName in files_list:    
    if fileName[-7:] == 'Agg.txt':
        Agg.append(int(fileName[:4]))
    if fileName[-7:] == 'Def.txt':
        Def.append(int(fileName[:4]))
        
file_count = 262 

for i in Agg:
    file_count +=1
    nameOld = '%04d' %i
    nameNew = '%04d' %file_count
    f_Agg_in = dir_path + '\\' + nameOld + 'Agg.txt'
    f_Def_in = dir_path + '\\' + nameOld + 'Def.txt'
    f_Agg_out = dir_AggDef + '\\' + nameNew + 'Agg.txt'
    f_Def_out = dir_AggDef + '\\' + nameNew + 'Def.txt'

    copy_file(f_Agg_in,f_Agg_out)
    copy_file(f_Def_in,f_Def_out)


for i in original_msh_1:
    file_count +=1
    nameOld = '%04d' %i
    nameNew = '%04d' %file_count
    f_Agg_in = dir_AggDef_1 + '\\' + nameOld + 'Agg.txt'
    f_Def_in = dir_AggDef_1 + '\\' + nameOld + 'Def.txt'
    f_geo_in = dir_Models_1 + '\\' + nameOld + 'UC.geo'
    f_msh_in = dir_Models_1 + '\\' + nameOld + 'UC.msh'
    f_Agg_out = dir_New + '\\AggDef\\' + nameNew + 'Agg.txt'
    f_Def_out = dir_New + '\\AggDef\\' + nameNew + 'Def.txt'
    f_geo_out = dir_New + '\\geo\\' + nameNew + 'UC.geo'
    f_msh_out = dir_New + '\\msh\\' + nameNew + 'UC.msh'
    copy_file(f_Agg_in,f_Agg_out)
    copy_file(f_Def_in,f_Def_out)
    copy_file(f_geo_in,f_geo_out)
    copy_file(f_msh_in,f_msh_out)
    
for i in original_msh_2:
    file_count +=1
    nameOld = '%04d' %i
    nameNew = '%04d' %file_count
    f_Agg_in = dir_AggDef_2 + '\\' + nameOld + 'Agg.txt'
    f_Def_in = dir_AggDef_2 + '\\' + nameOld + 'Def.txt'
    f_geo_in = dir_Models_2 + '\\' + nameOld + 'UC.geo'
    f_msh_in = dir_Models_2 + '\\' + nameOld + 'UC.msh'
    f_Agg_out = dir_New + '\\AggDef\\' + nameNew + 'Agg.txt'
    f_Def_out = dir_New + '\\AggDef\\' + nameNew + 'Def.txt'
    f_geo_out = dir_New + '\\geo\\' + nameNew + 'UC.geo'
    f_msh_out = dir_New + '\\msh\\' + nameNew + 'UC.msh'
    copy_file(f_Agg_in,f_Agg_out)
    copy_file(f_Def_in,f_Def_out)
    copy_file(f_geo_in,f_geo_out)
    copy_file(f_msh_in,f_msh_out)



