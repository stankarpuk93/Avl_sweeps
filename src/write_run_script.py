## @ingroup Methods-Aerodynamics-AVL
# write_runcases.py
# 
# Created:  Dec 2014, T. Momose
# Modified: Jan 2016, E. Botero
#           Apr 2017, M. Clarke
#           May 2020, S. Karpuk

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import os
import math as m
import numpy as np

def write_run_script(Input):
    """ This function writes the AVL-run script

    Assumptions:
        None
        
    Source:
        Drela, M. and Youngren, H., AVL, http://web.mit.edu/drela/Public/web/avl

    """    

    # unpack inputs
    batch_index    = Input.batch_index
    index          = Input.index_total    
    run_filename   = Input.run_file
    batch_filename = Input.batch_file
    geo_filename   = Input.geo_file

    # calculate number of cases for each batch
    N_full_cases   = 25
    N_full_batches = m.floor(index/N_full_cases)
    N_rem_cases    = index - N_full_batches * N_full_cases
    Num_tot_batches = N_full_batches + 1
    cases_cont      = np.zeros(Num_tot_batches)
    for i in range(N_full_batches):
        cases_cont[i] = N_full_cases
    cases_cont[len(cases_cont)-1] = N_rem_cases
    
    for j in range(batch_index):
        print(j)
        full_name = run_filename + str(j) + '.run'
        if os.path.exists(full_name):
            os.remove(full_name )
            
        with open(full_name ,'w') as input_deck:
            input_deck.write('load ' + geo_filename + '\n')
            input_deck.write('case ' + batch_filename + str(j+1) + '.batch' + '\n')
            input_deck.write('oper\n')
            
            index = cases_cont[j]
            for i in range(int(cases_cont[j])):
                input_deck.write(str(i+1) + '\n')
                input_deck.write('x\n')
                input_deck.write('st\n')
                input_deck.write('case_' + str(int(cases_cont[j-1])*j+i+1).zfill(2) + 'output.dat\n')
           
            input_deck.write('\n\nQUIT\n')

        input_deck.close()
    return
