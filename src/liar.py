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


def students(state, other_than=None):
    return (j for j in range(len(state)) if j != other_than)


def conclusion(replies, starting_with):
    i, i_is_honest = starting_with
    state = [None] * len(replies)
    state[i] = i_is_honest
    for j in students(replies, other_than=i):
        j_is_honest = state[j]
        if i_is_honest:
            "i is honest"
            if replies[j][i]:
                state[j] = i_is_honest
            elif replies[i][j]:
                return None, False
            else:
                state[j] = replies[i][j]
        elif replies[j][i]:
            "j says i is honest, but i is not honest"
            state[j] = False
    return state, True


def validated(replies, state):
    for i, i_is_honest in enumerate(state):
        i_lied = False
        conclusive = False
        for j in students(state, other_than=i):
            if (replies[i][j] or replies[j][i]):
                conclusive = True
            if state[j] is not None and replies[i][j] != state[j]:
                i_lied = True
                break
        if conclusive:
            if i_is_honest is not None and i_is_honest == i_lied:
                return None, False
            state[i] = not i_lied
    return state, True


def concluded_states(replies):
    for i in students(replies):
        for assumption in (True, False):
            state, ok = conclusion(replies, starting_with=(i, assumption))
            if not ok:
                continue
            state, ok = validated(replies, state)
            if ok:
                yield state


def class_score(replies):
    possible_states = list(concluded_states(replies))

    if not possible_states:
        return None, False

    liars_count = sorted([
        sum(1 for honest_student in possibility if not honest_student)
        for possibility in possible_states
    ])

    return (liars_count[0], liars_count[-1]), True


def print_class_score(index, class_survey):
    score, ok = class_score(class_survey)
    if not ok:
        print("Class Room#%s is paradoxical" % (index + 1))
    else:
        atleast, atmost = score
        print("Class Room#%s contains atleast %d and atmost %d liars" %
              (index + 1, atleast, atmost))


def run(in_file):
    class_surveys = load_classes(in_file)
    for class_number, class_survey in enumerate(class_surveys):
        print_class_score(class_number, class_survey)


if __name__ == "__main__":
    run(open("../test.txt"))
    # from sys import stdin
    # run(stdin)
