#read_results.py
# 
# Created:  Mar 2015, T. Momose
# Modified: Jan 2016, E. Botero
#           Dec 2017, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import glob
import numpy as np
from SUAVE.Core import Data


## @ingroup Methods-Aerodynamics-AVL
def read_results(Input):
    """ This functions reads the results from the results text file created 
    at the end of an AVL function call

    Assumptions:
        None
        
    Source:
        Drela, M. and Youngren, H., AVL, http://web.mit.edu/drela/Public/web/avl 

    """

    # unpack inputs
    case_num = Input.index_total
    num_ctrl = Input.ctrl_surf

    # gather ouput filenames
    output_filenames = []
    for name in sorted(glob.glob('case*')):
        output_filenames.append(name)

    Stab_der1 = np.zeros((case_num,13))
    Stab_der2 = np.zeros((case_num,10))
    Stab_der3 = np.zeros((case_num,15))
    print(case_num)
    for i in range(case_num):
       
        '''
        Output matrx formats:
        
        Aerodynamic coefficients:
        | Mach | AoA | AoS | CX | CY | CZ | CL | CD | CDi | Cl | Cm | Cn | e |
        ----------------------------------------------------------------------
        |      |     |     |    |    |    |    |    |     |    |    |    |   |
        |      |     |     |    |    |    |    |    |     |    |    |    |   |


        Stability derivatives (wrt AoA and AoS):
        CLa | CYa | Cla | Cma | Cna | CLb | CYb | Clb | Cmb | Cnb |
        -----------------------------------------------------------
        |     |     |     |     |     |     |     |     |     |   |
        |     |     |     |     |     |     |     |     |     |   |


        Stability derivatives (wrt p,q,r):
        CLp | CLq | CLr | CYp | CYq | CYr | Clp | Clq | Clr | Cmp | Cmq | Cmr | Cnp | Cnq | Cnr |
        --------------------------------------------------------------------------------------------------------------
            |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
            |     |     |     |     |     |     |     |     |     |     |     |     |     |     |         
        '''

        # define output coefficients array
        labels = ['Mach','AoA','AoS','CX','CY','CZ','CL','CD','CDi','Cl','Cm','Cn','e',
                  'CLa','CYa','Cla','Cma','Cna','CLb','CYb','Clb','Cmb','Cnb',
                  'CLp','CLq','CLr','CYp','CYq','CYr','Clp','Clq','Clr','Cmp','Cmq','Cmr','Cnp','Cnq','Cnr']

        with open(output_filenames[i],'r') as res_file:
 
            lines   = res_file.readlines()

            # write aerodynamic coefficients
            Stab_der1[i,0]  = float(lines[17][11:19].strip()) # Mach
            Stab_der1[i,1]  = float(lines[15][11:19].strip()) # AoA
            Stab_der1[i,2]  = float(lines[16][11:19].strip()) # AoS
            Stab_der1[i,3]  = float(lines[19][11:19].strip()) # CX
            Stab_der1[i,4]  = float(lines[20][11:19].strip()) # CY
            Stab_der1[i,5]  = float(lines[21][11:19].strip()) # CZ
            Stab_der1[i,6]  = float(lines[23][10:20].strip()) # CL
            Stab_der1[i,7]  = float(lines[24][10:20].strip()) # CD
            Stab_der1[i,8]  = float(lines[25][32:42].strip()) # CDi
            Stab_der1[i,9]  = float(lines[19][33:41].strip()) # Cl
            Stab_der1[i,10] = float(lines[20][33:41].strip()) # Cm
            Stab_der1[i,11] = float(lines[21][33:41].strip()) # Cn
            Stab_der1[i,12] = float(lines[27][32:42].strip()) # e

            # write stability coefficients
            Stab_der2[i,0]  = float(lines[36+num_ctrl][24:34].strip()) # CLa
            Stab_der2[i,1]  = float(lines[37+num_ctrl][24:34].strip()) # CYa
            Stab_der2[i,2]  = float(lines[38+num_ctrl][24:34].strip()) # Cla
            Stab_der2[i,3]  = float(lines[39+num_ctrl][24:34].strip()) # Cma
            Stab_der2[i,4]  = float(lines[40+num_ctrl][24:34].strip()) # Cna
            Stab_der2[i,5]  = float(lines[36+num_ctrl][43:54].strip()) # CLb
            Stab_der2[i,6]  = float(lines[37+num_ctrl][43:54].strip()) # CYb
            Stab_der2[i,7]  = float(lines[38+num_ctrl][43:54].strip()) # Clb
            Stab_der2[i,8]  = float(lines[39+num_ctrl][43:54].strip()) # Cmb
            Stab_der2[i,9]  = float(lines[40+num_ctrl][43:54].strip()) # Cnb

            Stab_der3[i,0]  = float(lines[44+num_ctrl][24:34].strip()) # CLp
            Stab_der3[i,1]  = float(lines[44+num_ctrl][43:54].strip()) # CLq
            Stab_der3[i,2]  = float(lines[44+num_ctrl][65:74].strip()) # CLr
            Stab_der3[i,3]  = float(lines[45+num_ctrl][24:34].strip()) # CYp
            Stab_der3[i,4]  = float(lines[45+num_ctrl][43:54].strip()) # CYq
            Stab_der3[i,5]  = float(lines[45+num_ctrl][65:74].strip()) # CYr
            Stab_der3[i,6]  = float(lines[46+num_ctrl][24:34].strip()) # Clp
            Stab_der3[i,7]  = float(lines[46+num_ctrl][43:54].strip()) # Clq
            Stab_der3[i,8]  = float(lines[44+num_ctrl][65:74].strip()) # Clr
            Stab_der3[i,9] = float(lines[47+num_ctrl][24:34].strip()) # Cmp
            Stab_der3[i,10] = float(lines[47+num_ctrl][43:54].strip()) # Cmq
            Stab_der3[i,11] = float(lines[44+num_ctrl][65:74].strip()) # Cmr
            Stab_der3[i,12] = float(lines[48+num_ctrl][24:34].strip()) # Cnp
            Stab_der3[i,13] = float(lines[48+num_ctrl][43:54].strip()) # Cnq
            Stab_der3[i,14] = float(lines[48+num_ctrl][65:74].strip()) # Cnr
            
    # stack results
    results = np.concatenate((Stab_der1, Stab_der2, Stab_der3), axis=1)        
 
    return labels,results
