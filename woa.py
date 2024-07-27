import numpy as np

class WOA():
    def __init__(seft, fitness_func, constants, n_solutions, b, a, a_step, maximize=False):
        seft._fitness_func = fitness_func
        seft._constants = constants # lb up
        seft._solutions = seft._init_solutions(n_solutions) # best_solutions if end for
        seft._b = b
        seft._a = a
        seft._a_step = a_step
        seft.maximize = maximize
        seft._best_solution = []
    
    # Khởi tạo quần thể    
    def _init_solutions(seft, n_solutions):
        solutions = [] 
        for c in seft._constants:
            solutions.append(np.random.uniform(c[0], c[1], size= n_solutions))
        solutions = np.stack(solutions, axis=-1)
        
        return solutions
    def _rank_solution(seft):
        """Find best solution"""
        fitness = seft._fitness_func()
    def _get_solutions(seft): 
        return seft._solutions
    
    # r[0, 1]
    def _compute_A(seft):
        r = np.random.uniform(0.0, 1.0, size=2)
        return 2 * np.multiply(seft._a * r) - seft._a
    def _compute_C(seft):
        return 2 * np.random.uniform(0.0, 1.0, size=2)
    
    # Cập nhật vị trí theo con đầu đàn
    # Tiến lại gần con đầu đàn hơn
    # Update position to leader_pos
    def _encircle_D(seft, solution, best_solution):
        C = seft._compute_C() # 2.4
        D = np.linalg.norm(np.multiply(C, best_solution) - solution) # 2.1
        return D
    def _encircle(seft, solution, best_solution, A):
        D = seft._encircle_D(solution, best_solution)
        return best_solution - np.multiply(A, D) # 2.2
    
    #Thực hiện tìm kiếm con mồi | khám phá
    def _search_D(seft, solutions, random_solution):
        C = seft._compute_C() # C = 2r
        return np.linalg.norm(np.multiply(C, random_solution) - solutions) # 2.7
    def _search(seft, solution, random_solution, A):
        D = seft._search_D(solution, random_solution, A)
        return random_solution - np.multiply(A, D) # 2.8
    
    # Tấn công xoắn ốc
    # Bubble-net attacking
    def _attack(seft, solution, best_solution):
        D = np.linalg.norm(best_solution - solution)
        L = np.random.uniform(-1.0, 1.0, size=2)
        return np.multiply(np.multiply(D, np.exp(seft._b)), 
                           np.cos(2.0 * np.pi * L)
                          )
        
    
        
    