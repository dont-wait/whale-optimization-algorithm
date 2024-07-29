import argparse

import numpy as np
from woa import WOA
from animate_scratter import AnimateScatter
from functions import schaffer, eggholder, booth, matyas, cross_in_tray, levi


def parse_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-nsols", type=int, default=100, dest='nsols', help='number of solutions per generation, default: 50')
    parser.add_argument("-ngens", type=int, default=20, dest='ngens', help='number of generations, default: 20')
    parser.add_argument("-a", type=float, default=2.0, dest='a', help='woa algorithm specific parameter, controls search spread default: 2.0')
    parser.add_argument("-b", type=float, default=0.5, dest='b', help='woa algorithm specific parameter, controls spiral, default: 0.5')
    parser.add_argument("-c", type=float, default=None, dest='c', help='absolute solution constraint value, default: None, will use default constraints')
    parser.add_argument("-func", type=str, default='cross', dest='func', help='function to be optimized, default: booth; options: matyas, cross, eggholder, schaffer, booth')
    parser.add_argument("-r", type=float, default=0.25, dest='r', help='resolution of function meshgrid, default: 0.25')
    parser.add_argument("-t", type=float, default=0.1, dest='t', help='animate sleep time, lower values increase animation speed, default: 0.1')
    parser.add_argument("-max", default=False, dest='max', action='store_true', help='enable for maximization, default: False (minimization)')

    args = parser.parse_args()
    return args


def main():
    args = parse_cl_args()

    nsols = args.nsols
    ngens = args.ngens

    funcs = {'schaffer':schaffer, 'eggholder':eggholder, 'booth':booth, 'matyas':matyas, 'cross':cross_in_tray, 'levi':levi}
    func_constraints = {'schaffer':100.0, 'eggholder':512.0, 'booth':10.0, 'matyas':10.0, 'cross':10.0, 'levi':10.0}

    if args.func in funcs:
        func = funcs[args.func]
    else:
        print('Missing supplied function ' + args.func + ' definition. Ensure function defintion exists or use command line options.')
        return

    if args.c is None:
        if args.func in func_constraints:
            args.c = func_constraints[args.func]
        else:
            print('Missing constraints for supplied function ' + args.func + '. Define constraints before use or supply via command line.')
            return

    C = args.c
    constraints = [[-C, C], [-C, C]]

    opt_func = func

    b = args.b
    a = args.a
    a_step = a / ngens

    maximize = args.max

    opt_alg = WOA(opt_func, constraints, nsols, b, a, a_step, maximize)
    solutions = opt_alg.get_solutions()
    colors = [[1.0, 1.0, 1.0] for _ in range(nsols)]

    a_scatter = AnimateScatter(constraints[0][0], 
                               constraints[0][1], 
                               constraints[1][0], 
                               constraints[1][1], 
                               solutions, colors, opt_func, args.r, args.t)
    for _ in range(ngens):
        opt_alg.optimize()
        solutions = opt_alg.get_solutions()
        a_scatter.update(solutions)
        opt_alg.print_best_solutions()

if __name__ == '__main__':
    main()
