from queue import Queue, PriorityQueue


class ProceduralSolver():
    def __init__(self, initial_state):
        self.state = initial_state


class DFS(ProceduralSolver):
    def __call__(self):
        stack = [self.state]
        while stack:
            state = stack.pop()
            if state.is_solution():
                yield state
            stack += list(state.frontier())


class BFS(ProceduralSolver):
    def __call__(self):
        queue = Queue()
        queue.put(self.state)
        while not queue.empty():
            state = queue.get()
            if state.is_solution():
                yield state
            for next_state in state.frontier():
                queue.put(next_state)


class BestSearch(ProceduralSolver):
    def __call__(self, cost):
        queue = PriorityQueue()
        queue.put((cost(self.state), self.state))
        while not queue.empty():
            state_cost, state = queue.get()
            if state.is_solution():
                return state
            for next_state in state.frontier():
                queue.put((cost(next_state), next_state))
