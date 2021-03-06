##############################################################################
### Tool to convert vorocrust PFLOTRAN HDF5 output to Exodus II mesh
### Author: Rosie Leone 5/6/2021
### Usage: python pflotran2exodus.py input_mesh.exo pflotran_output.h5 out.exo
#############################################################################
#
#This script takes the exodus II mesh file, input_mesh.exo, generated by
# VoroCrust software and HDF5 output from a PFLOTRAN simulation,
# pflotran_output.h5, and combines them into a single exodus II file, out.exo,
# that can be used for visualization in Paraview.

#NOTE: The exodus python wrapper is required to run this script.  If exodus is
# installed via seacas then the wrapper will automatically be installed. 

#Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC
#(NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
#Government retains certain rights in this software.

#This is free software; you can redistribute it and/or modify it under the
#terms of the GNU Lesser General Public License as published by the Free
#Software Foundation. See file LICENSE for details of the the open source 
#GNU LGPL 3.0 license.


import exodus
from numpy import *
import h5py
import time as t
import sys
from shutil import copyfile
import sys

def pflotran_to_exodus_vorocrust_mesh():
    start_time = t.time()
    input_mesh = sys.argv[1]
    pflotran_output = sys.argv[2]
    outfilename = sys.argv[3]
    print('**************************************************************************',\
          'Copyright 2021 National Technology & Engineering Solutions of Sandia, LLC',\
          '(NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.',\
          'Government retains certain rights in this software.',\
          'This is free software; you can redistribute it and/or modify it under the',\
          'terms of the GNU Lesser General Public License as published by the Free',\
          'Software Foundation. See file LICENSE for details of the the open source ',\
          'GNU LGPL 3.0 license.',\
          '**************************************************************************',sep='\n')
    
    if len(sys.argv) != 4:
        print ("ERROR: Command line arguments not provided")
        sys.exit(0)

    print("Reading: {}".format(pflotran_output))
    f = h5py.File(pflotran_output,'r')

    #Get list of datasets, store variable names, and save it as a dictionary
    datasets =[]
    pflotran_dict= {}
    variable_names = []
    f.visit(lambda key : datasets.append(key) if type(f[key]) is h5py._hl.dataset.Dataset else None)

    #Assumes pflotran output only has Time groups in it
    for dataset in datasets:
        dataset_split = dataset.strip().split('/')
        name = dataset_split[1]
        h5group = dataset_split[0].strip().split()
        time = h5group[2]
        if time in pflotran_dict.keys():
            pflotran_dict[time].append(dataset)
            if name not in variable_names:
                variable_names.append(name)
        else:
            pflotran_dict[time] = [dataset]
            if name not in variable_names:
                variable_names.append(name)
    
    variable_num = len(variable_names)

    #Copying input file, will change this to something more sophisticated

    copyfile(input_mesh,outfilename)
    exoid = exodus.exodus(outfilename,"a")
    #errors if can't open
    
    status = exoid.set_variable_number("EX_ELEM_BLOCK",variable_num)

    #time counter
    counter = 1

    #Get element ID to write to
    blk_ids = exoid.get_elem_blk_ids()

    first = True
    for times, variables in pflotran_dict.items():
        time = float(times)
        status = exoid.put_time(counter,time)
        for i in range(len(variables)):
            var_values = array(f[variables[i]])
            if first:
                status = exoid.put_element_variable_name(variable_names[i], i+1)
            status = exoid.put_element_variable_values(blk_ids[0],variable_names[i],counter,var_values)
        first = False
        counter = counter + 1   
    exoid.close()

    end_time = t.time()
    elapsed_time = end_time - start_time
    print ("Time for mesh conversion = {} s".format(elapsed_time))

if __name__ == "__main__":
    pflotran_to_exodus_vorocrust_mesh()
