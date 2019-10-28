from __future__ import print_function
import os
import sys
import pcbnew
import numpy as np
import pprint


def inch_to_nanometer(value):
    return (value*25.4)*1e6

def nanometer_to_inch(value):
    return value/(25.4*1.e6)

def nm_to_mm(value):
    return value*1.e-6 

def mm_to_nm(value):
    return value*1.e6

def print_module_info(module):
    ref = module.GetReference()
    pos = module.GetPosition()
    x = nanometer_to_inch(pos.x)
    y = nanometer_to_inch(pos.y)
    angle = 0.1*module.GetOrientation()
        
    print('  R: {}'.format(ref))
    print('  X: {}'.format(x))
    print('  Y: {}'.format(y))
    print('  A: {}'.format(angle))
    print()

def get_placement_data(param):
    placement_data = {}
    for i, ref in enumerate(param['ref_list']):
        x = param['x_start'] + i*param['x_step']
        y = param['y_value']
        angle = param['angle']
        placement_data[ref] = {'angle': angle, 'x': x, 'y': y} 
    return placement_data

def place_pcb_modules(filename, placement_data):
    print()
    print('loading pcb: {}'.format(filename))
    print()
    pcb = pcbnew.LoadBoard(filename)
    print()
    print('done')
    print()
    for module in pcb.GetModules():
        ref_str = str(module.GetReference())
        try:
            data = placement_data[ref_str]
        except KeyError:
            continue
        print_module_info(module)
    
        # Move to new position
        pos = module.GetPosition()
        angle = 0.1*module.GetOrientation()
        x_new = data['x']
        y_new = data['y']
        angle_new = data['angle']
        pos.x = int(mm_to_nm(x_new))
        pos.y = int(mm_to_nm(y_new))
        module.SetPosition(pos)
        module.SetOrientation(10.0*angle_new)
        print_module_info(module)
    
    pathname, basename = os.path.split(filename)
    new_basename = 'mod_{}'.format(basename)
    new_filename = os.path.join(pathname,new_basename)
    pcb.Save(new_filename)




# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    param = {
                'ref_list': ['J{}'.format(i) for i in range(1,19)],
                'y_value' : 56.0,
                'x_start' : 50.0+39.5, 
                'x_step'  : 13.0,
                'angle'   : 180.0,
            }
    
    placement_data = get_placement_data(param)
    
    if 0:
        print('led_data')
        print()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(placement_data)
        print()
    print('modules')
    print()
    
    filename = sys.argv[1]
    place_pcb_modules(filename, placement_data)




        

