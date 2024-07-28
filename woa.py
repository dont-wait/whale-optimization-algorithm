import numpy as np

class WOA():
    def __init__(self, fitness_func, constants, n_solutions, b, a, a_step
                 , maximize=False):
        self._fitness_func = fitness_func
        self._constants = constants # lb up
        self._solutions = self._init_solutions(n_solutions) # best_solutions if end for
        self._b = b
        self._a = a
        self._a_step = a_step
        self.maximize = maximize
        self._best_solution = []
    
    
    # Khởi tạo quần thể    
    def _init_solutions(self, n_solutions):
        solutions = [] 
        for c in self._constants:
            solutions.append(np.random.uniform(c[0], c[1], size= n_solutions))
        solutions = np.stack(solutions, axis=-1)
        
        return solutions
    
    
    # Đảm bảo solution không vượt biên
    # Ensure solution don't out by side lower, upper bound
    def _constrain_solution(self, solution):
        constrain_s = []
        for c, s in zip(self._constants, solution):
            if c[0] > s:
                s = c[0] 
            elif c[1] < s:
                s = c[1]
            constrain_s.append(s)
        return constrain_s
    
    
    def _rank_solution(self):
        """Find best solution"""
        fitness_score = self._fitness_func(self._solutions[:, 0], self._solutions[:, 1])
        
        """Sắp xếp lại thứ tự theo fitness giảm dần"""
        # Càng nhỏ thì càng đúng
        idx = np.argsort(fitness_score)[::-1] if self._maximize else np.argsort(fitness_score)
        # Tạo 1 mảng lần lượt chứa các giá trị fitness thì nhỏ đến cao
        # Nhỏ nhất là tốt nhất trong case này
        rank_solutions = self._solutions[idx] 
        # Lấy ra điểm + giải pháp tương ứng với điểm đó
        self._best_solution.append((fitness_score[idx[0]], rank_solutions[0]))
        return rank_solutions
        
        
    def _get_solutions(self): 
        return self._solutions
    
    
    # r[0, 1]
    # A[2, 0]
    def _compute_A(self):
        r = np.random.uniform(0.0, 1.0, size=2)
        return 2 * np.multiply(self._a * r) - self._a
    
    
    def _compute_C(self):
        return 2 * np.random.uniform(0.0, 1.0, size=2)
    
    
    # Cập nhật vị trí theo con đầu đàn
    # Tiến lại gần con đầu đàn hơn
    # Update position to leader_pos
    def _encircle_D(self, solution, best_solution):
        C = self._compute_C() # 2.4
        D = np.linalg.norm(np.multiply(C, best_solution) - solution) # 2.1
        return D
    
    
    def _encircle(self, solution, best_solution, A):
        D = self._encircle_D(solution, best_solution)
        return best_solution - np.multiply(A, D) # 2.2
    
    
    #Thực hiện tìm kiếm con mồi | khám phá
    def _search_D(self, solutions, random_solution):
        C = self._compute_C() # C = 2r
        return np.linalg.norm(np.multiply(C, random_solution) - solutions) # 2.7
    
    
    def _search(self, solution, random_solution, A):
        D = self._search_D(solution, random_solution, A)
        return random_solution - np.multiply(A, D) # 2.8
    
    
    # Tấn công xoắn ốc
    # Bubble-net attacking
    def _attack(self, solution, best_solution):
        D = np.linalg.norm(best_solution - solution)
        L = np.random.uniform(-1.0, 1.0, size=2)
        return np.multiply(np.multiply(D, np.exp(self._b)), 
                           np.cos(2.0 * np.pi * L)
                          )
    
    
    def print_best_solutions(self):
        print('generation best solution history')
        print('([fitness], [solution])')
        for s in self._best_solution:
            print(s)
        print(end='\n')
        print('best solution')
        print('([fitness], [solution])')
        print(sorted(self._best_solution, key=lambda x:x[0], reverse=self.maximize[0]))
   
   
    def optimize(self):
        rank_solution = self._rank_solution()
        best_solution = rank_solution[0] # ban đầu cho idx 0 là giá trị thích nghi tốt nhất
        new_solutions = [best_solution]
        p = np.random.uniform(0.0, 1.0)
       
        for s in rank_solution[1:]:
            if p > 0.5:
               A = self._compute_A
               norm_A = np.linalg.norm(A)
               if norm_A < 1.0:
                   new_s = self._encircle(s, best_solution, A)
               else:
                    random_solution = self._solutions[np.random.randint(self._solution.shape[0])] # Chọn 1 con trong đàn
                    new_s = self._search(s, random_solution, A) # bơi theo con đó
            elif p < 0.5:
                new_s = self._attack(s, best_solution)
            new_solutions.append(self._constants(new_s))
        self._solutions = np.stack(new_s)
        self._a -= self._a_step      
                
       
             
        
    
        
    