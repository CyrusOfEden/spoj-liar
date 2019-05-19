from queue import Queue, PriorityQueue

from problem_domain import Paradox, HonestyRelationships, ConcludedHonestyState


class StateSearch():
    def __init__(self, initial_state):
        self.state = initial_state

    def depth_search(self):
        stack = [self.state]
        while stack:
            state = stack.pop()
            if state.is_solution():
                yield state
            stack += list(state.frontier())

    def breadth_search(self):
        queue = Queue()
        queue.put(self.state)
        while not queue.empty():
            state = queue.get()
            if state.is_solution():
                yield state
            for next_state in state.frontier():
                queue.put(next_state)

    def best_search(self, cost):
        queue = PriorityQueue()
        queue.put((cost(self.state), self.state))
        while not queue.empty():
            state_cost, state = queue.get()
            if state.is_solution():
                return state
            for next_state in state.frontier():
                queue.put((cost(next_state), next_state))


def load_classes(from_file):
    """Given a source file object, return all class cases."""
    from_file.seek(0)
    test_cases = int(from_file.readline().strip())
    classes = [parse_one_class(from_file) for _ in range(test_cases)]
    return classes


def parse_one_class(from_file):
    """Given a Python file object, construct a 2D `class_survey` array of booleans."""
    student_count = int(from_file.readline().strip())
    replies = [[] for _ in range(student_count)]
    for i in range(student_count):
        for char in from_file.readline().strip():
            # True for when they're truthful, False for when they're a liar.
            replies[i].append(char == 'T')
    return replies


def class_score(class_survey):
    domain = HonestyRelationships(class_survey)
    starting_states = [
        ConcludedHonestyState([value], domain) for value in (True, False, None)
    ]

    valid_states = [
        s for initial_state in starting_states
        for s in StateSearch(initial_state).depth_search()
    ]

    if not valid_states:
        raise Paradox()

    return (min(valid_states).liar_count(), max(valid_states).liar_count())


if __name__ == "__main__":
    class_surveys = load_classes(open("../sample.txt"))
    # import sys
    # class_surveys = load_classes(sys.stdin)
    for index, survey in enumerate(class_surveys):
        try:
            atleast, atmost = class_score(survey)
        except Paradox:
            print("Class Room#%s is paradoxical" % (index + 1))
        else:
            print("Class Room#%s contains atleast %d and atmost %d liars" %
                  (index + 1, atleast, atmost))
