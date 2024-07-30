import argparse

import numpy as np
from woa import WOA
from animate_scratter import AnimateScatter
from functions import schaffer, eggholder, booth, matyas, cross_in_tray, levi


def parse_cl_args():
    parser = argparse.ArgumentParser()
    # Số giải pháp
    parser.add_argument("-nsols", type=int, default=50, dest='nsols') 
    # Số lần lặp, 
    parser.add_argument("-ngens", type=int, default=20, dest='ngens') 
    # Control Search Speread
    parser.add_argument("-a", type=float, default=2.0, dest='a')
    # Control Spiral
    parser.add_argument("-b", type=float, default=0.5, dest='b')  
    # Default Constrain, 
    parser.add_argument("-c", type=float, default=None, dest='c') 
    # Objective Func, 
    parser.add_argument("-func", type=str, default='cross', dest='func')
    # Độ dày của Lưới, 
    parser.add_argument("-r", type=float, default=0.25, dest='r')
    # Thời gian Xuất Hình, 
    parser.add_argument("-t", type=float, default=0.1, dest='t')
    # Tối thiểu hoặc Tối đa hoá
    parser.add_argument("-max", default=False, dest='max', action='store_true')

    args = parser.parse_args()
    print(args)
    return args


def main():
    args = parse_cl_args()

    nsols = args.nsols # Number of solutions 
    ngens = args.ngens # Number of loop

    funcs = {'schaffer':schaffer, 'eggholder':eggholder, 'booth':booth, 'matyas':matyas, 'cross':cross_in_tray, 'levi':levi}
    func_constraints = {'schaffer':100.0, 'eggholder':512.0, 'booth':10.0, 'matyas':10.0, 'cross':10.0, 'levi':10.0}

    # Kiểm tra Objective function có tồn tại trong Dict vừa khởi tạo hay không
    if args.func in funcs:
        func = funcs[args.func]
    else:
        print('Missing supplied function ' + args.func + ' definition. Ensure function defintion exists or use command line options.')
        return

    if args.c is None:
        if args.func in func_constraints:
            args.c = func_constraints[args.func] # cập nhật ràng buộc từ Dict trên
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
    colors = [[1.0, 1.0, 1.0] for _ in range(nsols)] # RGB White

    a_scatter = AnimateScatter(constraints[0][0], # giới hạn dưới chiều thứ 1
                               constraints[0][1], # giới hạn trên chiều thứ 1
                               constraints[1][0], # giới hạn dưới chiều thứ 2
                               constraints[1][1], # giới hạn trên chiều thứ 2
                               solutions, colors, opt_func, args.r, args.t)
    for _ in range(ngens):
        opt_alg.optimize()
        solutions = opt_alg.get_solutions()
        a_scatter.update(solutions)
        opt_alg.print_best_solutions()

if __name__ == '__main__':
    main()
