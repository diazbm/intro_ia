import tracemalloc
import time

from hanoi_states import StatesHanoi
from hanoi_states import ProblemHanoi
from tree_hanoi import NodeHanoi

# Inicializamos variables de control de tiempo y memoria
tracemalloc.start()
start_time = time.time()

# Inicializamos el problema
initial_state = StatesHanoi([5, 4, 3, 2, 1], [], [], max_disks=5)
goal_state = StatesHanoi([], [], [5, 4, 3, 2, 1], max_disks=5)
problem = ProblemHanoi(initial=initial_state, goal=goal_state)

frontier = [NodeHanoi(problem.initial)]  # Creamos una cola FIFO con el nodo inicial

explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente

# Mientras que la cola no este vacia
quantity_of_steps = 0
while len(frontier) != 0:
    node = frontier.pop()  # Extraemos el último nodo de la cola
    
    # Agregamos nodo al set. Esto evita guardar duplicados, porque set nunca tiene elementos repetidos
    explored.add(node.state)
    
    if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
        last_node = node
        break
    
    # Agregamos a la cola todos los nodos sucesores del nodo actual
    for next_node in node.expand(problem):
        # Solo si no fue explorado
        if next_node.state not in explored:
            print(next_node.state)
            quantity_of_steps = quantity_of_steps + 1
            frontier.append(next_node)
            
_, memory_peak = tracemalloc.get_traced_memory()
memory_peak /= 1024*1024
tracemalloc.stop()

print(f"Cantidad de pasos para llegar a la solución: {quantity_of_steps}")
print(f"Duración total de la ejecución: {(time.time() - start_time)}s")
print(f"Maxima memoria ocupada: {round(memory_peak, 2)} [MB]", )