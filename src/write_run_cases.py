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

def write_run_cases(Input):
    """ This function writes the run cases used in the AVL batch analysis

    Assumptions:
        None
        
    Source:
        Drela, M. and Youngren, H., AVL, http://web.mit.edu/drela/Public/web/avl

    """    
    
    base_case_text = \
'''

 ---------------------------------------------
 Run case  {0}:   {1}

 alpha        ->  alpha       =   {2}    
 beta         ->  beta        =   {3}    
 pb/2V        ->  pb/2V       =   0.00000    
 qc/2V        ->  qc/2V       =   0.00000    
 rb/2V        ->  rb/2V       =   0.00000    
 {4}   

 alpha     =   0.00000     deg                             
 beta      =   0.00000     deg                             
 pb/2V     =   0.00000                                     
 qc/2V     =   0.00000                                     
 rb/2V     =   0.00000                                     
 CL        =   0.00000                                    
 CDo       =   0.00000                                     
 bank      =   0.00000     deg                             
 elevation =   0.00000     deg                             
 heading   =   0.00000     deg                             
 Mach      =  {5}                                    
 velocity  =   0.00000     Lunit/Tunit                     
 density   =   1.00000     Munit/Lunit^3                   
 grav.acc. =   1.00000     Lunit/Tunit^2                   
 turn_rad. =   0.00000     Lunit                           
 load_fac. =   0.00000                                     
 X_cg      =   {6}     Lunit                           
 Y_cg      =   {7}     Lunit                           
 Z_cg      =   {8}     Lunit                           
 mass      =   1.00000     Munit                           
 Ixx       =   1.00000     Munit-Lunit^2                   
 Iyy       =   1.00000     Munit-Lunit^2                   
 Izz       =   1.00000     Munit-Lunit^2                   
 Ixy       =   0.00000     Munit-Lunit^2                   
 Iyz       =   0.00000     Munit-Lunit^2                   
 Izx       =   0.00000     Munit-Lunit^2                   
 visc CL_a =   0.00000                                     
 visc CL_u =   0.00000                                     
 visc CM_a =   0.00000                                     
 visc CM_u =   0.00000  

'''#{4} is a set of control surface inputs that will vary depending on the control surface configuration

    # unpack inputs
    batch_filename = Input.batch_file
    
    x_cg    = Input.CG[0]
    y_cg    = Input.CG[1]
    z_cg    = Input.CG[2]
    
    alpha   = Input.AoA
    beta    = Input.AoS
    mach    = Input.Mach 
    
    '''moments_of_inertia = aircraft.mass_properties.moments_of_inertia.tensor
    Ixx  = moments_of_inertia[0][0]
    Iyy  = moments_of_inertia[1][1]
    Izz  = moments_of_inertia[2][2]
    Ixy  = moments_of_inertia[0][1]
    Iyz  = moments_of_inertia[1][2]
    Izx  = moments_of_inertia[2][0]'''

    batch_index = 1
    full_batch_name = batch_filename + str(batch_index) + '.batch'
    if os.path.exists(full_batch_name):
        os.remove(full_batch_name)

    f = open(full_batch_name, 'a')  

    index_tot = 0
    index     = 0

    for i in range(len(mach)):
        for j in range(len(beta)):
            for k in range(len(alpha)):                      
                # create the case name
                case = 'case_' + str(index_tot+1)
                # form controls text
                controls = []
                if Input.controls:
                    for cs in Input.controls:
                        cs_text = make_controls_case_text(cs)
                        controls.append(cs_text)
                controls_text = ''.join(controls)
                case_text = base_case_text.format(index+1,case,alpha[k],beta[j],controls_text,mach[i],
                                                  x_cg,y_cg,z_cg)
                f.write(case_text)

                # limiter to create a new case file
                if index == 24:
                    f.close()
                    batch_index = batch_index +1 
                    f = open(batch_filename + str(batch_index) + '.batch', 'a')  
                    index = 0
                else:
                    index = index + 1
                    
                index_tot = index_tot + 1


    # pack outputs
    Input.index_total = index_tot
    Input.batch_index = batch_index 
    
    return 


def make_controls_case_text(control_deflection):
    """ This function writes the text of the control surfaces in the AVL batch analysis

    Assumptions:
        None
        
    Source:
        Drela, M. and Youngren, H., AVL, http://web.mit.edu/drela/Public/web/avl

    Inputs:
        control_deflection.tag                                  [-]
        control_deflection.deflection                           [-]
    Outputs: 
        controls_case_text                                      [-]
 
    Properties Used:
        N/A
    """  
    base_control_cond_text = '{0}      ->  {0}     =   {1}    \n'

    # Unpack inputs
    name = control_deflection.tag
    d    = control_deflection.deflection

    # Form text
    controls_case_text = base_control_cond_text.format(name,d)

    return controls_case_text
