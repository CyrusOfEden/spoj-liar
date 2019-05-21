from __future__ import print_function


def load_classes(from_file):
    test_cases = int(next(from_file))
    classes = [None] * test_cases
    for i in range(test_cases):
        count = int(next(from_file))
        classes[i] = [[c == 'T' for c in next(from_file)]
                      for _ in range(count)]
    return classes


def conclusion(replies, count, starting_with):
    i, i_is_honest = starting_with
    state = [None] * count
    state[i] = i_is_honest
    # Concluding what we can
    for j in range(count):
        if i == j:
            continue
        j_is_honest = state[j]
        j_as_per_i = replies[i][j]
        i_as_per_j = replies[j][i]
        if i_as_per_j == j_as_per_i:
            state[j] = i_is_honest
        if i_is_honest:
            if j_as_per_i is True and i_as_per_j is False:
                return None, False
            state[j] = j_as_per_i
        elif replies[j][i]:
            state[j] = False
    # Here we're deciding whether each student was honest, or lied
    for i, i_is_honest in enumerate(state):
        i_lied = False
        conclusive = False
        for j in range(count):
            if i == j:
                continue
            j_is_honest = state[j]
            j_as_per_i = replies[i][j]
            i_as_per_j = replies[j][i]
            if j_as_per_i or i_as_per_j:
                conclusive = True
            if j_is_honest is not None and j_as_per_i != j_is_honest:
                i_lied = True
                break
        if conclusive:
            if i_is_honest is None:
                state[i] = not i_lied
            elif i_is_honest == i_lied:
                return None, False
    return state, True


def class_score(replies):
    count = len(replies)
    min_liars = count
    max_liars = -1

    for i in range(count):
        for assumption in (True, False):
            state, ok = conclusion(replies,
                                   count,
                                   starting_with=(i, assumption))
            if not ok:
                continue
            liar_count = sum(1 for v in state if not v)
            if liar_count > max_liars:
                max_liars = liar_count
            elif liar_count < min_liars:
                min_liars = liar_count

    if max_liars == -1:
        return None, False

    return (min_liars, max_liars), True


def print_class_score(index, class_survey):
    score, ok = class_score(class_survey)
    if not ok:
        print("Class Room#%s is paradoxical" % index)
    else:
        atleast, atmost = score
        print("Class Room#%s contains atleast %d and atmost %d liars" %
              (index, atleast, atmost))


def run(in_file):
    class_surveys = load_classes(in_file)
    for index, class_survey in enumerate(class_surveys):
        print_class_score(index + 1, class_survey)


if __name__ == "__main__":
    # run(open("../test.txt"))
    from sys import stdin
    run(stdin)
