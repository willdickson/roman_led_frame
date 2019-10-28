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
    for name in ('left', 'right'):
        try:
            sub_param = param[name]
        except KeyError:
            continue
        placement_data.update(get_placement_vert(sub_param))

    for name in ('top', 'bottom'):
        try:
            sub_param = param[name]
        except KeyError:
            continue
        placement_data.update(get_placement_hori(sub_param))
    return placement_data

def get_placement_vert(param):
    placement_data = {}
    for i, ref in enumerate(param['ref_list']):
        x = param['x_value']
        y = param['y_start'] + i*param['y_step']
        angle = param['angle']
        placement_data[ref] = {'angle': angle, 'x': x, 'y': y} 
    return placement_data

def get_placement_hori(param):
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

    param_left = {
                'ref_list': ['J{}'.format(i) for i in range(19+0*9,19+1*9)],
                'x_value' : 50 + 10,
                'y_start' : 85 + 190/10.0,
                'y_step'  : 190/10.0,
                'angle'   : 270.0,
            }

    param_bottom = {
                'ref_list': ['J{}'.format(i) for i in range(19+1*9,19+2*9)],
                'y_value' : 310 - 10,
                'x_start' : 85 + 230/10.0,
                'x_step'  : 230/10.0,
                'angle'   : 0.0,
            }

    param_right = {
                'ref_list': reversed(['J{}'.format(i) for i in range(19+2*9,19+3*9)]),
                'x_value' : 350 - 10,
                'y_start' : 85 + 190/10.0,
                'y_step'  : 190/10.0,
                'angle'   : 270.0,
            }

    param_top = {
                'ref_list': reversed(['J{}'.format(i) for i in range(19+3*9,19+4*9)]),
                'y_value' : 50 + 22,
                'x_start' : 85 + 230/10.0,
                'x_step'  : 230/10.0,
                'angle'   : 0.0,
            }


    param = {
            'left'   : param_left,
            'bottom' : param_bottom,
            'right'  : param_right,
            'top'    : param_top,
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




        

