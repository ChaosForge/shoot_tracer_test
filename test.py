#!/usr/bin/env python3

import utils 
import os 
from shot_tracer import trace_shot
from shot_tracer import refine_src_position
from line_tracer import line_type, normal_traceline

CANVAS_SIZE = (16, 16)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_case(map_file_name, output_file_name):
    p = utils.picture(CANVAS_SIZE[0],CANVAS_SIZE[1])
    m,player_pos,enemy_pos,expected_result,width,height = utils.load_map(map_file_name,CANVAS_SIZE)
    utils.draw_map(m,p)
    r,succ = trace_shot(m,player_pos,enemy_pos)
    r1,succ1 = trace_shot(m,enemy_pos,player_pos)
    
    rr_f,_ = normal_traceline(line_type.FLOOR,player_pos,enemy_pos)
    rr_c,_ = normal_traceline(line_type.CEIL,player_pos,enemy_pos)

    utils.draw_route(r,p,(64,255,64,180))
    utils.draw_route(r1,p,(255,64,64,180))
    utils.draw_route(rr_f,p,(64,64,180,32))
    utils.draw_route(rr_c,p,(64,180,64,32))

    p.save(output_file_name)
    if succ == expected_result and succ1 == expected_result:
        print(bcolors.OKGREEN + "{} [OK]".format(map_file_name) + bcolors.ENDC)
    else: 
        print(bcolors.FAIL + "{} [FAILED]".format(map_file_name) + bcolors.ENDC)

def run_test_cases():
    cases_path = "cases"
    results_path = "results"

    test_cases = [f for f in os.listdir(cases_path) if os.path.isfile(os.path.join(cases_path,f))]
    test_cases.sort()
    for f in test_cases:
        name, ext = os.path.splitext(f)
        run_case(os.path.join(cases_path, f ), os.path.join(results_path,name + ".png"))

run_test_cases()


