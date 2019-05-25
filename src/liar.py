from __future__ import print_function

try:
    xrange = range
except NameError:
    pass


def load_classes(from_file):
    test_cases = int(next(from_file))
    classes = [None] * test_cases
    for i in range(test_cases):
        count = int(next(from_file))
        classes[i] = [[c == 'T' for c in next(from_file).strip()]
                      for _ in range(count)]
    return classes


def initialize_state(survey, i, starting_value):
    state = [None] * len(survey)
    state[i] = starting_value
    return state


def conclusion(survey, state, as_per):
    count = len(survey)
    i = as_per
    i_is_honest = state[i]
    if i_is_honest:
        if survey[i][i] is False:
            return False, "Perjury"
        for j in range(count):
            if i == j:
                continue
            j_as_per_i = survey[i][j]
            i_as_per_j = survey[j][i]
            if j_as_per_i is True and i_as_per_j is False:
                return False, "Paradox"
            state[j] = j_as_per_i
    else:
        for j in range(count):
            if i == j:
                continue
            j_as_per_i = survey[i][j]
            i_as_per_j = survey[j][i]
            if i_as_per_j is True:
                if state[j] is True:
                    return False, "Paradox"
                state[j] = False
    if any(honesty is None for honesty in state):
        for i, i_is_honest in enumerate(state):
            any_lies = any(survey[i][j] != state[j] for j in range(count))
            if i_is_honest is None:
                state[i] = not any_lies
            elif i_is_honest == any_lies:
                return False, "Perjury"
    for i, i_is_honest in enumerate(state):
        any_lies = any(survey[i][j] != state[j] for j in range(count))
        if i_is_honest == any_lies:
            return False, "Perjury"
    return True, state


def class_score(survey):
    states = []

    for i in range(len(survey)):
        state = initialize_state(survey, i, True)
        ok, state = conclusion(survey, state, as_per=i)
        if ok:
            states.append(state)
        state = initialize_state(survey, i, False)
        ok, state = conclusion(survey, state, as_per=i)
        if ok:
            states.append(state)

    def liar_count(state):
        return sum(1 for r in state if not r)

    if not states:
        return False, None

    scores = [liar_count(s) for s in states]
    return True, (min(scores), max(scores))


def print_class_score(index, class_survey):
    ok, score = class_score(class_survey)
    if ok:
        atleast, atmost = score
        print("Class Room#%s contains atleast %d and atmost %d liars" %
              (index, atleast, atmost))
    else:
        print("Class Room#%s is paradoxical" % index)


def run(in_file):
    class_surveys = load_classes(in_file)
    for index, class_survey in enumerate(class_surveys):
        print_class_score(index + 1, class_survey)


if __name__ == "__main__":
    # run(open("../test.txt"))
    from sys import stdin
    run(stdin)
