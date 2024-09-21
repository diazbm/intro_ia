import tracemalloc
import time
import queue

from hanoi_states import StatesHanoi
from hanoi_states import ProblemHanoi
from tree_hanoi import NodeHanoi

# Inicializamos variables de control de tiempo y memoria
tracemalloc.start()
start_time = time.perf_counter()

# Definir la función heurística para el problema de Hanoi
def h(state, goal_state):
    torre_actual = state.rods[2]
    
    discos_correctos = 0
    for i, disco in enumerate(reversed(torre_actual)):
        if disco == len(goal_state.rods[0]) - i:
            discos_correctos += 1
        else:
            break
    
    return -discos_correctos # Retorna el negativo de los nodos correctos como en el ejemplo de la ppt de la clase2


# Problema y condiciones iniciales
initial_state = StatesHanoi([5, 4, 3, 2, 1], [], [], max_disks=5)
goal_state = StatesHanoi([], [], [5, 4, 3, 2, 1], max_disks=5)
problem = ProblemHanoi(initial=initial_state, goal=goal_state)

# Priority Queue para la búsqueda A*
priority_queue = queue.PriorityQueue() # Usamos la librería queue para generar una PriorityQueue
priority_queue.put((0, NodeHanoi(problem.initial)))  # Insertamos el nodo inicial con prioridad 0

explored = set()  # Para rastrear los estados ya explorados

quantity_of_steps = 0  # Inicializa la cantidad de pasos

# Algoritmo A*
while not priority_queue.empty():
    # Extraemos el nodo con menor costo acumulado + heurística
    _, node = priority_queue.get()

    # Sumar nodo al set de explorados
    explored.add(node.state)

    if problem.goal_test(node.state):  # Comprobación si hemos llegado al estado objetivo
        last_node = node
        print(f'Longitud del camino de la solución: {last_node.state.accumulated_cost}')
        last_node.generate_solution_for_simulator()
        break

    # Expandimos los nodos hijos
    for next_node in node.expand(problem):
        if next_node.state not in explored:
            # Calcular el costo acumulado (g) y el valor heurístico (h)
            costo = next_node.state.accumulated_cost  # Costo acumulado
            f = costo + h(next_node.state, goal_state)  # f(nodo) = costo(nodo) + h(nodo)

            # Agregar el nodo a la Priority Queue con su costo f
            priority_queue.put((f, next_node))
            print(next_node.state)
            quantity_of_steps += 1
            print("-------------------------")

# Medir memoria y tiempo
_, memory_peak = tracemalloc.get_traced_memory()
memory_peak /= 1024*1024
tracemalloc.stop()

end_time = time.perf_counter()
elapsed_time = end_time - start_time

# Imprimir resultados
print(f"Cantidad de pasos para llegar a la solución: {quantity_of_steps}")
print(f"Tiempo que demoró: {elapsed_time} [s]")
print(f"Máxima memoria ocupada: {round(memory_peak, 2)} [MB]")
