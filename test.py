#!/usr/bin/env python3

import utils 
import os 
from shoot_tracer import trace_shoot

CANVAS_SIZE = (16, 16)

def run_case(map_file_name, output_file_name):
    p = utils.picture(CANVAS_SIZE[0],CANVAS_SIZE[1])
    m,player_pos,enemy_pos,expected_result,width,height = utils.load_map(map_file_name,CANVAS_SIZE)
    utils.draw_map(m,p)
    r,succ = trace_shoot(m,player_pos,enemy_pos)
    r1,succ1 = trace_shoot(m,enemy_pos,player_pos)

    utils.draw_route(r,p,(64,220,0,180))
    utils.draw_route(r1,p,(220,64,0,180))

    p.save(output_file_name)
    if succ == expected_result and succ1 == expected_result:
        print("{} [OK]".format(map_file_name))
    else: 
        print("{} [FAILED]".format(map_file_name))

def run_test_cases():
    cases_path = "cases"
    results_path = "results"

    test_cases = [f for f in os.listdir(cases_path) if os.path.isfile(os.path.join(cases_path,f))]
    for f in test_cases:
        name, ext = os.path.splitext(f)
        run_case(os.path.join(cases_path, f ), os.path.join(results_path,name + ".png"))


run_test_cases()


