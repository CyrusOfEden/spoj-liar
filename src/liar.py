from problem_domain import Paradox, HonestyRelationships, ConcludedHonestyState
from solvers import DFS, BFS


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

    concluded_states = [
        s for initial_state in starting_states for s in BFS(initial_state)()
    ]

    if not concluded_states:
        raise Paradox()

    return (min(concluded_states).liar_count(),
            max(concluded_states).liar_count())


def spoj():
    import sys
    class_surveys = load_classes(sys.stdin)
    for index, survey in enumerate(class_surveys):
        try:
            atleast, atmost = class_score(survey)
        except Paradox:
            print("Class Room#%s is paradoxical" % (index + 1))
        else:
            print("Class Room#%s contains atleast %d and atmost %d liars" %
                  (index + 1, atleast, atmost))


def test():
    class_surveys = load_classes(open("../test.txt"))
    expected = [None, (0, 3), (3, 4), (4, 4)]
    for index, (survey, expected) in enumerate(zip(class_surveys, expected)):
        try:
            atleast, atmost = class_score(survey)
        except Paradox:
            assert expected is None
            print("Class Room#%s is paradoxical" % (index + 1))
        else:
            assert atleast == expected[0]
            assert atmost == expected[1]
            print("Class Room#%s contains atleast %d and atmost %d liars" %
                  (index + 1, atleast, atmost))


if __name__ == "__main__":
    # spoj()
    test()
