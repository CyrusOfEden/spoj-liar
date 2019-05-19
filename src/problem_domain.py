class Paradox(ValueError):
    pass


class HonestyRelationships():
    def __init__(self, class_survey):
        self.survey = class_survey
        self.statements = {}

    @property
    def student_count(self):
        return len(self.survey)

    def logical_statements(self):
        if self.statements:
            return self.statements
        self.statements = {
            i: self.conclusions_for_given_j_given_i_value(i)
            for i in range(self.student_count)
        }
        return self.statements

    def conclusions_for_given_j_given_i_value(self, i):
        rxns = {}
        for j in range(self.student_count):
            if i == j:
                continue
            if self.survey[i][j]:
                if self.survey[j][i]:
                    rxns[j] = self.__class__.same
                else:
                    rxns[j] = self.__class__.paradox_if
            elif self.survey[j][i]:
                rxns[j] = self.__class__.liar
            else:
                rxns[j] = self.__class__.liar_if
        return rxns

    @staticmethod
    def honest_if(i):
        if i: return True

    @staticmethod
    def liar(i):
        return False

    @staticmethod
    def liar_if(i):
        if i: return False

    @staticmethod
    def paradox_if(i):
        if i: raise Paradox("Invalid progression")

    @staticmethod
    def same(i):
        return i


class ConcludedState():
    def frontier(self):
        return (p for p in self.naive_frontier() if p.is_logical(depth=1))


class ConcludedHonestyState(ConcludedState):
    def __init__(self, concluded_state, relationships):
        self.state = concluded_state
        self.global_state = concluded_state[:]
        self.relationships = relationships

    @property
    def replies(self):
        return self.relationships.survey

    @property
    def conclusions(self):
        return self.relationships.logical_statements()

    def follows_conclusions(self, depth=1):
        student_count = len(self.state)
        additions = self.state[-depth:]
        for i, i_is_honest in enumerate(additions):
            for j in range(student_count):
                if i == j:
                    continue
                try:
                    """
                    If based on the logical conclusions of additional students i,
                    it changes something about the current state,
                    then this addition is not a valid one.
                    """
                    expected = self.conclusions[i][j](self.state[i])
                    if expected is not None and self.state[j] != expected:
                        return False
                except Paradox:
                    return False
        return True

    def global_validation(self):
        if all(honesty is None for honesty in self.state):
            """Totally inconclusive"""
            return True

        for i, i_is_honest in enumerate(self.state):
            i_lied = False
            for j in range(len(self.state)):
                if i == j:
                    continue
                if self.replies[i][j] != self.state[j]:
                    i_lied = True
                if i_is_honest is True and i_lied:
                    """Perjury!"""
                    return False
            if i_is_honest is False and not i_lied:
                "Perjury again!"
                return False
            self.state[i] = not i_lied

        return True

    def is_logical(self, depth=1):
        return self.is_solution() or self.follows_conclusions(depth=depth)

    def is_solution(self):
        return (self.is_complete() and self.global_validation()
                and self.follows_conclusions(depth=len(self.state)))

    def is_complete(self):
        return len(self.state) == len(self.conclusions)

    def naive_frontier(self):
        if self.is_complete():
            return []

        return [
            self.__class__([*self.state, value], self.relationships)
            for value in (True, False, None)
        ]

    def liar_count(self):
        return len(self.state) - sum(v for v in self.state if v is not None)

    def __lt__(self, other):
        return self.liar_count() < other.liar_count()
