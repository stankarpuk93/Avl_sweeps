## run_AVL
#run_AVL.py
# 
# Created:  Oct 2014, T. Momose
# Modified: Jan 2016, E. Botero
#           Jul 2017, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import sys
import time
import subprocess
import os
from SUAVE.Core import redirect

## @ingroup Methods-Aerodynamics-AVL
def run_analysis(avl_object):
    """ This calls the AVL executable and runs an analysis

    Assumptions:
        None
        
    Source:
        None

    Inputs:
        avl_object - passed into the  call_avl function  
        
    Outputs:
        results

    Properties Used:
        N/A
    """    
    call_avl(avl_object)
    results = read_results(avl_object)

    return results


def call_avl(Input):
    """ This function calls the AVL executable and executes analyses

    Assumptions:
        None
        
    Source:
        None
        

    Properties Used:
        N/A
    """    

    log_file = Input.log_file
    err_file = Input.err_file
    '''if isinstance(log_file,str):
        os.remove(log_file)
    if isinstance(err_file,str):
        os.remove(err_file)'''
    avl_call = Input.avl_call
    geometry = Input.geo_file 
    in_deck  = Input.run_full_name 

    ctime = time.ctime() # Current date and time stamp
    with open(in_deck,'r') as commands:
        print_output = True
        
        # Initialize suppression of console window output
        if print_output == False:
            devnull = open(os.devnull,'w')
            sys.stdout = devnull       
    
        # Run AVL
        avl_run = subprocess.Popen([avl_call,geometry],stdout=sys.stdout,stderr=sys.stderr,stdin=subprocess.PIPE)
        for line in commands:
            avl_run.stdin.write(line.encode('utf-8'))
            avl_run.stdin.flush()
          
        # Terminate suppression of console window output  
        if print_output == False:
            sys.stdout = sys.__stdout__                    
            
    avl_run.wait()

    exit_status = avl_run.returncode
    ctime = time.ctime()

    return exit_status

