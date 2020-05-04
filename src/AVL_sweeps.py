## AVL_sweeps

# AVL_sweeps.py
# Author  : Stanislav Karpuk
#           (stankarpuk93@gmail.com)
# Created : 05/01/2020
# Modified:


import os
import glob
import numpy as np
import xlsxwriter

from Data_structure   import Data
from write_run_cases  import write_run_cases
from write_run_script import write_run_script
from run_AVL          import call_avl
from read_results     import read_results

'''
Description:
    The code generates files required for AVL-sweeps.
    The type of sweeps is defined by the user but are limited
    to alpha, betta, and Mach number sweeps.
    Deflections of flaps, ailerons, elevators, and rudders can
    be deifined too.

    IMPORTANT NOTE:
        AVL manages to run only 25 cases. For for more cases, AVL
        is run multiple times automatically
References:
'''

#-------------------------------------------------------------------------------------------------------
# Input
#-------------------------------------------------------------------------------------------------------

# Sweep parameters
alpha    = [0, 2, 4, 6, 8, 10, 12]                           # Angle-of-attack (deg)
beta     = [0, 2, 4, 6, 8]                           # Side-slip angle (deg)
Mach     = [0.41]                           # Mach number

flaps    = 30.0                           # Flap deflection (deg)
ailerons = 0.0                           # Aileron deflection (deg)
elevator = 0.0                           # Elevator deflection (deg)
rudder   = 0.0                           # Rudder deflection (deg)
# Note: if no control surface deflections are specified, then type "None"

# Define geometric properties
CG = [48.1627, 0.0000, -0.0000]          # CG definition
control_surfaces = 3                     # Number of control surfaces defined in the geometry file

# Define filenames
geo_filename   = 'exampe_aircraft.avl'                         # Geometry filename 
batch_header   = 'exampe_aircraft'                             # Batch file header
run_header     = 'exampe_aircraft'                             # Run file header
log_filename   = 'exampe_aircraft.log'                         # Log filename
err_filename   = 'exampe_aircraft.err'                         # Error filename

# Call AVL name
avl_call = 'avl.exe'


#-------------------------------------------------------------------------------------------------------
# Create an input data structure
#-------------------------------------------------------------------------------------------------------
Input = Data()
Input.run_file     = run_header
Input.batch_file   = batch_header
Input.geo_file     = geo_filename
Input.log_file     = log_filename
Input.err_file     = err_filename
Input.avl_call     = avl_call
Input.AoA          = alpha
Input.AoS          = beta
Input.Mach         = Mach
Input.CG           = CG
Input.ctrl_surf    = control_surfaces

Input.controls = Data()

if flaps != 0:
    Input.controls.flaps = Data()
    Input.controls.flaps.tag        = 'flaps'
    Input.controls.flaps.deflection = flaps

if ailerons != 0:
    Input.controls.ailerons = Data()
    Input.controls.ailerons.tag        = 'ailerons'
    Input.controls.ailerons.deflection = ailerons

if elevator != 0:
    Input.controls.elevator = Data()
    Input.controls.elevator.tag        = 'elevator'
    Input.controls.elevator.deflection = elevator
    
if rudder != 0:
    Input.controls.rudder = Data()
    Input.controls.rudder.tag          = 'rudder'
    Input.controls.rudder.deflection   = rudder

#-------------------------------------------------------------------------------------------------------
# Initialize the code
#-------------------------------------------------------------------------------------------------------
print('Calculation of AVL sweeps\n' + 
      'Number of cases: ' + str(len(alpha)*len(beta)*len(Mach)) + '\n')


#-------------------------------------------------------------------------------------------------------
# Creare run cases
#-------------------------------------------------------------------------------------------------------
print('Writing run cases...\n')
write_run_cases(Input)

#-------------------------------------------------------------------------------------------------------
# Creare run files
#-------------------------------------------------------------------------------------------------------
print('Writing the run script...\n')
write_run_script(Input)

# Remove output files if they exist
for name in glob.glob('case*'):
    os.remove(name)

#-------------------------------------------------------------------------------------------------------
# Run AVL
#-------------------------------------------------------------------------------------------------------
print('Running AVL...\n')
for i in range(Input.batch_index):
    Input.run_full_name = Input.run_file + str(i) + '.run'
    print(Input.run_full_name)
    call_avl(Input)

#-------------------------------------------------------------------------------------------------------
# Post-process results
#-------------------------------------------------------------------------------------------------------
# Read ouput results
print('Reading outputs...\n')
labels,results = read_results(Input)

# Write output into the file
print('Writing outputs to Excel...\n')
workbook  = xlsxwriter.Workbook('AVL_derivatives.xlsx')
worksheet = workbook.add_worksheet()
row = 0
worksheet.write_column(row, 0, labels)
for col, result in enumerate(results):
    worksheet.write_column(row, col+1, result)

workbook.close()

print('Calculations are completed\n')
