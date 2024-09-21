import tracemalloc
import time
import json

from hanoi_states import StatesHanoi
from hanoi_states import ProblemHanoi
from tree_hanoi import NodeHanoi

# Inicializamos variables de control de tiempo y memoria
tracemalloc.start()
start_time = time.perf_counter()

# Problema y condiciones iniciales
initial_state = StatesHanoi([5, 4, 3, 2, 1], [], [], max_disks=5)
goal_state = StatesHanoi([], [], [5, 4, 3, 2, 1], max_disks=5)
problem = ProblemHanoi(initial=initial_state, goal=goal_state)

lifo_frontier = [NodeHanoi(problem.initial)]  # Creamos una cola LIFO con el nodo inicial

explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente

quantity_of_steps = 0 # Inicializa la cantidad de pasos
steps = [] # Inicializa la lista de pasos
while len(lifo_frontier) != 0:
    node = lifo_frontier.pop()  # Extraemos el último nodo de la cola
    
    # Sumar nodo al set de explorados
    explored.add(node.state)
    
    if problem.goal_test(node.state):  # Comprobación
        last_node = node
        last_node.generate_solution_for_simulator()
        break
    

    for next_node in node.expand(problem):
        if next_node.state not in explored:
            print(next_node.state)
            quantity_of_steps = quantity_of_steps + 1
            lifo_frontier.append(next_node) # En las colas LIFO se hace un append.

            action_representation = next_node.action.__dict__
            action_dict = action_representation.get("action_dict") # Sacamos el json de la acción para que la use el simulador
            print("-------------------------")
            steps.append(action_dict) # Suma el json que representa a la acción en una lista de pasos.
            
_, memory_peak = tracemalloc.get_traced_memory()
memory_peak /= 1024*1024
tracemalloc.stop()

end_time = time.perf_counter()
elapsed_time = end_time - start_time

with open('sequence_profundidad.json', 'w') as fp:
    json.dump(steps, fp)

print(f"Cantidad de pasos para llegar a la solución: {quantity_of_steps}")
print(f"Tiempo que demoró: {elapsed_time} [s]", )
print(f"Maxima memoria ocupada: {round(memory_peak, 2)} [MB]", )